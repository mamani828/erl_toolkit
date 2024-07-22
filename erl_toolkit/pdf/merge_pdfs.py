import PyPDF2
import os
import argparse


# https://pypdf.readthedocs.io/en/latest/user/merging-pdfs.html
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdfs",
        type=str,
        required=True,
        nargs="+",
        help="list of pdf_file or pdf_file:page_start:page_end(inclusive)",
    )
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    merger = PyPDF2.PdfMerger()
    for pdf in args.pdfs:
        if pdf.endswith(".pdf"):
            merger.append(pdf)
        else:
            splits = pdf.split(":")
            pdf = ''.join(splits[:-2])
            page_start = int(splits[-2]) - 1
            page_end = int(splits[-1])
            merger.append(pdf, pages=(page_start, page_end))
    merger.write(args.output)
    merger.close()


if __name__ == "__main__":
    main()
