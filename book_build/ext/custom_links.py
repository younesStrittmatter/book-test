def setup(app):
    """
    Sphinx will call this function to initialize the extension.
    """
    app.connect("html-page-context", inject_jinja_variables)

def inject_jinja_variables(app, pagename, templatename, context, doctree):
    """
    Inject custom Jinja variables into the page context.
    """
    print(f"Injecting Jinja variables into page: {pagename}")
    context["my_variable"] = "Hello from Sphinx!"
    context["another_variable"] = "Welcome to Jupyter Book with custom Jinja!"
