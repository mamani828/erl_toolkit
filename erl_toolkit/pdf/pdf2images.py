import pdf2images
import argparse
import matplotlib.pyplot as plt
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, required=True)
    parser.add_argument("--output-dir", type=str, required=True)
    parser.add_argument("--add-page-number", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    pages = pdf2images.convert_from_path(args.pdf, 500)
    if args.add_page_number:
        for i, page in enumerate(pages):
            plt.imshow(page)
            plt.title(f"{i + 1}", y=-0.01)
            plt.axis("off")
            plt.savefig(f"{args.output_dir}/page_{i+1}.png")
            plt.close()


if __name__ == "__main__":
    main()
