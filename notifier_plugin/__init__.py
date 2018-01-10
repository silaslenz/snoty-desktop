from gi.repository import Notify




def create_notification(body):
    Notify.init(body["title"])
    Notify.Notification.new(body["text"]).show()
    return body["title"].encode()
