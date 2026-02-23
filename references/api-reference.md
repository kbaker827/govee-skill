# Govee Developer API Reference

## Base URL

```
https://developer-api.govee.com/v1
```

## Authentication

All requests require the `Govee-API-Key` header:

```
Govee-API-Key: your_api_key_here
```

Get your API key from the Govee app: Profile → Settings → About → Apply for API Key

## Rate Limits

- 10,000 requests per day per API key
- 100 requests per minute per API key

## Endpoints

### List Devices

```
GET /devices
```

Returns all devices associated with your API key.

**Response:**
```json
{
  "data": {
    "devices": [
      {
        "device": "H6199_1234",
        "model": "H6199",
        "deviceName": "Living Room Strip",
        "controllable": true,
        "retrievable": true,
        "supportCmds": ["turn", "brightness", "color", "colorTem"],
        "properties": {
          "colorTem": {
            "range": [2000, 9000]
          }
        }
      }
    ]
  },
  "message": "Success",
  "code": 200
}
```

### Get Device State

```
GET /devices/state?device={device}&model={model}
```

**Parameters:**
- `device` (required): Device ID (e.g., "H6199_1234")
- `model` (required): Device model (e.g., "H6199")

**Response:**
```json
{
  "data": {
    "device": "H6199_1234",
    "model": "H6199",
    "properties": [
      {"online": true},
      {"powerState": "on"},
      {"brightness": 80},
      {"color": {"r": 255, "g": 0, "b": 0}}
    ]
  },
  "message": "Success",
  "code": 200
}
```

### Control Device

```
PUT /devices/control
```

**Request Body:**
```json
{
  "device": "H6199_1234",
  "model": "H6199",
  "cmd": {
    "name": "turn",
    "value": "on"
  }
}
```

**Commands:**

| Command | Value Type | Description |
|---------|-----------|-------------|
| `turn` | `"on"` or `"off"` | Power control |
| `brightness` | Integer (0-100) | Brightness level |
| `color` | Object `{r, g, b}` | RGB color (0-255 each) |
| `colorTem` | Integer (2000-9000) | Color temperature in Kelvin |

**Turn On/Off:**
```json
{
  "cmd": {
    "name": "turn",
    "value": "on"
  }
}
```

**Set Brightness:**
```json
{
  "cmd": {
    "name": "brightness",
    "value": 75
  }
}
```

**Set Color:**
```json
{
  "cmd": {
    "name": "color",
    "value": {"r": 255, "g": 0, "b": 128}
  }
}
```

**Set Color Temperature:**
```json
{
  "cmd": {
    "name": "colorTem",
    "value": 3000
  }
}
```

## Common Device Models

| Model | Type |
|-------|------|
| H6199 | LED Strip Light |
| H6008 | RGBWW Bulb |
| H6076 | Floor Lamp |
| H6061 | Glide Wall Light |
| H6056 | Table Lamp |
| H5081 | Smart Plug |

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized (invalid API key) |
| 429 | Rate Limited |
| 500 | Server Error |

## Official Documentation

https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf
