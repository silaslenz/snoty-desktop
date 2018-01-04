from gi.repository import Notify

Notify.init("Snoty")


def create_notification(text):
    Notify.Notification.new(text).show()
