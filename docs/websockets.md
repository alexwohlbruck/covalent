# Websockets Protocol

## Client to server events

### `SEND_LAMP_COMMAND`
Update a lamp's state. This does the same as `PATCH /lamps/:id/state` but is duplicated on the websocket server so the board can send this event with only one open connection.

Payload:
```json
{
  "lampId": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "color": "#ff00ff",
  "touching": true
}
```


## Server to client events

All these events correspond to mutations in the Vuex store.

### `GROUP_STATE_CHANGED`
Fired when a user in your group starts or stops touching their lamp. 
Returns a new group state with the computed colors and active flag.

Payload:
```json
{
  "groupId": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "state": {
    "colors": ["#ff00ff", "#00ff00", "#0000fff"],
    "active": true
  }
```



### `ADD_USER`

### `REMOVE_USER`

### `ADD_LAMP`

### `REMOVE_LAMP`

### `ADD_GROUP`

### `REMOVE_GROUP`