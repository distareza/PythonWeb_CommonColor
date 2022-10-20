from flask import Flask, render_template, request, send_file, jsonify, make_response
import io
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/tmp/upload"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/")
def home():
    return render_template("index.html")

img_obj = None
img_arr = None

@app.route("/upload", methods=["POST"])
def upload():
    print("upload started")
    uploadedfile = request.files["upload-file"]
    print(f"Uploaded file : {uploadedfile}" )

    # https://blog.furas.pl/python-how-to-display-image-without-saving-in-file-using-bytesio-and-base64-string-in-url-gb.html#:~:text=To%20display%20image%20in%20web,it%20without%20saving%20on%20disk.&text=And%20later%20you%20can%20use,read()%20or%20img.
    # read to pillow
    global img_obj, img_arr
    image = Image.open(uploadedfile)

    # draw something
    draw = ImageDraw.Draw(image) # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
    #draw.rectangle([(20,20), (280,280)], outline=(255,0,0), width=3)  # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.rectangle
    #draw.text((15,5), "Hello World!")                                 # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.text

    # convert to file-like data
    img_obj = io.BytesIO()             # file in memory to save image without using disk  #
    image.save(img_obj, format='png')  # save in file (BytesIO)                           # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save
    img_obj.seek(0)                    # move to beginning of file (BytesIO) to read it   #

    # convert to tensor ( n-dimensional array )
    img_arr = np.array(image)
    print(f"array dimension {img_arr.ndim}")
    print(f"array shape {img_arr.shape}")

    return "OK", 200

@app.route("/showimage")
def showImage():
    if img_obj is None:
        return

    return send_file(img_obj, "file.png")

@app.route("/showdetailinfo", methods=["POST"])
def showDetail():
    if img_arr is None:
        return

    # Group pixel color
    colour_arr = []
    for y in range(img_arr.shape[1]):
        colour_arr.extend([ img_arr[x,y,:] for x in range(img_arr.shape[0])])
    arr = [ str(x[0]) + '-' + str(x[1]) + '-' + str(x[2]) for x in colour_arr ]
    df = pd.Series(arr).to_frame().rename(columns={0: "Colours"})
    print(f"colour count : {df.count()}")
    colour_group = df.value_counts().head(5)
    colour_count = int(df.count())
    group_color = []
    for idx, group in enumerate(colour_group.index.tolist()):
        group_color.append( [str(group[0]), int(colour_group[idx]), float(colour_group[idx] * 100 / colour_count )] )

    json = jsonify(
         color_count= colour_count,
         group_color= group_color,
         )
    return json, 200

@app.route("/color/<rgb_param>", methods=['GET'])
def drawColorPallet(rgb_param:str):
    print(f"drawColorPallete {rgb_param}")
    rgb = (int(rgb_param.split("-")[0]), int(rgb_param.split("-")[1]), int(rgb_param.split("-")[2]))
    image = Image.new('RGB', (2,1), rgb)
    draw = ImageDraw.Draw(image)                                      # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
    # convert to file-like object
    image_obj = io.BytesIO()             # file in memory to save image without using disk  #
    image.save(image_obj, format='png')  # save in file (BytesIO)                           # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save
    image_obj.seek(0)                    # move to beginning of file (BytesIO) to read it   #
    return send_file(image_obj, f"{str(rgb[0])}-{str(rgb[1])}-{str(rgb[2])}.png")


if __name__ == "__main__":
   app.run()
