# 🖥️ Offline OCR and Translator App

A fully offline Python application to extract text from images (screenshots, snips, etc.), translate it into your preferred language, and save the output as a clean PDF.  
No internet connection is needed after setup!

---

## 🚀 Features
- 📋 Capture image directly from the clipboard.
- 🛠️ Preprocess images to boost OCR (Optical Character Recognition) accuracy.
- 🧠 Extract text using Tesseract OCR engine.
- 🌍 Translate text offline using Argos Translate.
- 📄 Save translated text into a neatly formatted PDF.
- 🖱️ Simple and intuitive Tkinter-based GUI.

---

## 📦 Prerequisites

Make sure you have the following installed:

```bash
pip install pytesseract Pillow opencv-python numpy argostranslate fpdf
```

You will also need:
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.
- `DejaVuSans.ttf` font file for proper PDF text formatting.

---

## 🔥 Setup Instructions

1. **Install Tesseract**  
   Download and install Tesseract OCR. During installation, note the installation path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`).

2. **Download Offline Translation Models**  
   Run `satisfyDependency.py` to download the required Argos Translate language models (German → English, Japanese → English, etc.).

3. **First Launch Setup**  
   - When you open the app for the first time, you will be asked to locate:
     - `tesseract.exe`
     - `tessdata` folder
   - These settings are saved automatically for future use (`config.json`).

---

## 🏗️ Folder Structure

```
OCR_Translator_App/
│
├── DejaVuSans.ttf          # Font for PDF generation
├── config.json             # Auto-generated configuration file
├── InHouseOcrCumTranslator.py  # Main Application
├── satisfyDependency.py    # Script to download translation models
└── README.md               # Documentation
```

---

## 🎯 How to Use

1. **Launch** `InHouseOcrCumTranslator.py`
2. **Paste an Image**: Click "Paste from Clipboard" after copying a screenshot.
3. **Select Language**: Choose the source language of the text.
4. **Translate**: Extract and translate the text offline.
5. **Save**: Export the translated text to a PDF file.
6. **Copy**: Optionally copy the translated text to clipboard.

---

## ⚙️ Technologies Used

- **Python**
- **Tesseract OCR**
- **Argos Translate**
- **Tkinter**
- **OpenCV**
- **Pillow**
- **FPDF**

---

## 💡 Future Improvements

- Support for multiple pages in a single PDF.
- Batch processing multiple images.
- Additional language options.
- Integrated translation history.

---

## 📜 License

This project is open-source and free to use for learning and development purposes.

---

# 🙌 Happy Translating!

---

Would you also like me to generate a **shorter version** for GitHub if you want something more "minimal"? 🎯  
Or a **banner** text like: `![Offline OCR Translator Banner](your-image-url)`? 🎨
