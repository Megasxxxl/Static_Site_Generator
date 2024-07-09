from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node



block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in blocks:
        if block == "":
            continue
        block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    split_block_lines = block.split("\n")
    line_iteration = 0

    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    for line in split_block_lines:
        line_iteration += 1
        
        if line[0] == ">":
            if line_iteration == len(split_block_lines):
                return block_type_quote
        elif line[0] + line[1] == "* " or line[0] + line[1] == "- ":
            if line_iteration == len(split_block_lines):
                return block_type_unordered_list
        elif line[0] + line[1] + line[2] == f"{split_block_lines.index(line) + 1}. ":
            if line_iteration == len(split_block_lines):
                return block_type_ordered_list
        else:
            block_type_paragraph
    else:
        return block_type_paragraph 
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    text = block.lstrip("# ")
    level = len(block) - len(text) - 1
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)
    
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")  
    text = block[4:-3]
    children = text_to_children(text)
    node = ParentNode("code", children)
    return ParentNode("pre", [node])

def quote_to_html_node(block):
    split_block_lines = block.split("\n")
    list_lines = []

    for line in split_block_lines:
        if not line.startswith(">"):
            raise ValueError("Invalid Quote Block")
        list_lines.append(line.lstrip(">").strip())

    content = " ".join(list_lines)
    text = text_to_children(content)
    return ParentNode("blockquote", text)

def unordered_list_to_html_node(block):
    split_block_lines = block.split("\n")
    list_lines = []

    for line in split_block_lines:
        text = line[2:]
        children = text_to_children(text)
        list_lines.append(ParentNode("li", children))
    return ParentNode("ul", list_lines)
    

def ordered_list_to_html_node(block):
    split_block_lines = block.split("\n")
    list_lines = []

    for line in split_block_lines:
        if not line[0] + line[1] + line[2] == f"{split_block_lines.index(line) + 1}. ":
            raise ValueError("Invalid ordered list block")  
        
        text = line[2:].lstrip()
        children = text_to_children(text)
        list_lines.append(ParentNode("li", children))
    return ParentNode("ol", list_lines)



def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_box = []

    for block in blocks:
        convert_block = block_to_html_node(block)
        html_node_box.append(convert_block)
    return ParentNode("div", html_node_box, None)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    title = ""

    for block in blocks:
        if block.startswith("# "):
            title = block
            break
            
    if title == "":
        raise Exception("Title not found in markdown")
    return title

