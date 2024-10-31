import fitz  # PyMuPDF
import sys
import csv

def extract_text_from_pdf(pdf_path):
    entries = []
    current_entry = {}

    # Open the PDF file
    with fitz.open(pdf_path) as pdf:
        # Iterate over each page
        for page_num, page in enumerate(pdf, start=1):
            # Split page text into lines
            lines = page.get_text().splitlines()

            # Iterate over lines to capture specific entries
            i = 0
            while i < len(lines):
                line = lines[i].strip()

                # Look for a line starting with a date format (DD.MM.YYYY)
                if (
                    len(line) == 10 and  # Format length check for DD.MM.YYYY
                    line[2] == '.' and line[5] == '.' and  # Period separators
                    line[:2].isdigit() and line[3:5].isdigit() and line[6:].isdigit()
                ):
                    current_entry['date'] = line
                    i += 1  # Move to the next line

                    # Check for a bank card number line
                    if i < len(lines) and len(lines[i]) == 16 and lines[i][:6].isdigit() and lines[i][6:12] == "******" and lines[i][12:].isdigit():
                        current_entry['card_number'] = lines[i]
                        i += 1  # Move to the next line

                        # Check for a recipient line
                        if i < len(lines) and lines[i].isupper():  # Recipient lines are uppercase
                            current_entry['recipient'] = lines[i]
                            i += 1  # Move to the next line

                            # Check for a sum line (ends with ",XX" for cents)
                            if i < len(lines) and ',' in lines[i]:
                                current_entry['amount'] = lines[i]
                                entries.append(current_entry)  # Add the entry to the list
                                current_entry = {}  # Reset for the next entry

                i += 1  # Continue to the next line

    return entries

if __name__ == "__main__":
    # Check if a PDF path argument was provided
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_text.py <pdf_path>")
        sys.exit(1)

    # Get the PDF path from command-line arguments
    pdf_path = sys.argv[1]

    # Extract entries from the PDF
    entries = extract_text_from_pdf(pdf_path)

    # Save entries to a CSV file
    output_file = "extracted_entries.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "card_number", "recipient", "amount"])
        writer.writeheader()
        writer.writerows(entries)

    print(f"Entry extraction complete. Entries saved to '{output_file}'.")
