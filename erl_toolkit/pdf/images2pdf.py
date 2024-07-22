import fpdf
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-files", type=str, required=True, nargs="+")
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    pdf = fpdf.FPDF()
    for image in args.image_files:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)
    pdf.output(args.output)


if __name__ == "__main__":
    main()
