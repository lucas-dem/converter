from flask import Flask, render_template, request, Response, send_file, json, make_response
import imageio.v2 as imageio
from PIL import Image
import io
from reportlab.pdfgen import canvas
from io import BytesIO
import base64

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

    # Read the converted image and encode it in base64 format
    with open("converted_image.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
    # Return the decoded image in the response as JSON
    response = make_response(json.dumps({'image': encoded_string}))
    response.headers['Content-Disposition'] = 'attachment; filename=converted_image.png'
    return response


@app.route('/api/webptopng', methods=['POST'])
def webp_to_png():
    # Get the image file from the POST request
    image = request.files.get('image')

    # Check if an image was uploaded
    if not image:
        return "No image selected"
    
    # Check if the image is in WEBP format
    if not image.filename.endswith('.webp'):
        return "Invalid image format. Please select a WEBP image."
    
    # Check if the image size is less than 5MB
    if image.content_length > 5000000:
        return "Image size too large. Please select an image less than 5MB."

    # Read the image file and convert it to a numpy array
    image_bytes = image.read()
    image = imageio.imread(image_bytes, format='webp', pilmode='L')

    # Save the image as a PNG file
    imageio.imwrite("converted_image.png", image, format='png')

    # Read the converted image and encode it in base64 format
    with open("converted_image.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
    # Return the decoded image in the response as JSON
    response = make_response(json.dumps({'image': encoded_string}))
    response.headers['Content-Disposition'] = 'attachment; filename=converted_image.png'
    return response


@app.route('/api/bmptopng', methods=['POST'])
def bmp_to_png():
    # Get the image file from the POST request
    image = request.files.get('image')

    # Check if an image was uploaded
    if not image:
        return "No image selected"
    
    # Check if the image is in BMP format
    if not image.filename.endswith('.bmp'):
        return "Invalid image format. Please select a BMP image."
    
    # Check if the image size is less than 5MB
    if image.content_length > 5000000:
        return "Image size too large. Please select an image less than 5MB."

    # Read the image file and convert it to a numpy array
    image_bytes = image.read()
    image = imageio.imread(image_bytes, format='bmp')

    # Save the image as a PNG file
    imageio.imwrite("converted_image.png", image, format='png')

    # Read the converted image and encode it in base64 format
    with open("converted_image.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
    # Return the decoded image in the response as JSON
    response = make_response(json.dumps({'image': encoded_string}))
    response.headers['Content-Disposition'] = 'attachment; filename=converted_image.png'
    return response


@app.route('/api/pngtopdf', methods=['POST'])
def png_to_pdf():
    # Get the image file from the POST request
    image = request.files.get('image')

    # Check if an image was uploaded
    if not image:
        return "No image selected"
    
    # Check if the image is in PNG format
    if not image.filename.endswith('.png'):
        return "Invalid image format. Please select a PNG image."
    
    # Check if the image size is less than 5MB
    if image.content_length > 5000000:
        return "Image size too large. Please select an image less than 5MB."

    # Read the image file and convert it to a numpy array
    image_bytes = image.read()
    image = Image.open(BytesIO(image_bytes))

    # Save the image as a PDF file
    image_file = BytesIO()
    canvas_obj = canvas.Canvas(image_file)
    canvas_obj.drawInlineImage(image_bytes, 0, 0)
    canvas_obj.save()

    # Read the converted image and encode it in base64 format
    encoded_string = base64.b64encode(image_file.getvalue()).decode("utf-8")
        
    # Return the decoded image in the response as JSON
    response = make_response(json.dumps({'image': encoded_string}))
    response.headers['Content-Type'] = 'application/json'
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
