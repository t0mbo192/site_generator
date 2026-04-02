import os
import sys

from copystatic import copy_files_recursive
from markdown_to_html import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    content_dir = os.path.join(project_root, "content")
    docs_dir = os.path.join(project_root, "docs")
    template_path = os.path.join(project_root, "template.html")

    copy_files_recursive(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)


if __name__ == "__main__":
    main()
