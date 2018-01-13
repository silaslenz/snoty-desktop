import notify2

notify2.init("Snoty", 'qt')


def notification_callback(object, data):
    print("callback")


def create_notification(body):
    notification = notify2.Notification(body["title"], body["text"])
    notification.add_action(
        "action_click",
        "Reply to Message",
        notification_callback,
        None  # Arguments
    )
    notification.show()
    return body["title"].encode()
