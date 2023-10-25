# qpsalt-ble-decoder
Some information about the ble protocol of the QP Salt Bright Duo/Pro salt chlorinator. Also implementation in esphome.

## Motivation
The Salt Bright Duo can be configured locally over BLE via a smartphone app called ePool connect, which also displays some sensor readings like pH, ORP, salt concentration or water temperature. 
Unfortunately, there is no way to read these measurements from a web interface or even cloud service for use in eg. home automation or for logging. The suggested "connectivity addon" turns out to not connect via Bluetooth to the unit, but instead uses its own temperature sensor and can only switch the power to the unit via a relay.

## The communication
### Pairing to the device
To receive data, the device has to be paired/bonded to whatever BLE client one uses. This is done via `menu`, `arrow up/down` until "CO(mmunication)" is displayed. Select with `OK`. Scroll down and select "Bt". Enter pairing mode by selecting "pa". If Bluetooth is turned off, turn it on with "mo".
### Receiving data
The device does not simply publish each datapoint on its own characteristic uuid, but publishes everything on a single uuid in packets of bytes containing several datapoints/registers at once.
- Service UUID: `1081`
- Characteristic UUID: `ef785c24-22bb-463d-b651-0b7445ba091c`
### Packet structure
These packets use an encoding which looks a little bit like _ASN.1_: \
Every packet starts with a nullbyte `0x00`, followed by one byte describing the length of the entire packet in bytes. The third Byte seems to be mostly `0x01`, in one case being `0x02`. The fourth byte identifies the data register being transmitted, followed by one byte denoting the length of the following data. Lastly, the data follows. When multiple registers get sent, the order `register, length, data` is simply repeated.
For example, lets look at the following Packet: `(0x) 00 09 01 0C 01 6D B0 01 36`

| 00 | 09 | 01 | 0C | 01 | 6D | B0 | 01 | 36 |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Startbyte | Length of entire packet: `0x09` Bytes | Either `0x01` or `0x02`  | Data for register `0x0C` follows | Length of data is `0x01` Bytes | Register `0x0C` has the value `0x6D = 109` | Data for register `0xB0` follows | Length of data is `0x01` Bytes | Register `0xB0` has the value `0x36 = 54` |

This is an (incomplete) list of the registers and their apparent purpose:
<details>
  <summary> Table </summary>
  
| Register | Length | Description             | Notes                               |
|----------|--------|-------------------------|-------------------------------------|
| `01`     | 1      | pH * 10, resolution 1   |                                     |
| `02`     | 2      | pH * 100, resolution 10 |                                     |
| `03`     | 1      | ?                       |                                     |
| `06`     | 2      | ORP in mV               |                                     |
| `08`     | 1      | ?                       |                                     |
| `09`     | 2      | water temperature * 10  |                                     |
| `0A`     | 1      | ?                       |                                     |
| `0B`     | 1      | ?                       | some sort of measurement            |
| `0C`     | 1      | ?                       | some sort of measurement            |
| `0E`     | 2      | ?                       |                                     |
| `0F`     | 2      | ?                       |                                     |
| `10`     | 2      | ?                       |                                     |
| `11`     | 2      | ?                       |                                     |
| `12`     | 4      | ?                       |                                     |
| `13`     | 4      | ?                       |                                     |
| `30`     | 1      | pH setpoint * 10        |                                     |
| `31`     | 1      | ?                       |                                     |
| `32`     | 1      | ?                       |                                     |
| `33`     | 1      | ?                       |                                     |
| `35`     | 1      | ORP setpoint in mV / 10 |                                     |
| `37`     | 1      | ?                       |                                     |
| `39`     | 1      | ?                       |                                     |
| `50`     | 1      | ?                       |                                     |
| `51`     | 1      | ?                       |                                     |
| `5F`     | 1      | ?                       |                                     |
| `67`     | 2      | ?                       |                                     |
| `69`     | 4      | ?                       |                                     |
| `6A`     | 1      | ?                       |                                     |
| `8F`     | 1      | ?                       |                                     |
| `90`     | 8      | ?                       |                                     |
| `91`     | 8      | ?                       |                                     |
| `92`     | 1      | ?                       |                                     |
| `93`     | 2      | ?                       |                                     |
| `94`     | 2      | ?                       |                                     |
| `95`     | 4      | ?                       |                                     |
| `96`     | 2      | ?                       |                                     |
| `97`     | 2      | ?                       |                                     |
| `99`     | 22     | Device Name ascii       |                                     |
| `9A`     | 16     | Serial Number ascii     |                                     |
| `9B`     | 2      | ?                       |                                     |
| `9C`     | 2      | ?                       |                                     |
| `9D`     | 8      | ?                       |                                     |
| `A3`     | 8      | ?                       |                                     |
| `B0`     | 1      | ?                       | some sort of measurement            |
| `B1`     | 6      | MAC address             |                                     |
| `D1`     | 1      | ?                       |                                     |
| `E1`     | 15     | ?                       | this has `0x02` as third packetbyte |
| `E2`     | 15     | ?                       |                                     |
| `FE`     | 1      | ?                       |                                     |
</details>
