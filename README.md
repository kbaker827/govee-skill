# Govee Skill for OpenClaw

Control Govee smart lights, LED strips, and other devices via the Govee Developer API.

## What is OpenClaw?

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source agent framework. This skill extends OpenClaw with Govee smart home integration.

## Setup

### 1. Get Your API Key

1. Download the Govee Home app
2. Go to **Profile → Settings → About → Apply for API Key**
3. Or visit: https://govee-home.com/user-manual/govee-developer-program
4. Copy your API key

### 2. Use the Skill

```bash
# List all devices
python3 scripts/govee.py --api-key YOUR_KEY list

# Turn on a light
python3 scripts/govee.py --api-key YOUR_KEY turn-on --device "H6199_1234"

# Set color to red
python3 scripts/govee.py --api-key YOUR_KEY color --device "H6199_1234" --r 255 --g 0 --b 0

# Set brightness to 75%
python3 scripts/govee.py --api-key YOUR_KEY brightness --device "H6199_1234" --value 75

# Set warm white (3000K)
python3 scripts/govee.py --api-key YOUR_KEY color-temp --device "H6199_1234" --temp 3000
```

### Environment Variable

Set `GOVEE_API_KEY` to skip the `--api-key` flag:

```bash
export GOVEE_API_KEY=your_api_key
python3 scripts/govee.py list
```

## Features

- List all Govee devices
- Turn devices on/off
- Set RGB colors
- Adjust brightness (0-100%)
- Set color temperature (2000-9000K)
- Check device status

## API Reference

See [`references/api-reference.md`](references/api-reference.md) for complete Govee Developer API documentation.

## Supported Devices

- LED Strip Lights (H6199, etc.)
- RGBWW Bulbs (H6008, etc.)
- Floor Lamps (H6076, etc.)
- Table Lamps (H6056, etc.)
- Smart Plugs (H5081, etc.)

## License

MIT
