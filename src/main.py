import os

from copystatic import copy_files_recursive
from markdown_to_html import generate_pages_recursive


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    content_dir = os.path.join(project_root, "content")
    public_dir = os.path.join(project_root, "public")
    template_path = os.path.join(project_root, "template.html")

    copy_files_recursive(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
