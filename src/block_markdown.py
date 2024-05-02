import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        cleaned_blocks.append(block)    
    return cleaned_blocks


def block_to_block_type(markdown: str) -> str:
    if re.match(r"^#{1,6}\s.", markdown):
        return block_type_heading
    elif re.match(r"^`{3}[\s\S]+`{3}$", markdown, flags=re.MULTILINE):
        return block_type_code
    elif re.match(r"^>[^\n]*(?:\n>[^\n]*)*$", markdown):
        return block_type_quote
    elif re.match(r"^(?:\s*[-\*\+]\s+.+(\n|$))+", markdown):
        return block_type_unordered_list
    else:
        return block_type_paragraph
