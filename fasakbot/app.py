import json
import logging

from flask import Flask, request, Response, make_response
from slackclient import SlackClient

app = Flask(__name__)
SLACK_WEBHOOK_SECRET = 'xoxp-492626270997-493899120038-500326181943-5873c346a3c173fb61a3f21108c57b7a'
slack_client = SlackClient(SLACK_WEBHOOK_SECRET)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


@app.route('/')
def hello_world():
    return 'Fasak Bot: Hello World!'


@app.route("/message_options", methods=["POST"])
def message_options():
    form_json = json.loads(request.form["payload"])
    logging.info("Message Options: {}".format(form_json))
    menu_options = {
        "options": [
            {
                "text": "He is a topper",
                "value": "topper"
            },
            {
                "text": "He is a billionaire",
                "value": "billionaire"
            }
        ]
    }
    return Response(json.dumps(menu_options), mimetype='application/json')


@app.route("/message_actions", methods=["POST"])
def message_actions():
    form_json = json.loads(request.form["payload"])
    # verify_slack_token(form_json["token"])
    logging.info("Message Actions: {}".format(form_json))
    selection = form_json["actions"][0]["selected_options"][0]["value"]
    if selection == "topper":
        message_text = "Wrong Answer. Both are true :joy:"
    else:
        message_text = "Wrong Answer. Both are true :rolling_on_the_floor_laughing:"
    response = slack_client.api_call(
        "chat.update",
        channel=form_json["channel"]["id"],
        ts=form_json["message_ts"],
        text=message_text,
        attachments=[]
    )
    return make_response("", 200)


def init():
    attachments_json = [
        {
            "fallback": "Upgrade your Slack client to use messages like these.",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "menu_options_2319",
            "actions": [
                {
                    "name": "answer_list",
                    "text": "Select the correct answer",
                    "type": "select",
                    "data_source": "external"
                }
            ]
        }
    ]
    slack_client.api_call(
        "chat.postMessage",
        channel="#general",
        text="Which of the following about Manoj is true? :god:",
        attachments=attachments_json
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    slack_client.api_call("api.test")
    slack_client.api_call("auth.test")
    app.run()
