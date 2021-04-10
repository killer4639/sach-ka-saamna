import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import requests
from io import BytesIO
from PIL import Image, ImageChops, ImageEnhance
from skimage.io import imread
import matplotlib.pyplot as plt
from app import *
import boto3
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_REGION

s3 = boto3.client("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"], "/slack/events", app
)
client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
# client.chat_postMessage(channel='#slack-bot1',text="Hello world!")
BOT_ID = client.api_call("auth.test")["user_id"]
checkLoop = False


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    # print(event)
    # print('###########################################################')
    channel_id = event.get("channel")
    user_id = event.get("user")
    if BOT_ID != user_id:
        # print(BOT_ID)
        # print(user_id)
        # print("################################")
        text = event.get("text")
        global checkLoop
        if text != "":
            client.chat_postMessage(
                channel=channel_id, text="Welcome To Sach Ka Saamna"
            )
            checkLoop = True
            return
        elif checkLoop:
            checkLoop = False
            client.chat_postMessage(
                channel=channel_id, text="We have received your image"
            )
            url = event.get("files")[0].get("url_private_download")
            token = os.environ["SLACK_TOKEN"]
            response = requests.get(url, headers={"Authorization": "Bearer %s" % token})
            image = Image.open(BytesIO(response.content)).convert("RGB")
            client.chat_postMessage(channel=channel_id, text="Image uploaded")
            print(type(image))
            file_name = "temp_filename.png"
            image.save("temp_filename.png")
            processed_image = preprocess_image(file_name, target_size=(224, 224))

            # preprocessing done here. Prediction stage
            prediction = model.predict(processed_image)
            y_pred_class = np.argmax(prediction, axis=1)[0]
            class_names = ["Real", "Fake"]
            new_path = "./static/assets/black.jpg"
            if class_names[y_pred_class] == "Fake":
                # segmented image prediction
                new_path = segment_image(file_name)

            client.chat_postMessage(channel=channel_id, text="Image Processed")
            print(
                f"Class: {class_names[y_pred_class]} Confidence: {np.amax(prediction) * 100:0.2f}"
            )
            # print(type(prediction), type(np.amax(prediction)))
            pred = {}
            # session["prediction"] = class_names[y_pred_class]
            # session["confidence"] = float(np.amax(prediction) * 100)
            # session["fromPredict"] = True
            # session["imageURL"] = image
            outputMessage = (
                class_names[y_pred_class]
                + " with confidence of "
                + str((np.amax(prediction) * 100))
                + " percent."
            )
            result = client.files_upload(
                channels=channel_id,
                initial_comment=outputMessage,
                file=new_path,
            )
            return


if __name__ == "__main__":
    app.run(debug=True)
