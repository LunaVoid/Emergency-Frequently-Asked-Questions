import asyncio
from bleak import BleakScanner, BleakClient

async def connect_by_name(device_name):
    print(f"Searching for device: {device_name}")
    
    # Scan for devices
    devices = await BleakScanner.discover()
    
    # Find the device with the matching name
    for device in devices:
        if device.name == device_name:
            print(f"Found device: {device.name} ({device.address})")
            
            # Attempt to connect
            async with BleakClient(device.address) as client:
                if client.is_connected:
                    print(f"Connected to {device.name}")
                    
                else:
                    print(f"Failed to connect to {device.name}")
            
            return
    
    print(f"Device '{device_name}' not found")

# Replace 'ESP32-BT' with your device's name
asyncio.run(connect_by_name("ESP32_BT"))