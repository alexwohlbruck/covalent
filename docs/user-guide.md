# User guide

## Table of contents
- [User guide](#user-guide)
  - [Table of contents](#table-of-contents)
  - [LED indicator colors](#led-indicator-colors)
  - [Signing in](#signing-in)
  - [Pairing a lamp](#pairing-a-lamp)
  - [Sending messages](#sending-messages)
    - [From the lamp](#from-the-lamp)
    - [From the app](#from-the-app)
  - [Adjusting lamp settings](#adjusting-lamp-settings)
  - [Removing or factory resetting your lamp](#removing-or-factory-resetting-your-lamp)
    - [From the app](#from-the-app-1)
    - [From the lamp](#from-the-lamp-1)
  - [Signing out](#signing-out)

## LED indicator colors
|                                                        | Color                  | Lamp mode              |
|--------------------------------------------------------|------------------------|------------------------|
| <img src="indicators/dot-blue-pulse.svg" width='12'>   | Blue pulsing           | Bluetooth pairing mode |
| <img src="indicators/dot-blue.svg" width='12'>         | Blue solid             | Bluetooth connected    |
| <img src="indicators/dot-amber-pulse.svg" width='12'>  | Amber pulsing          | Connecting to wifi     |
| <img src="indicators/dot-amber.svg" width='12'>        | Amber solid            | Connected to wifi      |
| <img src="indicators/dot-green-pulse.svg" width='12'>  | Green pulsing          | Connecting to server   |
| <img src="indicators/dot-green.svg" width='12'>        | Green solid            | Successfully set up    |
| <img src="indicators/dot-red.svg" width='12'>          | Red solid              | Error                  |
| <img src="indicators/dot-white-pulse.svg" width='12'>  | White pulsing          | Factory resetting      |



## Signing in
Visit https://project-covalent.herokuapp.com and sign in with your Google account. You will be redirected to the home page where you see your lamp or pair a new one.

## Pairing a lamp
The app uses Bluetooth to pair to your lamp and configure it. This is not supported on iOS devices, or in the Safari browser. Compatible browsers are Chrome, Opera, Edge, and Samsung Internet. For more info about compatibility, visit <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API#browser_compatibility" target="_blank">this page</a>.

1. Ensure your lamp is is plugged in and in pairing mode. Paring mode is indicated by a pulsing blue light. If the lamps has already been set up, follow the [factory reset instructions](#removing-or-factory-resetting-your-lamp) below.
2. On the lamps page, click `+ ADD LAMP` to begin the pairing process.
3. Turn on bluetooth on your device and click `PAIR WITH BLUETOOTH`. A prompt will appear with the lamp name shown. Select it and click `Pair`.
4. Wait for the wifi network list to load, and select the network you wish to connect to. Enter the pasword if it is secured, and click `Connect`.
5. After the lamp is connected, give your lamp a name and add it to a group. You can either create a new group or add it to an existing one.
    a. Create a new group
    -  Enter a unique group ID and click `CONTINUE`.
    
    b. Add the lamp to an existing group
    - Select `Add to existing group`.
    - Enter the group ID and access code, then click `CONTINUE`.
6. The lamp will begin handshaking with the server, after a few seconds it will be available to use.

## Sending messages
You can send a message or "pulse" to your group from the lamp itself or from the app. Each lamp that is paried to the group will light the same color that you choose when you send the message.

### From the lamp
1. Rotate the top lid to select a color from the color wheel.
2. When you have found the color you want, push the top lid and hold for as long as you like to send the pulse.

### From the app
1. In the lamps list, find the lamp you want to control, and drag the white thumb along the color slider.
2. When you have found the color you want, click `SEND PULSE` and hold for as long as you like to send the pulse.

## Adjusting lamp settings
1. Tap the cog icon on a lamp to open it's settings.
2. You can rename the lamp, and adjust any of the settings on the screen. After adjusting, the changes will be saved automatically.

## Removing or factory resetting your lamp
If you wish to reset your lamp its original settings and remove it from your account, follow these steps. This will wipe all of your settings and will require you to pair the lamp again.
### From the app
1. Tap the cog icon on a lamp to open it's settings.
2. Click `DELETE LAMP`.
3. The lamp will be removed from your account and it will be factory reset if it is connected to the internet. After resetting, it will reboot into pairing mode.

### From the lamp
1. Double press the top button and on the second press, hold for at least 10 seconds.
2. Release the button, the lamp will reset itself and reboot into pairing mode. This will not remove the lamp from your account. If you wish to remove the lamp from your account, follow the steps in "From the app".

## Signing out
1. Tap your profile photo in the top right corner of the app.
2. Click `SIGN OUT`.