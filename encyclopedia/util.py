import re

from markdown2 import Markdown
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def delete_entry(title):
    """
    Delete an encyclopedia entry, given its title.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    
    
def markdown_to_html_converter(markdown):
    """
    Convert markdown to html
    """
    markdowner = Markdown()
    return markdowner.convert(get_entry(markdown))


default_textarea = '''
# THIS IS A BIG TITLE

## This is a smaller title

##### Here are examples of what you can do :

- You can also make text **bold**... whoa!
- Or _italic_.
- Or... wait for it... **_both!_**

There's also [links](https://cs50.harvard.edu/web/2020/projects/1/wiki/)

<img src="https://static.djangoproject.com/img/logos/django-logo-negative.png" alt="Django logo" width="300" height="150">
'''