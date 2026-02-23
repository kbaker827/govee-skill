---
name: govee
description: Control Govee smart home devices (lights, LED strips, plugs) via the Govee Developer API. Use when the user wants to turn lights on/off, change colors, adjust brightness, set scenes, or check device status for Govee products.
---

# Govee

Control Govee smart lights, LED strips, and other devices via the Govee Developer API.

## Quick Start

### API Key Setup

1. Download the Govee Home app
2. Go to **Profile → Settings → About → Apply for API Key**
3. Or visit: https://govee-home.com/user-manual/govee-developer-program
4. Copy your API key

Set environment variable (optional):
```bash
export GOVEE_API_KEY=your_api_key_here
```

### List Devices

```bash
python3 scripts/govee.py --api-key YOUR_KEY list
```

### Control a Light

```bash
# Turn on
python3 scripts/govee.py --api-key YOUR_KEY turn-on --device DEVICE_ID

# Turn off
python3 scripts/govee.py --api-key YOUR_KEY turn-off --device DEVICE_ID

# Set color (RGB)
python3 scripts/govee.py --api-key YOUR_KEY color --device DEVICE_ID --r 255 --g 0 --b 0

# Set brightness (0-100)
python3 scripts/govee.py --api-key YOUR_KEY brightness --device DEVICE_ID --value 75
```

## Common Commands

| Command | Description |
|---------|-------------|
| `list` | List all Govee devices |
| `turn-on` | Turn device on |
| `turn-off` | Turn device off |
| `color` | Set RGB color |
| `brightness` | Set brightness (0-100) |
| `color-temp` | Set color temperature (2000-9000K) |
| `status` | Get device status |

## Resources

### scripts/
- `govee.py` - CLI tool for controlling Govee devices

### references/
- `api-reference.md` - Govee Developer API documentation

## Examples

### List all devices
```bash
python3 scripts/govee.py --api-key YOUR_KEY list
```

### Turn on a light strip
```bash
python3 scripts/govee.py --api-key YOUR_KEY turn-on --device "H6199_1234"
```

### Set warm white
```bash
python3 scripts/govee.py --api-key YOUR_KEY color-temp --device "H6199_1234" --temp 3000
```

### Set purple color
```bash
python3 scripts/govee.py --api-key YOUR_KEY color --device "H6199_1234" --r 128 --g 0 --b 128
```
