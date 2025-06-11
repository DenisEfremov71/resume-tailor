def insert_links_into_markdown(markdown_text, links):
    """
    Inserts all links into the markdown text.
    Each link is formatted as **[text](url)**.
    """

    markdown_text_with_links = markdown_text

    for link in links:
        markdown_text_with_links = markdown_text_with_links.replace(f"{link['text']}", f"**[{link['text']}]({link['uri']})**", 1)

    return markdown_text_with_links