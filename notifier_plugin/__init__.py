import json

import notify2

notify2.init("Snoty", "qt")


def notification_callback(object, data, socket):
    print("callback", object, data)
    print(data)
    socket.transport.write(data.encode())
    print("sentstuff")


def create_notification(body, socket):
    notification = notify2.Notification(body["title"], body["text"])
    for action in body["actions"]:
        response = {
                "header": {
                    "type": "NotificationOperation",
                    "version": "1"
                },
                "body": {
                    "id": "com.textra#4",
                    "operation": "action",
                    "actionId": action["id"],
                    "inputValue": None}}
        notification.add_action(
            json.dumps(response),
        action["label"],
        notification_callback,
        socket
        )
        notification.show()
        return body["title"].encode()
