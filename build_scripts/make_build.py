# Copy a complete directory structure to a new location

import os

def delete(src):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if os.path.isdir(s):
            delete(s)
        else:
            os.remove(s)
    os.rmdir(src)

def copy(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy(s, d)
        else:
            if os.path.exists(d):
                os.remove(d)
            os.symlink(s, d)


delete("book_build")
copy("book", "book_build")
