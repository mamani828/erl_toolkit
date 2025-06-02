import pdf2image
import argparse
import matplotlib.pyplot as plt
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, required=True)
    parser.add_argument("--output-dir", type=str, required=True)
    parser.add_argument("--add-page-number", action="store_true")
    parser.add_argument("--single-page", action="store_true", help="Hint that the PDF has only one page")
    args = parser.parse_args()

    filename = os.path.basename(args.pdf)
    filename = os.path.splitext(filename)[0]
    os.makedirs(args.output_dir, exist_ok=True)
    pages = pdf2image.convert_from_path(args.pdf, 500)
    if args.add_page_number:
        for i, page in enumerate(pages):
            plt.imshow(page)
            plt.title(f"{i + 1}", y=-0.01)
            plt.axis("off")
            if args.single_page:
                plt.savefig(f"{args.output_dir}/{filename}.png")
                break
            else:
                plt.savefig(f"{args.output_dir}/page_{i+1}.png")
            plt.close()
    else:
        for i, page in enumerate(pages):
            if args.single_page:
                plt.imsave(f"{args.output_dir}/{filename}.png", page)
                break
            else:
                plt.imsave(f"{args.output_dir}/page_{i+1}.png", page)


if __name__ == "__main__":
    main()
