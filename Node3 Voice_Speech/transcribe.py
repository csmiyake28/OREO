import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import keyboard
import time 




sample_rate = 16000 #16k Hz 
recorded_chunks = []
is_recording = False
message = " "

# Load the model once at the start so it doesn't delay recording later
model = WhisperModel("base", device="cpu", compute_type="int8")


def start_recording():
    # 1. Bring the global variables into this function's scope
    global is_recording, recorded_chunks

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        Continue = True
        while Continue:


            if not is_recording:
                print("Recording started...")
                recorded_chunks.clear()  # 2. Safely empty the list without breaking the reference
                is_recording = True
            keyboard.wait('r')
            if  is_recording:
                is_recording = False
                print("Recording stopped.")
                
                # 3. Prevent the ValueError crash if the list is empty
                if len(recorded_chunks) > 0:
                    audio_data = np.concatenate(recorded_chunks, axis=0)
                    audio_array = np.squeeze(audio_data).astype(np.float32)

                    segments, info = model.transcribe(audio_array, beam_size=5)

                    #concatenate the segments into a single message and return that as the message
                    for segment in segments:
                        message = segment.text
                        return message
                        
                    Continue = False  # Stop the loop after transcription
                else:
                    print("No audio captured.")
            
            # Wait for the user to lift their finger off 'r' before looping again
            # This completely replaces the need for time.sleep(0.5)
            while keyboard.is_pressed('r'):
                time.sleep(0.05)

def audio_callback(indata, frames, time, status):
    """This function runs continuously in the background, capturing audio chunks."""
    if is_recording:
        # Append a copy of the incoming audio to our list
        recorded_chunks.append(indata.copy())

# we need to work on getting it sent to an AI now

def chat_bot_response(message):
    # Placeholder for the actual chat bot implementation



    return reponse

    pass





if __name__ == "__main__":
    
    message = start_recording()
    print(message)

    # response = chat_bot(message)
    
