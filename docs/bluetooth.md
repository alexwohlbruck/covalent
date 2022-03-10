# Bluetooth Protocol

## RX Messages (web app to board)

### `REQUEST_NETWORKS`
Request a list of available Wifi networks from the board. A response is sent via `AVAILABLE_NETWORKS`. In addition, `DEVICE_DATA` is sent for convenience.

Payload:
```json
{}
```

### `CONNECT_NETWORK`
Connect to a Wifi network. Pass the SSID and password in the payload. If successfull, a response is sent via `CONNECTION_SUCCESS`. If unsuccessful, a response is sent via `CONNECTION_FAILURE`.

Payload:
```json
{
  "ssid": "My wifi",
  "password": "mypassword"
}
```

## TX Messages (board to web app)

### `DEVICE_DATA`
Sends info about the board.

Payload:
```json
{
  "deviceId": "abcd1234",
}
```

### `AVAILABLE_NETWORKS`
Sends a list of available Wifi networks.

Payload:
```json
{
  "networks": [
    {
      "ssid": "My wifi",
      "strength": 0.9
    },
    {
      "ssid": "My other wifi",
      "strength": 0.5
    }
  ]
}
```

### `CONNECTION_SUCCESS`
The board has successfully connected to Wifi.

Payload:
```json
{
  "ssid": "My wifi",
  "ip": "192.168.1.1",
  "strength": 0.9
}
```

### `CONNECTION_FAILURE`
The board failed to connect to Wifi.

Payload:
```json
{}
```