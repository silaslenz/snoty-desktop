import json

import notify2

notify2.init("Snoty", "qt")


def notification_callback(object, data, socket):
    print("sending", data)
    socket.transport.write(data.encode() + b"\n")


def create_notification(message, socket):
    notification = notify2.Notification(message["title"], message["text"])
    for action in message["actions"]:
        response = {
            "type": "NotificationOperation",
            "id": message["id"],
            "operation": "action",
            "actionId": action["id"],
            "inputValue": None
        }
        if action["input"] == True:
            response["inputValue"] = "cat"
        notification.add_action(
            json.dumps(response),
            action["label"],
            notification_callback,
            socket
        )
    notification.show()
    return message["title"].encode()
