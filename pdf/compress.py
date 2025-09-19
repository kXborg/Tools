import PyPDF2
import os
import argparse
from pathlib import Path

def optimize_pdf(input_path, output_path):
    """
    Optimize a PDF file by compressing its content streams.
    
    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path where the optimized PDF will be saved
    Returns:
        bool: True if optimization succeeded, False otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            print(f"Error: Input file '{input_path}' does not exist.")
            return False

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the input PDF
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()

            # Copy all pages to the writer
            for page in reader.pages:
                # Compress the page's content streams
                page.compress_content_streams()  # No compression level parameter
                writer.add_page(page)

            # Write the optimized PDF to the output file
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            # Verify the output file was created
            if os.path.exists(output_path):
                input_size = os.path.getsize(input_path) / 1024  # Size in KB
                output_size = os.path.getsize(output_path) / 1024  # Size in KB
                print(f"Optimization complete!")
                print(f"Input file size: {input_size:.2f} KB")
                print(f"Output file size: {output_size:.2f} KB")
                print(f"Size reduction: {(input_size - output_size) / input_size * 100:.2f}%")
                return True
            else:
                print(f"Error: Failed to create output file '{output_path}'.")
                return False

    except Exception as e:
        print(f"Error during optimization: {str(e)}")
        return False

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Optimize a PDF file by compressing its content streams.")
    parser.add_argument("input_pdf", type=str, help="Path to the input PDF file")
    parser.add_argument("--output", "-o", type=str, default="optimized_output.pdf",
                        help="Path for the optimized PDF (default: optimized_output.pdf)")

    # Parse arguments
    args = parser.parse_args()

    print(f"Optimizing PDF: {args.input_pdf}")
    success = optimize_pdf(args.input_pdf, args.output)
    if not success:
        print("PDF optimization failed.")
    else:
        print(f"Optimized PDF saved as: {args.output}")

if __name__ == "__main__":
    main()