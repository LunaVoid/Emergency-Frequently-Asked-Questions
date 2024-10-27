import gtts
import os
import subprocess
#from TTS.api import TTS


def createonlineAudio(text,filename = "basicOnline"):
    # Text you want to convert to speech
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')
    # Save the audio to a file
    tts.save(f"{filename}.mp3")
    print("MP3 file has been created.")

'''
def createofflineAudio(text, filename="basicOffline"):
    try:
        # Initialize the TTS model
        tts = TTS(model_name="tts_models/en/ljspeech/vits")
        output_file = f"{filename}.mp3"
        # Generate speech and save to an MP3 file
        tts.tts_to_file(text=text, file_path=output_file)
        print(f"Audio saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
'''
def createLocalAudio(text, filename="basicLocal"):
    aiff_file = f"{filename}.aiff"
    wav_file = f"{filename}.wav"
    try:
        # Save the audio as an AIFF file
        subprocess.call(['say', '-o', aiff_file, text])
        print(f"Saved audio to: {aiff_file}")

        # Convert AIFF to MP3
        subprocess.call(['ffmpeg','-y', '-i', aiff_file,'-ar','8000', wav_file])
        print(f"Converted to MP3: {wav_file}")

        # Optionally remove the AIFF file after conversion
        os.remove(aiff_file)
        print(f"Removed temporary file: {aiff_file}")

    except Exception as e:
        print(f"Error occurred: {e}")

def convertToWAV():
    print("converting")

if __name__ == '__main__':
    createLocalAudio("Flood Alert","flood")
    
    #convertToWAV()