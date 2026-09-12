import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os

# Define the main application window
class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BibCleaner")
        self.root.geometry("500x600")  # Increased window size for additional fields
        self.root.configure(bg="#f0f4c3")  # Set background color
        self.root.attributes("-topmost", True)  # Keep window on top

        # Define styles
        label_font = ("Helvetica", 12, "bold")
        entry_bg = "#f5f5f5"
        button_bg = "#90caf9"
        button_fg = "black"

        # Input file label and entry
        self.input_label = tk.Label(root, text="File Name (without .bib):", font=label_font, bg="#f0f4c3", fg="#37474f")
        self.input_label.pack(pady=5)
        
        self.input_entry = tk.Entry(root, width=50, bg=entry_bg)
        self.input_entry.pack(pady=5)
        
        self.browse_input_button = tk.Button(root, text="Browse", command=self.browse_input_file, bg=button_bg, fg=button_fg)
        self.browse_input_button.pack(pady=5)

        # Output file label and entry
        self.output_label = tk.Label(root, text="Output File Name (without .bib):", font=label_font, bg="#f0f4c3", fg="#37474f")
        self.output_label.pack(pady=5)
        
        self.output_entry = tk.Entry(root, width=50, bg=entry_bg)
        self.output_entry.pack(pady=5)
        
        self.browse_output_button = tk.Button(root, text="Browse", command=self.browse_output_file, bg=button_bg, fg=button_fg)
        self.browse_output_button.pack(pady=5)
        
        # Checkboxes for processing options
        self.remove_abstracts = tk.BooleanVar(value=True)  # Default to checked
        self.rename_records = tk.BooleanVar(value=True)  # Default to checked
        self.remove_links = tk.BooleanVar(value=False)  # Default to unchecked

        self.abstract_checkbox = tk.Checkbutton(root, text="Remove All Abstracts", variable=self.remove_abstracts, font=("Helvetica", 10), bg="#f0f4c3")
        self.abstract_checkbox.pack(pady=5)

        # Rename records checkbox with command to enable/disable related fields
        self.rename_checkbox = tk.Checkbutton(root, text="Rename Records", variable=self.rename_records, command=self.toggle_rename_fields, font=("Helvetica", 10), bg="#f0f4c3")
        self.rename_checkbox.pack(pady=5)

        # Additional fields for renaming configuration
        self.start_number_label = tk.Label(root, text="Starting Number for Renaming:", font=("Helvetica", 10), bg="#f0f4c3", fg="#37474f")
        self.start_number_label.pack(pady=5)
        
        self.start_number_entry = tk.Entry(root, width=10, bg=entry_bg)
        self.start_number_entry.insert(0, "21")  # Default starting number
        self.start_number_entry.pack(pady=5)

        self.prefix_label = tk.Label(root, text="Prefix for Renaming (e.g., 'zR'):", font=("Helvetica", 10), bg="#f0f4c3", fg="#37474f")
        self.prefix_label.pack(pady=5)
        
        self.prefix_entry = tk.Entry(root, width=10, bg=entry_bg)
        self.prefix_entry.insert(0, "zR")  # Default prefix
        self.prefix_entry.pack(pady=5)

        # Checkbox for removing links (url only)
        self.links_checkbox = tk.Checkbutton(root, text="Remove All URLs", variable=self.remove_links, font=("Helvetica", 10), bg="#f0f4c3")
        self.links_checkbox.pack(pady=5)

        # Process button
        self.process_button = tk.Button(root, text="Process File", command=self.process_file, bg="#66bb6a", fg="white", font=("Helvetica", 10, "bold"))
        self.process_button.pack(pady=10)

        # Button to merge multiple .bib files
        self.merge_button = tk.Button(root, text="Merge Multiple .bib Files", command=self.merge_bib_files, bg="#ffa726", fg="white", font=("Helvetica", 10, "bold"))
        self.merge_button.pack(pady=10)

    def toggle_rename_fields(self):
        if self.rename_records.get():
            self.start_number_entry.config(state="normal")
            self.prefix_entry.config(state="normal")
        else:
            self.start_number_entry.config(state="disabled")
            self.prefix_entry.config(state="disabled")

    # Browse input file
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("BibTeX files", "*.bib"), ("All files", "*.*")])
        if file_path:
            file_name = os.path.splitext(os.path.basename(file_path))[0]  # Remove .bib extension
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_name)
    
    # Browse output file
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bib", filetypes=[("BibTeX files", "*.bib"), ("All files", "*.*")])
        if file_path:
            file_name = os.path.splitext(os.path.basename(file_path))[0]  # Remove .bib extension
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_name)

    # Process file
    def process_file(self):
        input_file_name = self.input_entry.get()
        output_file_name = self.output_entry.get()

        # Validate file names
        if not input_file_name or not output_file_name:
            messagebox.showerror("Error", "Please specify both input and output file names.")
            return

        # Construct full paths in the current directory with .bib extension
        input_file_path = os.path.join(os.getcwd(), f"{input_file_name}.bib")
        output_file_path = os.path.join(os.getcwd(), f"{output_file_name}.bib")

        try:
            # Read the content of the file
            with open(input_file_path, 'r') as file:
                content = file.read()

            # Remove abstracts if checkbox is selected
            if self.remove_abstracts.get():
                content = re.sub(r'abstract = {.*?},\n\s*', '', content, flags=re.DOTALL)

            # Remove URLs if checkbox is selected
            if self.remove_links.get():
                content = re.sub(r'url = {.*?},\n\s*', '', content, flags=re.DOTALL)

            # Rename each record if checkbox is selected
            if self.rename_records.get():
                pattern = r'(@\w+{)([^,]+)'

                # Retrieve starting number and prefix, and handle invalid input
                try:
                    start_number = int(self.start_number_entry.get() or 21)  # Use default if empty
                except ValueError:
                    messagebox.showerror("Error", "Starting number must be an integer.")
                    return

                # Use "zR" as the prefix if the user has not modified it from the default value
                prefix = self.prefix_entry.get() if self.prefix_entry.get() else "zR"

                def replace_record_name(match):
                    nonlocal start_number
                    new_name = f"{prefix}{start_number}"
                    start_number += 1
                    return f"{match.group(1)}{new_name}"

                content = re.sub(pattern, replace_record_name, content)

            # Verify that each reference ends with a "}"
            records = content.split('\n@')  # Split content by BibTeX entries
            corrected_records = []

            for i, record in enumerate(records):
                if i > 0:  # Add "@" to each entry after the first one
                    record = '@' + record

                # Check if the record ends with "}", if not, add it
                if not record.strip().endswith('}'):
                    record = record.strip() + '\n}'

                corrected_records.append(record)

            # Join the corrected records into the final content
            corrected_content = "\n\n".join(corrected_records)

            # Save the final content to a new file
            with open(output_file_path, 'w') as file:
                file.write(corrected_content)

            messagebox.showinfo("Success", f"The processed file has been saved to:\n{output_file_name}.bib")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Merge multiple .bib files
    def merge_bib_files(self):
        # Select multiple .bib files
        file_paths = filedialog.askopenfilenames(filetypes=[("BibTeX files", "*.bib"), ("All files", "*.*")])
        if not file_paths:
            return  # Exit if no files were selected

        # Output file path for the merged content
        output_file_path = filedialog.asksaveasfilename(defaultextension=".bib", filetypes=[("BibTeX files", "*.bib"), ("All files", "*.*")])
        if not output_file_path:
            return  # Exit if no output file was specified

        try:
            merged_content = ""
            # Read and merge content from each selected file
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    merged_content += file.read() + "\n"

            # Save the merged content to the specified output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(merged_content)

            messagebox.showinfo("Success", f"The .bib files have been merged and saved to:\n{output_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging files: {str(e)}")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessorApp(root)
    root.mainloop()
