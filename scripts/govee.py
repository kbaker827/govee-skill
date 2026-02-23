#!/usr/bin/env python3
"""
Govee CLI - Control Govee smart devices via the Developer API.

Usage:
    python3 govee.py --api-key YOUR_KEY list
    python3 govee.py --api-key YOUR_KEY turn-on --device DEVICE_ID
    python3 govee.py --api-key YOUR_KEY color --device DEVICE_ID --r 255 --g 0 --b 0
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Optional

API_BASE = "https://developer-api.govee.com/v1"


def api_request(endpoint: str, api_key: str, method: str = "GET", data: dict = None) -> dict:
    """Make an API request to Govee."""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "Govee-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        if data:
            req = urllib.request.Request(
                url, 
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method=method
            )
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
        if error_body:
            print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_devices(api_key: str):
    """List all Govee devices."""
    data = api_request("/devices", api_key)
    devices = data.get("data", {}).get("devices", [])
    
    if not devices:
        print("No devices found.")
        return
    
    print(f"Found {len(devices)} device(s):\n")
    for device in devices:
        print(f"Device: {device.get('deviceName', 'Unknown')}")
        print(f"  Model: {device.get('model', 'Unknown')}")
        print(f"  ID: {device.get('device', 'Unknown')}")
        print(f"  MAC: {device.get('mac', 'Unknown')}")
        controllable = device.get('controllable', False)
        retrievable = device.get('retrievable', False)
        print(f"  Controllable: {controllable}")
        print(f"  Status Retrievable: {retrievable}")
        
        # Show supported commands
        support_cmd = device.get('supportCmds', [])
        if support_cmd:
            print(f"  Supported Commands: {', '.join(support_cmd)}")
        print()


def get_device_status(api_key: str, device_id: str, model: str):
    """Get device status."""
    # Note: Govee API requires both device and model
    # User needs to provide model or we look it up
    endpoint = f"/devices/state?device={device_id}&model={model}"
    data = api_request(endpoint, api_key)
    
    properties = data.get("data", {}).get("properties", [])
    print(f"Device Status ({device_id}):")
    for prop in properties:
        for key, value in prop.items():
            print(f"  {key}: {value}")


def turn_on(api_key: str, device_id: str, model: str):
    """Turn device on."""
    payload = {
        "device": device_id,
        "model": model,
        "cmd": {
            "name": "turn",
            "value": "on"
        }
    }
    api_request("/devices/control", api_key, method="PUT", data=payload)
    print(f"Turned on {device_id}")


def turn_off(api_key: str, device_id: str, model: str):
    """Turn device off."""
    payload = {
        "device": device_id,
        "model": model,
        "cmd": {
            "name": "turn",
            "value": "off"
        }
    }
    api_request("/devices/control", api_key, method="PUT", data=payload)
    print(f"Turned off {device_id}")


def set_color(api_key: str, device_id: str, model: str, r: int, g: int, b: int):
    """Set RGB color."""
    payload = {
        "device": device_id,
        "model": model,
        "cmd": {
            "name": "color",
            "value": {
                "r": r,
                "g": g,
                "b": b
            }
        }
    }
    api_request("/devices/control", api_key, method="PUT", data=payload)
    print(f"Set color to RGB({r}, {g}, {b}) for {device_id}")


def set_brightness(api_key: str, device_id: str, model: str, value: int):
    """Set brightness (0-100)."""
    payload = {
        "device": device_id,
        "model": model,
        "cmd": {
            "name": "brightness",
            "value": value
        }
    }
    api_request("/devices/control", api_key, method="PUT", data=payload)
    print(f"Set brightness to {value}% for {device_id}")


def set_color_temp(api_key: str, device_id: str, model: str, temp: int):
    """Set color temperature (2000-9000K)."""
    payload = {
        "device": device_id,
        "model": model,
        "cmd": {
            "name": "colorTem",
            "value": temp
        }
    }
    api_request("/devices/control", api_key, method="PUT", data=payload)
    print(f"Set color temperature to {temp}K for {device_id}")


def find_device_model(api_key: str, device_id: str) -> Optional[str]:
    """Find model for a device ID."""
    data = api_request("/devices", api_key)
    devices = data.get("data", {}).get("devices", [])
    
    for device in devices:
        if device.get("device") == device_id:
            return device.get("model")
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Control Govee devices')
    parser.add_argument('--api-key', '-k', help='Govee API key (or set GOVEE_API_KEY env var)')
    parser.add_argument('--model', '-m', help='Device model (auto-detected if not provided)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # list command
    subparsers.add_parser('list', help='List all devices')
    
    # status command
    status_parser = subparsers.add_parser('status', help='Get device status')
    status_parser.add_argument('--device', '-d', required=True, help='Device ID')
    
    # turn-on command
    on_parser = subparsers.add_parser('turn-on', help='Turn device on')
    on_parser.add_argument('--device', '-d', required=True, help='Device ID')
    
    # turn-off command
    off_parser = subparsers.add_parser('turn-off', help='Turn device off')
    off_parser.add_argument('--device', '-d', required=True, help='Device ID')
    
    # color command
    color_parser = subparsers.add_parser('color', help='Set RGB color')
    color_parser.add_argument('--device', '-d', required=True, help='Device ID')
    color_parser.add_argument('--r', type=int, required=True, help='Red (0-255)')
    color_parser.add_argument('--g', type=int, required=True, help='Green (0-255)')
    color_parser.add_argument('--b', type=int, required=True, help='Blue (0-255)')
    
    # brightness command
    bright_parser = subparsers.add_parser('brightness', help='Set brightness')
    bright_parser.add_argument('--device', '-d', required=True, help='Device ID')
    bright_parser.add_argument('--value', '-v', type=int, required=True, help='Brightness (0-100)')
    
    # color-temp command
    temp_parser = subparsers.add_parser('color-temp', help='Set color temperature')
    temp_parser.add_argument('--device', '-d', required=True, help='Device ID')
    temp_parser.add_argument('--temp', '-t', type=int, required=True, help='Temperature in Kelvin (2000-9000)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Get API key
    api_key = args.api_key or os.environ.get('GOVEE_API_KEY')
    if not api_key:
        print("Error: API key required.", file=sys.stderr)
        print("Usage: --api-key YOUR_KEY or set GOVEE_API_KEY environment variable", file=sys.stderr)
        print("\nGet your API key from the Govee app: Profile → Settings → About → Apply for API Key", file=sys.stderr)
        sys.exit(1)
    
    # Handle list command (no device needed)
    if args.command == 'list':
        list_devices(api_key)
        return
    
    # For other commands, we need to determine the model
    device_id = args.device
    model = args.model
    
    if not model:
        print(f"Auto-detecting model for {device_id}...")
        model = find_device_model(api_key, device_id)
        if not model:
            print(f"Error: Could not find model for device {device_id}", file=sys.stderr)
            print("Please provide --model explicitly", file=sys.stderr)
            sys.exit(1)
        print(f"Found model: {model}")
    
    # Execute command
    if args.command == 'status':
        get_device_status(api_key, device_id, model)
    elif args.command == 'turn-on':
        turn_on(api_key, device_id, model)
    elif args.command == 'turn-off':
        turn_off(api_key, device_id, model)
    elif args.command == 'color':
        set_color(api_key, device_id, model, args.r, args.g, args.b)
    elif args.command == 'brightness':
        set_brightness(api_key, device_id, model, args.value)
    elif args.command == 'color-temp':
        set_color_temp(api_key, device_id, model, args.temp)


if __name__ == '__main__':
    main()
