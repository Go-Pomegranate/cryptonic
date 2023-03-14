import pyaudio
import wave
import datetime

# Define audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
RECORD_SECONDS = 30  # zmienione z 60 na 30

# Create PyAudio object
audio = pyaudio.PyAudio()

while True:
    # Open microphone stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    # Record audio data
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording and close stream
    stream.stop_stream()
    stream.close()

    # Save audio data to WAV file with current timestamp in filename
    filename = datetime.datetime.now().strftime("recording_%Y-%m-%d_%H-%M-%S.wav")
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Open microphone stream for next recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
