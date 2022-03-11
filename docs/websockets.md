# Websockets Protocol

## Client to server events

### `SEND_LAMP_COMMAND`
Update a lamp's state. This does the same as `PATCH /lamps/:id/state` but is duplicated on the websocket server so the board can send this event with only one open connection.

Payload:
```json
{
  "color": "#ff00ff",
  "touching": true
}
```


## Server to client events

All these events correspond to mutations in the Vuex store.

### `LAMP_STATE_CHANGED`
Fired when a user in your group starts or stops touching their lamp. 
Returns a list of lamps that are active and their states. Not all lamp data is published, only `_id`, `state`, and `userId`, which is the owner of the lamp.

Payload:
```json
{
  "lamps": [
    {
      "_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
      "state": {
        "touching": true,
        "color": "#ff0000"
      },
      "userId": "xxxxxxxxxxxxxxxxxxxxxxxx"
    },
    {
      "_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
      "state": {
        "touching": true,
        "color": "#ff0000"
      },
      "userId": "xxxxxxxxxxxxxxxxxxxxxxxx"
    }
  ]
}
```



### `ADD_USER`

### `REMOVE_USER`

### `ADD_LAMP`

### `REMOVE_LAMP`

### `ADD_GROUP`

### `REMOVE_GROUP`