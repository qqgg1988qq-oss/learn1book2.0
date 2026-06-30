import fitz
import pytesseract
from PIL import Image
import os
import io
import sys


def extract_text_from_pdf(pdf_path, output_dir=None, lang="chi_sim+eng"):
    """
    Extract text from a PDF file. For image-based PDFs, use OCR.
    Saves output as Markdown file in the same directory or specified output_dir.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Optional directory to save the extracted text. If None, saves next to PDF.
        lang: Tesseract OCR language(s), default chi_sim+eng for Chinese+English.
    
    Returns:
        Path to the output markdown file.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    all_text = []
    
    for page_idx, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            all_text.append(f"--- Page {page_idx + 1} ---\n{text}")
        else:
            # No text layer — extract images and OCR
            images = page.get_images()
            page_text = []
            for img_idx, img in enumerate(images):
                xref = img[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n > 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    img_data = pix.tobytes("png")
                    img_obj = Image.open(io.BytesIO(img_data))
                    ocr_text = pytesseract.image_to_string(img_obj, lang=lang)
                    if ocr_text.strip():
                        page_text.append(ocr_text)
                except Exception as e:
                    print(f"  [WARN] Page {page_idx + 1} img {img_idx}: {e}", file=sys.stderr)
            if page_text:
                all_text.append(f"--- Page {page_idx + 1} ---\n" + "\n".join(page_text))
    
    # Determine output path
    base_name = os.path.basename(pdf_path).replace(".pdf", ".md")
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, base_name)
    else:
        out_path = pdf_path.replace(".pdf", ".md")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name.replace('.md', '')}\n\n")
        f.write("\n\n".join(all_text))
    
    print(f"[DONE] {base_name} - {len(doc)} pages, saved to {out_path}")
    return out_path


def batch_extract(folder_path, output_dir=None, lang="chi_sim+eng"):
    """
    Batch extract text from all PDFs in a folder.
    
    Args:
        folder_path: Directory containing PDF files
        output_dir: Optional directory to save extracted texts
        lang: Tesseract OCR language(s)
    
    Returns:
        List of paths to output markdown files
    """
    results = []
    for fname in sorted(os.listdir(folder_path)):
        if fname.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, fname)
            try:
                out_path = extract_text_from_pdf(pdf_path, output_dir, lang)
                results.append(out_path)
            except Exception as e:
                print(f"[ERROR] {fname}: {e}", file=sys.stderr)
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_text.py <pdf_path_or_folder> [output_dir] [lang]")
        print("  lang: default 'chi_sim+eng', use 'eng' for English-only")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    lang = sys.argv[3] if len(sys.argv) > 3 else "chi_sim+eng"
    
    if os.path.isdir(input_path):
        batch_extract(input_path, output_dir, lang)
    else:
        extract_text_from_pdf(input_path, output_dir, lang)
