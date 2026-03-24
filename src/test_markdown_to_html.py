import os
import tempfile
import unittest

from markdown_to_html import (
    extract_title,
    generate_page,
    generate_pages_recursive,
    markdown_to_html_node,
)


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_mixed_blocks(self):
        md = """
    # Main heading

    > quoted _text_
    > across lines

    - first item
    - second **item**

    1. ordered one
    2. ordered two
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main heading</h1><blockquote>quoted <i>text</i> across lines</blockquote><ul><li>first item</li><li>second <b>item</b></li></ul><ol><li>ordered one</li><li>ordered two</li></ol></div>",
        )

    def test_missing_title_raises(self):
        md = """
    This is a paragraph without a title
    """
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_title_extraction(self):
        md = """
    # This is the title 
    This is a paragraph
    """
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_generate_page_creates_html_file(self):
        markdown = """# Hello World

This is a paragraph with **bold** text.
"""
        template = """<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            from_path = os.path.join(tmpdir, "content", "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "public", "nested", "index.html")

            os.makedirs(os.path.dirname(from_path), exist_ok=True)
            with open(from_path, "w", encoding="utf-8") as markdown_file:
                markdown_file.write(markdown)
            with open(template_path, "w", encoding="utf-8") as template_file:
                template_file.write(template)

            generate_page(from_path, template_path, dest_path)

            with open(dest_path, encoding="utf-8") as dest_file:
                generated = dest_file.read()

        self.assertEqual(
            generated,
            "<html><head><title>Hello World</title></head><body><div><h1>Hello World</h1><p>This is a paragraph with <b>bold</b> text.</p></div></body></html>",
        )

    def test_generate_pages_recursive_creates_nested_html_files(self):
        template = """<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = os.path.join(tmpdir, "content")
            public_dir = os.path.join(tmpdir, "public")
            template_path = os.path.join(tmpdir, "template.html")

            root_markdown_path = os.path.join(content_dir, "index.md")
            nested_markdown_path = os.path.join(content_dir, "blog", "post.md")
            asset_path = os.path.join(content_dir, "notes.txt")

            os.makedirs(os.path.dirname(nested_markdown_path), exist_ok=True)

            with open(root_markdown_path, "w", encoding="utf-8") as markdown_file:
                markdown_file.write("# Home\n\nWelcome home.")

            with open(nested_markdown_path, "w", encoding="utf-8") as markdown_file:
                markdown_file.write("# Post\n\nNested content.")

            with open(asset_path, "w", encoding="utf-8") as asset_file:
                asset_file.write("ignore me")

            with open(template_path, "w", encoding="utf-8") as template_file:
                template_file.write(template)

            generate_pages_recursive(content_dir, template_path, public_dir)

            root_html_path = os.path.join(public_dir, "index.html")
            nested_html_path = os.path.join(public_dir, "blog", "post.html")

            self.assertTrue(os.path.exists(root_html_path))
            self.assertTrue(os.path.exists(nested_html_path))
            self.assertFalse(os.path.exists(os.path.join(public_dir, "notes.html")))

            with open(root_html_path, encoding="utf-8") as root_html_file:
                root_html = root_html_file.read()

            with open(nested_html_path, encoding="utf-8") as nested_html_file:
                nested_html = nested_html_file.read()

        self.assertEqual(
            root_html,
            "<html><head><title>Home</title></head><body><div><h1>Home</h1><p>Welcome home.</p></div></body></html>",
        )
        self.assertEqual(
            nested_html,
            "<html><head><title>Post</title></head><body><div><h1>Post</h1><p>Nested content.</p></div></body></html>",
        )

    if __name__ == "__main__":
        unittest.main()
