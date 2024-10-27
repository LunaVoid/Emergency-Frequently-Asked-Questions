import asyncio
from bleak import BleakClient, BleakScanner
import wave
import numpy as np

ESP32_NAME = "ESP32"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


def read_wav_all_points(filename):
    # Open the .wav file
    with wave.open(filename, 'rb') as wav_file:
        # Get the audio parameters
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

        # Read all frames from the audio
        frames = wav_file.readframes(n_frames)

        # Convert the raw frames to numpy array
        dtype = np.int16 if sample_width == 2 else np.int8  # 16-bit PCM or 8-bit PCM
        data = np.frombuffer(frames, dtype=dtype)

        # Reshape for stereo audio (2 channels)
        if n_channels == 2:
            data = data.reshape(-1, 2)

    return frame_rate, data


def normalize_audio(audio_data):
    """
    Normalize audio data to range [0, 255].
    
    Parameters:
    audio_data (np.ndarray): Array of audio samples to normalize.
    
    Returns:
    np.ndarray: Normalized audio samples in the range [0, 255].
    """
    # Determine min and max values based on the data type
    if audio_data.dtype == np.int16:
        min_val, max_val = -32768, 32767
    elif audio_data.dtype == np.uint8:
        min_val, max_val = 0, 255
    else:
        raise ValueError("Unsupported data type for normalization.")
    
    # Normalize to range [0, 255]
    normalized_audio = ((audio_data - min_val) * (255 / (max_val - min_val))).astype(np.uint8)
    
    return normalized_audio


async def run(address, debug=False):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        #framerate,data = read_wav_all_points("Bluetooth/Hurricane.wav")
        framerate,data = read_wav_all_points("Bluetooth/flood.wav")
        normalized = normalize_audio(data)
        name = bytes([int(item) for item in normalized])
        await client.write_gatt_char(CHARACTERISTIC_UUID, name)

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == ESP32_NAME:
            print(f"Found {ESP32_NAME} with address {d.address}")
            await run(d.address)
            return

    print(f"{ESP32_NAME} not found")

asyncio.run(main())