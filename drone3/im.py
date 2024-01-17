from PIL import Image

def resize_image(input_path, output_path, size):
    """
    Resize an image.

    Parameters:
    - input_path: The path to the input image.
    - output_path: The path to save the resized image.
    - size: A tuple representing the new size (width, height).

    Returns:
    - None
    """
    with Image.open(input_path) as img:
        resized_img = img.resize(size)
        resized_img.save(output_path)

# Example usage:
input_image_path = "1.png"
output_image_path = "1.png"
new_size = (30, 30)  # Specify the new size (width, height)

resize_image(input_image_path, output_image_path, new_size)
