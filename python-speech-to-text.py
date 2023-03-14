import os
import datetime
import whisper
import wave
import numpy as np

# Define audio settings
MODEL_PATH = "large" 
result = None

# Load model
model = whisper.load_model(MODEL_PATH)

# Get list of WAV files in current directory, sorted by timestamp (oldest first)
wav_files = sorted([f for f in os.listdir() if f.endswith(".wav")],
                   key=lambda x: datetime.datetime.strptime(x[10:-4], "%Y-%m-%d_%H-%M-%S"),
                   reverse=True)

# Print count of WAV files
print(f"Found {len(wav_files)} WAV files")

# Print oldest and earliest timestamps
if len(wav_files) > 0:
    oldest = datetime.datetime.strptime(wav_files[-1][10:-4], "%Y-%m-%d_%H-%M-%S")
    earliest = datetime.datetime.strptime(wav_files[0][10:-4], "%Y-%m-%d_%H-%M-%S")
    print(f"Oldest file: {oldest}")
    print(f"Earliest file: {earliest}")
else:
    print("No WAV files found")

# Transcribe each WAV file and write result to text file
with open("transcript.txt", "a") as f:
    for wav_file in wav_files:
        # Load audio data from WAV file
        with wave.open(wav_file, "rb") as wf:
            # Transcribe audio data using model
            result = model.transcribe(wav_file)


        # Write transcript to file with timestamp
        timestamp = datetime.datetime.strptime(wav_file[10:-4], "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp}: {result['text']}\n")
        print(f"Wrote to file: {timestamp}: {result['text']}")

print("File closed")
