import json

import notify2
from PyQt5.QtWidgets import QDesktopWidget

notify2.init("Snoty", "qt")


def notification_callback(notification_object, data, extra_input):
    socket, has_input = extra_input
    print(has_input)
    data = json.loads(data)
    print("sending", data)
    if not has_input:
        socket.transport.write(json.dumps(data).encode() + b"\n")
    else:
        from PyQt5 import QtWidgets

        gui = QtWidgets.QWidget()

        widget = gui.geometry()
        screen = QDesktopWidget().screenGeometry()
        x = screen.width() - widget.width()
        y = screen.height() - widget.height()
        gui.move(x, y)
        text, ok = QtWidgets.QInputDialog.getText(gui, "Response",
                                                  """Type your reply.""")
        print(text, ok)
        data["inputValue"] = text
        socket.transport.write(json.dumps(data).encode() + b"\n")


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
        notification.add_action(
            json.dumps(response),
            action["label"],
            notification_callback,
            (socket, action["input"])
        )
    notification.show()
    return message["title"].encode()
