import re

from textnode import (TextNode, text_type_bold, text_type_code, text_type_italic, text_type_text, text_type_image, text_type_link)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
            
        split_text_variable = node.text.split(delimiter)    
        
        if len(split_text_variable) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for string in split_text_variable:
            index = split_text_variable.index(string)
            

            if index % 2 == 0:
                new_nodes.append(TextNode(string, node.text_type))

            else:
                new_nodes.append(TextNode(string, text_type))
    
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:    
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        image_extracts = extract_markdown_images(original_text)
        
        
        if len(image_extracts) == 0:
            new_nodes.append(old_node)
            continue

        for image_extract in image_extracts:
            image_split = original_text.split(f"![{image_extract[0]}]({image_extract[1]})", 1)

            if len(image_split) != 2:
                raise ValueError("Invalid Markdown, image section not closed")
               
            if image_split[0] != "":
                new_nodes.append(TextNode(image_split[0], text_type_text))
            new_nodes.append(TextNode(image_extract[0], text_type_image, image_extract[1]))
                
            original_text = image_split[1]

        if original_text != "":    
            new_nodes.append(TextNode(original_text, text_type_text))       
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:    
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        link_extracts = extract_markdown_links(original_text)
            
        if len(link_extracts) == 0:
            new_nodes.append(old_node)
            continue

        for link_extract in link_extracts:
            link_split = original_text.split(f"[{link_extract[0]}]({link_extract[1]})", 1)
                
            if len(link_split) != 2:
                raise ValueError("Invalid Markdown, image section not closed")
               
            if link_split[0] != "":
                new_nodes.append(TextNode(link_split[0], text_type_text))
            new_nodes.append(TextNode(link_extract[0], text_type_link, link_extract[1]))
                
            original_text = link_split[1]
            
        if original_text != "":    
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    node_change_1 = split_nodes_delimiter([node], "**", text_type_bold)
    node_change_2 = split_nodes_delimiter(node_change_1, "*", text_type_italic)
    node_change_3 = split_nodes_delimiter(node_change_2, "`", text_type_code)
    node_change_4 = split_nodes_image(node_change_3)
    node_change_5 = split_nodes_link(node_change_4)
    return node_change_5
