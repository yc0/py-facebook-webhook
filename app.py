from sanic import Sanic
from argparse import ArgumentParser
from sanic import response
import requests
import os
import sys
import json

app = Sanic(__name__)


@app.route('/webhook', methods=['GET'])
def verify(request):
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return response.text("Verification token mismatch", status=403)
        return response.text(request.args["hub.challenge"][0])

    return response.text("Hello world")


@app.route('/webhook', methods=['POST'])
def webhook(request):
    # endpoint for processing incoming messaging events

    data = request.json
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data.get("entry"):
            if "messaging" in entry:
                for event in entry.get("messaging"):
                    #   print(event.get('sender'))
                    #   print(event.get('sender').get('id'))
                    #   sender_id = event.get('sender').get('id')
                    if event.get("message"):   # delivery confirmation
                        recipient_id = event.get('recipient').get('id')
                        sender_id = event.get('sender').get('id')
                        send_message(sender_id, "roger that!")

                    if event.get("delivery"):
                        pass

                    if event.get("optin"):     # optin confirmation
                        user_ref = event.get('optin').get("user_ref")
                        send_message(user_ref,
                                     "Good to see you",
                                     category="user_ref")
                    if event.get("postback"):   # user clicked/tapped "postback" button in earlier message
                        pass
    return response.text("ok")


def send_message(recipient_id,
                 message_text,
                 category="id",
                 message_type="UPDATE"):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            category: recipient_id
        },
        "message": {
            "text": message_text
        },
        "messaging_type": message_type
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    log(r.text)
    if r.status_code != 200:
        log(r.status_code)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


def main():
    if "VERIFY_TOKEN" in os.environ:
        print("your verify token is: ", os.environ["VERIFY_TOKEN"])

    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('--host', default='127.0.0.1', help='host')
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    arg_parser.add_argument('--cert', default=None, help='cert')
    arg_parser.add_argument('--key', default=None, help='key')
    args = arg_parser.parse_args()

    if not args.key:
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        app.run(host=args.host, port=args.port, debug=args.debug,
                ssl={'cert': args.cert, 'key': args.key})


if __name__ == "__main__":
    main()
