# BibCleaner

BibCleaner is a lightweight Python GUI utility designed to help researchers and academics clean, manage, and merge BibTeX (`.bib`) reference files with minimal effort. 

## Features

* **Remove Abstracts:** Easily strip all `abstract` fields from your input files to reduce file size and clutter.
* **Remove URLs:** Optionally remove all `url` fields from the references.
* **Rename Records:** Automatically and sequentially rename your BibTeX citation keys. You can customize the renaming prefix (defaults to `zR`) and set the starting number (defaults to `21`).
* **Auto-Correction:** The application automatically verifies that every BibTeX entry ends with a closing brace `}`, appending it if missing to ensure file integrity.
* **Merge .bib Files:** A dedicated function allows you to select multiple `.bib` files and seamlessly combine them into a single output file.

## Prerequisites

* Python 3.x
* Built-in Python libraries: `tkinter`, `re`, `os` (No additional `pip` installations are required).

## Installation & Execution

1. Clone the repository or download the `BibCleaner.py` file.
2. Open your terminal or command prompt.
3. Run the script:
   ```bash
   python BibCleaner.py