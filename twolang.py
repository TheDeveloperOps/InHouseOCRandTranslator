import pytesseract
from PIL import Image, ImageGrab, ImageFilter
from transformers import MarianMTModel, MarianTokenizer
from fpdf import FPDF
import io
import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import json

# ---------- Global Variables ----------

CONFIG_FILE = "config.json"

# ---------- OCR Preprocessing Functions ----------

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def set_tesseract_path():
    config = load_config()

    # Check if first-time setup is needed
    if 'tesseract_path' not in config or 'tessdata_path' not in config:
        messagebox.showinfo("First Time Setup", "Please select the Tesseract executable and tessdata folder.")

        # Ask for Tesseract executable
        tesseract_exe = filedialog.askopenfilename(title="Select tesseract.exe", filetypes=[("Tesseract Executable", "tesseract.exe")])
        if not tesseract_exe:
            messagebox.showerror("Error", "Tesseract executable not selected.")
            return

        # Ask for tessdata folder
        tessdata_folder = filedialog.askdirectory(title="Select tessdata folder")
        if not tessdata_folder:
            messagebox.showerror("Error", "tessdata folder not selected.")
            return

        config['tesseract_path'] = tesseract_exe
        config['tessdata_path'] = tessdata_folder
        save_config(config)

    # Set paths
    pytesseract.pytesseract.tesseract_cmd = config.get('tesseract_path')
    os.environ['TESSDATA_PREFIX'] = config.get('tessdata_path')

    # Debug
    print(f"[DEBUG] Tesseract CMD: {pytesseract.pytesseract.tesseract_cmd}")
    print(f"[DEBUG] TESSDATA_PREFIX: {os.environ.get('TESSDATA_PREFIX')}")

    # Double check if paths exist
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        messagebox.showerror("Error", f"Tesseract executable not found at {pytesseract.pytesseract.tesseract_cmd}")
    if not os.path.exists(os.environ.get('TESSDATA_PREFIX', '')):
        messagebox.showerror("Error", f"Tessdata folder not found at {os.environ.get('TESSDATA_PREFIX')}")


def preprocess_image(image):
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, thresh_image = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blurred_image = cv2.GaussianBlur(thresh_image, (5, 5), 0)
    return Image.fromarray(blurred_image)

def capture_image_from_clipboard():
    print("[INFO] Pasting image from clipboard...")
    image = ImageGrab.grabclipboard()
    if image is None:
        print("[ERROR] No image found in clipboard.")
        return None
    return preprocess_image(image)

def images_to_text(image, lang):
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except pytesseract.TesseractError as e:
        messagebox.showerror("Tesseract Error", str(e))
        return ""

# ---------- Translation Function (MarianMT) ----------

def translate_with_marian(text, src_lang='de', tgt_lang='en'):
    print("[INFO] Loading MarianMT model...")
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    chunks = [text[i:i+512] for i in range(0, len(text), 512)]
    translated = []

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
        translated_tokens = model.generate(**inputs)
        translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
        translated.extend(translated_text)

    return " ".join(translated)

# ---------- Save to PDF ----------

def save_text_to_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path)
    print(f"[✅] Translated output saved to PDF: {output_path}")

# ---------- Tkinter App ----------

def run_app():
    def handle_clipboard():
        lang = language_var.get()
        image = capture_image_from_clipboard()
        if image is None:
            messagebox.showerror("Error", "No image found in clipboard")
            return
        extracted = images_to_text(image, lang)
        extracted_text_box.delete("1.0", tk.END)
        extracted_text_box.insert(tk.END, extracted)
        # Set src_lang properly for MarianMT
        lang_map = {"deu": "de", "jpn": "ja", "spa": "es", "dan": "da"}
        src_lang_marian = lang_map.get(lang, "de")
        translated = translate_with_marian(extracted, src_lang=src_lang_marian)
        translated_text_box.delete("1.0", tk.END)
        translated_text_box.insert(tk.END, translated)

    def save_pdf():
        if not translated_text_box.get("1.0", tk.END).strip():
            messagebox.showwarning("Warning", "No translated text to save.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            save_text_to_pdf(translated_text_box.get("1.0", tk.END), output_path)

    def copy_to_clipboard():
        translated_text = translated_text_box.get("1.0", tk.END)
        root.clipboard_clear()
        root.clipboard_append(translated_text)
        messagebox.showinfo("Copied", "Translated text copied to clipboard!")

    def exit_app():
        root.destroy()

    # Initialize Tesseract path
    set_tesseract_path()

    root = tk.Tk()
    root.title("OCR & Translator")
    root.geometry("900x600")

    action_frame = tk.Frame(root)
    action_frame.pack(pady=10)

    tk.Button(action_frame, text="📋 Paste from Clipboard", command=handle_clipboard).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="📂 Save as PDF", command=save_pdf).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="📌 Copy to Clipboard", command=copy_to_clipboard).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="❌ Exit", command=exit_app).pack(side=tk.LEFT, padx=5)

    # Language Selection
    language_var = tk.StringVar(value='deu')  # Correct: 3-letter code

    language_frame = tk.Frame(root)
    language_frame.pack(pady=10)
    tk.Radiobutton(language_frame, text="German", variable=language_var, value="deu").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(language_frame, text="Japanese", variable=language_var, value="jpn").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(language_frame, text="Spanish", variable=language_var, value="spa").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(language_frame, text="Danish", variable=language_var, value="dan").pack(side=tk.LEFT, padx=5)

    tk.Label(root, text="📄 Extracted Text").pack()
    extracted_text_box = ScrolledText(root, height=10, wrap=tk.WORD)
    extracted_text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    tk.Label(root, text="🌐 Translated Text").pack()
    translated_text_box = ScrolledText(root, height=10, wrap=tk.WORD)
    translated_text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    root.mainloop()

# ---------- Run ----------

if __name__ == "__main__":
    run_app()