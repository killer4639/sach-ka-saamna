# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from PIL import Image, ImageChops, ImageEnhance
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import io
from io import BytesIO
import requests
import os
import numpy as np
import base64
from keras.models import load_model
from keras.preprocessing import image
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from config import S3_BUCKET, S3_KEY, S3_SECRET, S3_REGION
from helpers import *
from segmentation import *
from keras.models import model_from_json
import slack
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
app.config["SECRET_KEY"] = "prettyprinted"
count = 1
# get the model from here. Works fine. No need to touch
def get_model():

    global model
    json_file = open("models/model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    # load weights into new model
    model.load_weights("models/model_weights.h5")
    print("Loaded model from disk")

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    print("Model compiled.")


# preprocessing function. Here is where everything starts
# converts to error level analysis picture
def convert_to_ela_image(path, quality):
    temp_filename = "temp_file_name.jpg"
    ela_filename = "temp_ela.png"

    # s3 se fetch image ko
    image = ""
    try:
        response = requests.get(path)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except:
        # if you want to locally import the image from path then comment above line
        # Uncomment the below line
        image = Image.open(path).convert("RGB")

    # saving local
    image.save(temp_filename, "JPEG", quality=quality)
    temp_image = Image.open(temp_filename)

    ela_image = ImageChops.difference(image, temp_image)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff

    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image


def prepare_image(image_path, image_size=(224, 224)):
    img = np.array(convert_to_ela_image(image_path, 90).resize(image_size))
    return img * 5


def preprocess_image(image_path, target_size):

    image = prepare_image(image_path, target_size)
    image = image.reshape(-1, 224, 224, 3)

    return image


def create_path():
    return "assets/temp" + count + ".png"


# loads the model on running
print("Loading Model...")
get_model()


# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("fromPredict"):
        session["fromPredict"] = False
    elif session.get("prediction"):
        session.pop("prediction")
        session.pop("confidence")
        if session.get("imageURL"):
            session.pop("imageURL")
        # if(os.path.exists(session.get('segmentImageURL'))):
        #     os.remove(session.get('segmentImageURL'))
        #     print("File Removed!")

    if not session.get("logged_in"):
        form = forms.LoginForm(request.form)
        if request.method == "POST":
            username = request.form["username"].lower()
            password = request.form["password"]
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session["logged_in"] = True
                    session["username"] = username
                    return json.dumps({"status": "Login successful"})
                return json.dumps({"status": "Invalid user/pass"})
            return json.dumps({"status": "Both fields required"})
        return render_template("login.html", form=form)
    user = helpers.get_user()
    return render_template("home.html", user=user)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


# ------------------hello----------------------------------#


@app.route("/hello", methods=["POST"])
def hello():
    form = forms.HelloForm(request.form)
    if request.method == "POST":
        name = request.form["name"]
        return json.dumps({"greeting": "Hello, " + name + "!"})


# -------- Signup ---------------------------------------------------------- #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if not session.get("logged_in"):
        form = forms.LoginForm(request.form)
        if request.method == "POST":
            username = request.form["username"].lower()
            password = helpers.hash_password(request.form["password"])
            email = request.form["email"]
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session["logged_in"] = True
                    session["username"] = username
                    return json.dumps({"status": "Signup successful"})
                return json.dumps({"status": "Username taken"})
            return json.dumps({"status": "User/Pass required"})
        return render_template("login.html", form=form)
    return redirect(url_for("login"))


# ----------------Predict------------------------------------------------------#
@app.route("/predict", methods=["POST"])
def predict():
    if session.get("logged_in"):
        if request.method == "POST":
            if "image" not in request.files:
                return "No image key in request.files"

            # A
            imageFile = request.files["image"]

            # B, upload to S3 and get the URL
            image = upload_file(imageFile)

            # C, prints the s3 path.
            print(image)

            # additionally if you don't want to use s3 then you can simply
            # supply the image path like below and comment the above lines A,B,C and
            # uncomment the below line to get the image path from local.
            # Supply the absolute path to this and make changes in convert_to_ela_image
            # function as given

            # image = '<PATH>'

            processed_image = preprocess_image(image, target_size=(224, 224))

            # preprocessing done here. Prediction stage
            prediction = model.predict(processed_image)
            y_pred_class = np.argmax(prediction, axis=1)[0]
            class_names = ["Real", "Fake"]
            new_path = "./static/assets/black.jpg"
            if class_names[y_pred_class] == "Fake":
                # segmented image prediction
                new_path = segment_image(image)

            print(
                f"Class: {class_names[y_pred_class]} Confidence: {np.amax(prediction) * 100:0.2f}"
            )
            # print(type(prediction), type(np.amax(prediction)))
            pred = {}
            session["prediction"] = class_names[y_pred_class]
            session["confidence"] = float(np.amax(prediction) * 100)
            session["fromPredict"] = True
            session["imageURL"] = image
            session["segmentImageURL"] = new_path
            return redirect(url_for("login"))
    return redirect(url_for("login"))


# -------- Settings ---------------------------------------------------------- #
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if session.get("logged_in"):
        if request.method == "POST":
            password = request.form["password"]
            if password != "":
                password = helpers.hash_password(password)
            email = request.form["email"]
            helpers.change_user(password=password, email=email)
            return json.dumps({"status": "Saved"})
        user = helpers.get_user()
        return render_template("settings.html", user=user)
    return redirect(url_for("login"))


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8080)
