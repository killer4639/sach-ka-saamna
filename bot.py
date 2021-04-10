import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import requests
from io import BytesIO
from PIL import Image, ImageChops, ImageEnhance

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"], "/slack/events", app
)
client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
# client.chat_postMessage(channel='#slack-bot1',text="Hello world!")
BOT_ID = client.api_call("auth.test")["user_id"]


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    # print(event)
    # print('###########################################################')
    channel_id = event.get("channel")
    user_id = event.get("user")
    if BOT_ID != user_id:
        text = event.get("text")
        if text != "":
            client.chat_postMessage(channel=channel_id, text=text)
        else:
            url = event.get("files")[0].get("url_private_download")
            token = os.environ["SLACK_TOKEN"]
            response = requests.get(url, headers={"Authorization": "Bearer %s" % token})
            image = Image.open(BytesIO(response.content)).convert("RGB")

            # if you want to locally import the image from path then comment above line
            # Uncomment the below line
            # img = Image.open(path).convert('RGB')

            # saving local
            image.save("temp_filename.jpg")
            client.chat_postMessage(
                {
                    "channel": channel_id,
                    "attachments": [
                        {
                            "accessory": {
                                "type": "image",
                                "image_url": url,
                                "alt_text": "Haunted hotel image",
                            }
                        }
                    ],
                }
            )
            print(url)
    # if BOT_ID!=user_id:
    #     text=event.get('text')
    #     client.chat_postMessage(channel=channel_id,text=text)


if __name__ == "__main__":
    app.run(debug=True)
