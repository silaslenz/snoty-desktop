import notify2
import dbus
notifications = []


def notification_callback(object, data):
    print("callback")

def create_notification(body):
    notify2.init(body["title"])

    notification = notify2.Notification("text")
    notification.add_action(
        "action_click",
        "Reply to Message",
        notification_callback,
        None  # Arguments
    )
    notification.show()
    notifications.append(notification)
    return body["title"].encode()
