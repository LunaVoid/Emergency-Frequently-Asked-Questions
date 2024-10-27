import bluetooth

def pair_by_name(target_name):
    print(f"Searching for device: {target_name}")
    
    # Perform device discovery
    print("Here")
    nearby_devices = bluetooth.discover_devices(duration=2, lookup_names=True)
    print(nearby_devices)
    print("test")
    target_address = None
    
    # Find the target device by name
    for addr, name in nearby_devices:
        if name == target_name:
            target_address = addr
            break
    
    if target_address is None:
        print(f"Could not find device: {target_name}")
        return
    
    print(f"Found device: {target_name} ({target_address})")
    
    # Attempt to pair with the device
    try:
        print("Attempting to pair...")
        bluetooth.pair_device(target_address)
        print(f"Successfully paired with {target_name}")
    except bluetooth.BluetoothError as e:
        print(f"Pairing failed: {e}")

# Example usage
target_device_name = "ESP32-BT"
pair_by_name(target_device_name)