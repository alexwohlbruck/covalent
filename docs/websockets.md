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

## Server to web client events

All these events correspond to mutations in the Vuex store (💻) or are send to the board to perform an action (⚛️).

### ⚛️ `FACTORY_RESET`
Removes the config file and reset the board to its default state.

Payload:
```json
{}
```

### ⚛️💻 `GROUP_STATE_CHANGED`
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

### ⚛️💻 `UPDATE_SETTINGS`
Updates settings in the config file (config.json). Only the settings below are allowed to be updated.

Payload:
```json
{
  "brightness": 0.9,
  "nightMode": true,
  "minimumLightLevel": 0.2,
  "readingLightColorTemperature": 2700
}
```

### ⚛️💻 `GET_SETTINGS`
Returns the config file (config.json).
```json
{
  "deviceId": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "lampId": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "wifi": [
    {
      "ssid": "My network",
      "password": "password"
    }
  ],
  "brightness": 0.9,
  "nightMode": true,
  "minimumLightLevel": 0.2,
  "readingLight_colorTemperature": 2700
}
```



### 💻 `ADD_USER`
Updates or adds a user to the store

Payload:
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "googleId": "xxxxxxxxxxxxxxxxxxxxx",
  "name": "Alex Wohlbruck",
  "familyName": "Wohlbruck",
  "givenName": "Alex",
  "email": "alexwohlbruck@gmail.com",
  "picture": "https://lh3.googleusercontent.com/a-/AOh14GhYgUCf9yFuj-Xt6_X_cDz-5gSusrGde-lerdKqXxA=s96-c",
  "createdAt": "2022-03-08T01:50:46.226Z",
  "updatedAt": "2022-03-08T01:50:46.226Z",
  "__v": 0
}
```


### 💻 `REMOVE_USER`
Removes a user from the store

Payload:
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
}
```

### 💻 `ADD_LAMP`
Updates or adds a lamp to the store

Payload:
```json
{
  "state": {
    "color": "#ff0000",
    "touching": false
  },
  "deviceData": {
    "deviceId": "xxxxxxxxxxx"
  },
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "name": "My lamp",
  "createdAt": "2022-03-22T21:38:02.337Z",
  "updatedAt": "2022-03-22T21:38:02.337Z",
  "__v": 0,
  "userId": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "groupId": "xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

### 💻 `REMOVE_LAMP`
Removes a lamp from the store

Payload:
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
}
```