import os

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from textnode import TextNode, TextType, text_node_to_html


def get_heading_level(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    return level


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html(node) for node in text_nodes]


def paragraph_block_to_html_node(block):
    paragraph_text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph_text))


def heading_block_to_html_node(block):
    heading_level = get_heading_level(block)
    heading_text = block[heading_level + 1 :]
    return ParentNode(f"h{heading_level}", text_to_children(heading_text))


def code_block_to_html_node(block):
    lines = block.split("\n")
    code_text = "\n".join(lines[1:-1]) + "\n"
    code_text_node = TextNode(code_text, TextType.TEXT)
    code_child = text_node_to_html(code_text_node)
    code_node = ParentNode("code", [code_child])
    return ParentNode("pre", [code_node])


def quote_block_to_html_node(block):
    quote_lines = []
    for line in block.split("\n"):
        quote_lines.append(line[1:].lstrip())
    quote_text = " ".join(quote_lines)
    return ParentNode("blockquote", text_to_children(quote_text))


def list_item_to_html_node(text):
    return ParentNode("li", text_to_children(text))


def unordered_list_block_to_html_node(block):
    list_items = []
    for line in block.split("\n"):
        list_items.append(list_item_to_html_node(line[2:]))
    return ParentNode("ul", list_items)


def ordered_list_block_to_html_node(block):
    list_items = []
    for line in block.split("\n"):
        list_item_text = line.split(". ", 1)[1]
        list_items.append(list_item_to_html_node(list_item_text))
    return ParentNode("ol", list_items)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_block_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_block_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_block_to_html_node(block)

    raise ValueError(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def extract_title(markdown):
    for line in markdown.split("\n"):
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line[2:].strip()
    raise ValueError("No title found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    with open(from_path, encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, encoding="utf-8") as template_file:
        template = template_file.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(full_html)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    for entry in sorted(os.listdir(dir_path_content)):
        source_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(source_path):
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
                basepath,
            )
            continue

        if not entry.endswith(".md"):
            continue

        html_dest_path = os.path.splitext(destination_path)[0] + ".html"
        generate_page(source_path, template_path, html_dest_path, basepath)
