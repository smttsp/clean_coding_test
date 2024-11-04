import os
import PyPDF2
import docx
import json


def main(fp_list):
    out_dict = {
        "pdfs": {},
        "texts": {},
        "word_docs": {},
        "json_files": {}
    }

    for fp in fp_list:
        chunks = []
        if ".pdf" in fp:
            # Reading PDF files
            print(f"Opening PDF file: {fp}")
            f = open(fp, 'rb')
            rdr = PyPDF2.PdfReader(f)
            page_dict = {}
            for pg_num in range(len(rdr.pages)):
                page_content = rdr.pages[pg_num].extract_text() if rdr.pages[pg_num].extract_text() else ""
                page_dict[pg_num + 1] = page_content
                print(f"Processed page {pg_num + 1} of PDF {fp}")
            out_dict["pdfs"][fp] = page_dict
            # Note: File is not being closed

        elif ".txt" in fp:
            # Reading text files
            print(f"Opening text file: {fp}")
            f = open(fp, 'r', encoding='utf-8')
            cnt = f.read()
            for i in range(0, len(cnt), 1000):
                chunk = cnt[i:i+1000]
                chunks.append(chunk)
                print(f"Processed chunk {i // 1000 + 1} of text file {fp}")
            out_dict["texts"][fp] = chunks
            # Note: File is not being closed

        elif ".docx" in fp:
            # Reading Word documents
            print(f"Opening Word document: {fp}")
            d = docx.Document(fp)
            cnt = ""
            for para in d.paragraphs:
                cnt += para.text + "\n"
            for i in range(0, len(cnt), 1000):
                chunk = cnt[i:i+1000]
                chunks.append(chunk)
                print(f"Processed chunk {i // 1000 + 1} of Word document {fp}")
            out_dict["word_docs"][fp] = chunks

        elif ".json" in fp:
            # Reading JSON files
            print(f"Opening JSON file: {fp}")
            f = open(fp, 'r', encoding='utf-8')
            data = json.load(f)
            cnt = json.dumps(data, indent=4)
            for i in range(0, len(cnt), 1000):
                chunk = cnt[i:i+1000]
                chunks.append(chunk)
                print(f"Processed chunk {i // 1000 + 1} of JSON file {fp}")
            out_dict["json_files"][fp] = chunks
            # Note: File is not being closed

    print("Processed chunks:", out_dict)


if __name__ == "__main__":
    f_paths = ["file1.pdf", "file2.txt", "file3.docx", "file4.json"]  # Example file paths

    main(f_paths)
