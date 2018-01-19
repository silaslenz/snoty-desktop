# Protocol

## [C→S] Notification Posted/Updated on Phone
```
{
    "type":"NotificationPosted",
    "id":"com.textra#4",
    "package":"com.textra",
    "isUpdate":true,
    "title":"Big Text",
    "text":"Notification Sub Text",
        "actions":[
        {
            "id":0,
            "label":"Als ungelesen markieren",
            "input":false
        },
        {
            "id":1,
            "label":"Antworten",
            "input":true
        }
        ],
    "clearable":true
}
```


| Parameter | Content | Description |
| ------------- |:-------------:| :-----|
| actions | [] | Possible actions on the notification (click actions and input actions) |
| clearable | true/false | Whether the notification can be removed on the phone |
| isUpdate | true/false | New notification or updated existing one
## [C→S] Notification Removed on Phone
```
{
      "type":"NotificationRemoved,
      "id":"com.textra#4"
}
```

## [S→C] Notification Operation triggered by PC
```
{
      "type":"NotificationOperation",
        "id":"com.textra#4",
        "operation":"action",
    "actionId":0,
    "inputValue":null
}
```
| Parameter | Content | Description |
| ------------- |:-------------:| :-----|
|operation|"action"/"close"|Either triggeres an action (defined by actionId) field based on the item in NotificationPosted or closes the notification (if possible)|
|inputValue|null/"some text"|Response text for the input in case the action contained a RemoteInput field|


## [S→C] Ignore all of a certain package
```
{
      "type":"IgnorePackage",
    "package":"com.textra"
}
```
| Parameter | Content | Description |
| ------------- |:-------------:| :-----|
|package|Any package name (FQD)|Stop sending notifications of a given package to server (package name as in NotificationPosted request)|
