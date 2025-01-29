import subprocess
import jinja2
import yaml
import json
import os
import shutil
import filecmp

# Directory paths
SOURCE_DIR = "./book"
BUILD_DIR = "./book_build"
JUPYTER_BOOK_BUILD_CMD = ["jupyter-book", "build", "book_build"]

skip_dirs = ["_build"]


def copy_if_changed(src_dir, dest_dir):
    """
    Recursively copy files from src_dir to dest_dir, only if the file has changed.
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        # Compute relative path to maintain directory structure
        relative_path = os.path.relpath(root, src_dir)

        if any(relative_path == d or relative_path.startswith(d + os.sep) for d in skip_dirs):
            continue

        # if the current directory is in skip list, pass

        current_dest_dir = os.path.join(dest_dir, relative_path)

        # Ensure the current destination subdirectory exists
        os.makedirs(current_dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(current_dest_dir, file)

            # Copy only if the file doesn't exist in destination or content differs
            if not os.path.exists(dest_file) or not filecmp.cmp(src_file, dest_file, shallow=False):
                shutil.copy2(src_file, dest_file)
                # print(f"Copied: {src_file} -> {dest_file}")
            # else:
            # print(f"Skipped (unchanged): {src_file}")


def build_notebook(path=BUILD_DIR, yaml_path=f"{BUILD_DIR}/_config.yml"):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="."),
        autoescape=False
    )
    # Load yaml file
    with open(yaml_path) as f:
        variables = yaml.safe_load(f)["parse"]["myst_substitutions"]

    template = env.get_template(path)

    rendered_notebook_str = template.render(**variables)
    rendered_nbjson = json.loads(rendered_notebook_str)
    rendered_notebook_str = json.dumps(rendered_nbjson, indent=1)
    # Write out the final notebook with the same name but with _colab appended
    with open(path.replace(".ipynb", ".ipynb"), "w") as f:
        f.write(rendered_notebook_str)


def build():
    copy_if_changed(SOURCE_DIR, BUILD_DIR)

    _d = None
    with open(f"{BUILD_DIR}/_config.yml") as f:
        _d = yaml.safe_load(f)
        _d["repository"]["path_to_book"] = "book_build"

    yaml.safe_dump(_d, open(f"{BUILD_DIR}/_config.yml", "w"))

    for root, dirs, files in os.walk(BUILD_DIR):
        for file in files:
            if file.endswith(".ipynb") and not file.endswith("_colab.ipynb"):
                build_notebook(os.path.join(root, file))

    print(f"Preprocessed notebooks saved to: {BUILD_DIR}")


if __name__ == '__main__':
    build()
