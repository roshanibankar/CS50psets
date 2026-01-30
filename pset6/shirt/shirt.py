import sys
import os
from PIL import Image, ImageOps

def main():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    valid_extensions = [".jpg", ".jpeg", ".png"]
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()

    if input_ext not in valid_extensions:
        sys.exit("Invalid input")
    if output_ext not in valid_extensions:
        sys.exit("Invalid output")
    if input_ext != output_ext:
        sys.exit("Input and output have different extensions")

    if not os.path.exists(input_path):
        sys.exit("Input does not exist")

    try:
       
        shirt = Image.open("shirt.png")
        photo = Image.open(input_path)
        size = shirt.size
        photo = ImageOps.fit(photo, size)
        photo.paste(shirt, shirt)
        photo.save(output_path)

    except Exception as e:
        sys.exit(f"Error processing image: {e}")


if __name__ == "__main__":
    main()
