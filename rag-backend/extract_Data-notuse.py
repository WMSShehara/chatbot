

# extract images from pdf
# def extract_images(pdf_path, output_folder):
#     doc = fitz.open(pdf_path)
#     for page_num, page in enumerate(doc, start=1):
#         images = page.get_images(full=True)
#         for img_index, img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]
#             image_ext = base_image["ext"]
#             image_path = f"{output_folder}/page{page_num}_img{img_index}.{image_ext}"
#             with open(image_path, "wb") as img_file:
#                 img_file.write(image_bytes)
#             print(f"Saved image: {image_path}")

# # Example usage
# extract_images("BioResoBook.pdf", "output_images")

# def extract_text_with_positions(pdf_path):
#     doc = fitz.open(pdf_path)
#     for page_num, page in enumerate(doc, start=1):
#         print(f"Page {page_num} text positions:")
#         for block in page.get_text("dict")["blocks"]:
#             for line in block.get("lines", []):
#                 for span in line.get("spans", []):
#                     text = span["text"]
#                     bbox = span["bbox"]
#                     print(f"Text: {text} | Position: {bbox}")

# # Example usage
# extract_text_with_positions("example.pdf")
