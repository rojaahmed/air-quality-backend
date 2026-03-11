import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

firebase_key = json.loads(os.environ["FIREBASE_KEY"])

cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)

def send_notification(token, title, body):

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )

    response = messaging.send(message)
    return response