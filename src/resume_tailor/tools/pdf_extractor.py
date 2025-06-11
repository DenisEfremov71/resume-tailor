import fitz


def extract_text_and_style(resume_path: str) -> dict:
    """
    Extracts clean text and layout styling info from a resume PDF.

    Returns:
        {
            "text": full text content as a string,
            "styles": [
                {
                    "text": ...,
                    "font": ...,
                    "size": ...,
                    "color": ...,
                    "bbox": [...]
                },
                ...
            ]
        }
    """
    doc = fitz.open(resume_path)
    full_text = ""
    styles = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            styles.append(
                                {
                                    "page": page_num,
                                    "text": text,
                                    "font": span["font"],
                                    "size": span["size"],
                                    "color": span["color"],
                                    "bbox": span["bbox"],
                                }
                            )
                            full_text += text + " "
        full_text += "\n"

    return {"text": full_text.strip(), "styles": styles}


def extract_links_with_text_first_page(resume_path: str) -> list:
    """
    Extracts all embedded links (URLs) and their associated text from the first page of a PDF.

    Returns:
        [
            {
                "text": ...,  # The text that is hyperlinked
                "uri": ...,   # The URL
                "rect": ...   # The rectangle area of the link
            },
            ...
        ]
    """
    doc = fitz.open(resume_path)
    links = []
    if len(doc) > 0:
        page = doc[0]  # Only first page
        for link in page.get_links():
            if link["uri"] and link["from"]:
                rect = fitz.Rect(link["from"])
                text = page.get_textbox(rect).strip()
                if text:
                    links.append({
                        "text": text,
                        "uri": link["uri"],
                        "rect": link["from"]
                    })
    return links
