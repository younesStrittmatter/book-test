import jinja2
import json
import yaml
import os


def build_all(path="."):
    # Recursively search all the notebooks in the path
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".ipynb") and not file.endswith("_colab.ipynb"):
                build_notebook(os.path.join(root, file))

def build_notebook(path=".", yaml_path="./_config.yml"):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="."),
        autoescape=False
    )

    # Load yaml file
    with open(yaml_path) as f:
        variables = yaml.safe_load(f)["parse"]["myst_substitutions"]

    template = env.get_template(path)
    print(template)


    rendered_notebook_str = template.render(**variables)
    rendered_nbjson = json.loads(rendered_notebook_str)
    rendered_notebook_str = json.dumps(rendered_nbjson, indent=1)
    # Write out the final notebook with the same name but with _colab appended
    with open(path.replace(".ipynb", "_colab.ipynb"), "w") as f:
        f.write(rendered_notebook_str)

if __name__ == "__main__":
    build_all()

