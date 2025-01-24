import jinja2
import json
import yaml
import os


def build_notebooks(path):
    # Recursively search all the notebooks in the path
    for root, dirs, files in os.walk(path):


    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="."),
        autoescape=False
    )
    template = env.get_template(path)
    base_url = "https://raw.githubusercontent.com/username/myrepo/main"
    rendered_notebook_str = template.render(base_url=base_url)
    rendered_nbjson = json.loads(rendered_notebook_str)
    rendered_notebook_str = json.dumps(rendered_nbjson, indent=1)
    with open("my_notebook_final.ipynb", "w") as f:
        f.write(rendered_notebook_str)


# 1. Set up the Jinja environment


# 2. Load the template .ipynb
template = env.get_template("my_notebook_template.ipynb")

# 3. Define your base_url or any other vars you want to inject
#    For GitHub raw URLs, it might look like:
#    "https://raw.githubusercontent.com/<user>/<repo>/<branch>"
base_url = "https://raw.githubusercontent.com/username/myrepo/main"

# 4. Render the template
rendered_notebook_str = template.render(base_url=base_url)

# 5. (Optional) Validate or pretty-print
#    The result is still JSON, so let's parse and re-dump it in a standard format:
rendered_nbjson = json.loads(rendered_notebook_str)
rendered_notebook_str = json.dumps(rendered_nbjson, indent=1)

# 6. Write out the final notebook
with open("my_notebook_final.ipynb", "w") as f:
    f.write(rendered_notebook_str)

print("Notebook built successfully!")
