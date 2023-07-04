import os
import qrcode
import requests


def generate_qrcode(text, format_typ="png", filename="qrimage", fill_color="black", back_color="white", size=10):
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4
    )

    qr_code.add_data(text)
    qr_code.make(fit=True)
    img = qr_code.make_image(fill_color=fill_color, back_color=back_color)

    # Get the user's home directory and append the path to the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Save the image to the desktop with the specified filename and format
    img.save(os.path.join(desktop_path, f"{filename}.{format_typ}"))

    # Provide feedback to the user indicating where the QR code image was saved
    print(f"QR code saved to {desktop_path}/{filename}.{format_typ}")


while True:
    url_string = input("Please enter the URL for which you want to generate a QR code (or enter 'quit' to exit): ")

    # Check if the user entered 'quit' to exit the program
    if url_string.lower() == "quit":
        break

    # Handle exceptions for invalid URL input
    try:
        response = requests.head(url_string)
        if response.status_code >= 400:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException:
        print("Invalid URL inputted. Please enter a valid URL.")
        continue

    # Prompt user for size input and handle exceptions
    while True:
        try:
            size_input = input("Please enter the size of the QR code (default is 10): ")
            if size_input != "":
                try:
                    size = int(size_input)
                except ValueError:
                    print("Invalid input for size, using default value of 10")
                    size = 10
            else:
                size = 10
            break
        except ValueError:
            print("Invalid size input. Please enter a valid integer.")

    file_format = input("Please enter the image format (png, jpeg, bmp, etc.): ")
    file_name = input("Please enter the file name (without extension): ")
    fill_color = input("Please enter the QR code fill color (default is black): ")
    back_color = input("Please enter the QR code background color (default is white): ")

    # Generate the QR code with the specified format, filename, and color specifications
    try:
        generate_qrcode(url_string, format_typ=file_format, filename=file_name, fill_color=fill_color,
                        back_color=back_color, size=size)
    except Exception as e:
        print(f"Error generating QR code: {e}")

    print()  

