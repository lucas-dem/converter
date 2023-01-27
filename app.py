from flask import Flask, render_template, request, Response, send_file
import imageio
from PIL import Image
import io

app = Flask(__name__)

@app.route('/api/jpgtopng', methods=['POST'])
def jpg_to_png():
    # Get the image file from the POST request
    image = request.files.get('image')

    # Check if an image was uploaded
    if not image:
        return "No image selected"
    
    # Check if the image is in JPG format
    if not image.filename.endswith('.jpg'):
        return "Invalid image format. Please select a JPG image."
    
    # Check if the image size is less than 5MB
    if image.content_length > 5000000:
        return "Image size too large. Please select an image less than 5MB."

    # Read the image file and convert it to a numpy array
    image_bytes = image.read()
    image = imageio.imread(image_bytes, format='jpg')

    # Save the image as a PNG file
    imageio.imwrite("converted_image.png", image, format='png')

    # Create a Response object with the PNG image
    response = Response(image, content_type='image/png')
    response.headers["Content-Disposition"] = "attachment; filename=image.png"
    return response

@app.route('/api/pngtojpg', methods=['POST'])
def png_to_jpg():
    # Get the PNG image from the POST request
    png_image = request.files.get('image')
    # Open the PNG image with PIL
    img = Image.open(png_image)
    # Convert the PNG image to JPG
    img = img.convert('RGB')
    # Create a file-like buffer to receive JPG data.
    buffer = io.BytesIO()
    # Save the JPG image to the buffer
    img.save(buffer, format='JPEG')
    # Get the value of the buffer
    jpg_image = buffer.getvalue()
    # Close the buffer
    buffer.close()
    # Create a response with the JPG image as an attachment
    response = send_file(io.BytesIO(jpg_image), attachment_filename='image.jpg', as_attachment=True)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/api/webptopng', methods=['POST'])
def webp_to_png():
    # Get the webp image from the POST request
    webp_image = request.files['webp_image']

    # Open the webp image
    with Image.open(webp_image) as img:
        # Convert the image to PNG format
        img = img.convert('RGB')

        # Create a BytesIO object to save the PNG image to
        png_image = io.BytesIO()
        img.save(png_image, 'PNG')

        # Set the file cursor to the beginning of the BytesIO object
        png_image.seek(0)

        # Return the PNG image as a downloadable attachment
        return send_file(png_image, attachment_filename='converted.png', as_attachment=True, mimetype='image/png')

@app.route("/api/bmptopng", methods=["POST"])
def bmp_to_png():
    # Get the BMP image from the request
    bmp_image = request.files["image"]

    # Open the BMP image and convert it to PNG
    with Image.open(bmp_image) as img:
        img = img.convert("RGB")
        png_image = io.BytesIO()
        img.save(png_image, "PNG")
        png_image.seek(0)

    # Return the PNG image as a downloadable attachment
    return send_file(png_image, mimetype="image/png", as_attachment=True, attachment_filename="converted.png")

@app.route('/api/pngtopdf', methods=['POST'])
def convert_png_to_pdf():
    # Get the PNG image from the request
    image = request.files['image']
    
    # Open the image and convert it to RGB mode
    img = Image.open(image)
    img = img.convert("RGB")
    
    # Convert the image to a PDF
    pdf_buffer = io.BytesIO()
    img.save(pdf_buffer, 'PDF', resolution=100.0)
    pdf_buffer.seek(0)
    response = Response(pdf_buffer.read(),content_type='application/pdf')
    response.headers["Content-Disposition"] = "attachment; filename=image.pdf"
    return response

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/jpgtopng", methods=["GET"])
def jpgtopng():
    return render_template("jpgtopng.html")

@app.route("/pngtojpg", methods=["GET"])
def pngtojpg():
    return render_template("pngtojpg.html")

@app.route("/webptopng", methods=["GET"])
def webptopng():
    return render_template("webptopng.html")

@app.route("/bmptopng", methods=["GET"])
def bmptopng():
    return render_template("bmptopng.html")

@app.route("/pngtopdf", methods=["GET"])
def pngtopdf():
    return render_template("pngtopdf.html")

if __name__ == "__main__":
    app.run(debug=True)
