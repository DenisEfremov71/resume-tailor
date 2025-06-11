import pypandoc

def save_docx_with_styles(markdown_text, output_path):
    # pypandoc will handle the conversion and file writing

    pypandoc.convert_text(
        markdown_text,
        'docx',
        format='md',
        outputfile=output_path
    )