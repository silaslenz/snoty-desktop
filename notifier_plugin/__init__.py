import json

import notify2

notify2.init("Snoty", "qt")


def notification_callback(object, data, extra_input):
    socket, has_input = extra_input
    print(has_input)
    data = json.loads(data)
    print("sending", data)
    if not has_input:
        socket.transport.write(json.dumps(data).encode() + b"\n")
    else:
        import tkinter

        root = tkinter.Tk()
        root.geometry("300x100")
        tkinter.Label(root, text="Input ", height=1, width=7).grid(row=0)
        inpt = tkinter.Entry(root, width=35)
        inpt.grid(row=0, column=1)
        info = tkinter.Label(root, text="", height=1)
        info.grid(row=3, column=1)
        def inp():
            input = inpt.get()
            data["inputValue"] = input
            socket.transport.write(json.dumps(data).encode() + b"\n")
            root.destroy()

        get = tkinter.Button(root, text="Input", command=inp)
        get.grid(row=2, column=1)
        tkinter.mainloop()

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
            (socket, action["input"])
        )
    notification.show()
    return message["title"].encode()
