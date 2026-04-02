# Live Speech-to-Text using Faster-Whisper
# This program captures audio from your microphone in real-time,
# breaks it into chunks, and uses AI (Whisper) to convert speech to text.
# Install dependencies: pip install faster-whisper pyaudio numpy

import pyaudio  # Library for recording audio from microphone
import numpy as np  # Library for numerical operations on audio data
from faster_whisper import WhisperModel  # AI model for speech-to-text
import time  # For adding pauses between recordings

# Initialize the Whisper AI model
# "tiny.en" is a small, fast model optimized for English
# Change to "small" for better accuracy (but slower processing)
model_size = "tiny.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Audio recording parameters - these control how we capture sound
FORMAT = pyaudio.paInt16  # Audio format: 16-bit signed integers (-32768 to 32767)
                          # This gives good quality without using too much memory
CHANNELS = 1  # Mono audio (1 channel) - we don't need stereo for speech
RATE = 16000  # Sampling rate: 16,000 samples per second
              # Think of this as taking 16,000 "snapshots" of the sound wave each second
              # Whisper AI was trained on 16kHz audio, so we use this rate
CHUNK = 1024  # Buffer size: read 1024 samples at a time
              # Instead of reading the whole recording at once, we process it in small pieces
              # This makes the program more responsive and uses less memory
RECORD_SECONDS = 5  # How long to record each chunk of audio (in seconds)

# Initialize PyAudio - this handles the microphone input
audio = pyaudio.PyAudio()

# Open the microphone stream
# This creates a connection to your microphone that we can read from
stream = audio.open(format=FORMAT,      # Audio format we specified
                    channels=CHANNELS,  # Mono audio
                    rate=RATE,          # 16kHz sampling rate
                    input=True,         # We're recording (input), not playing (output)
                    frames_per_buffer=CHUNK)  # Read in chunks of 1024 samples

print("Live Speech-to-Text started. Speak into the microphone...")
print("Press Ctrl+C to stop.")

try:
    while True:  # Main loop - keeps recording and transcribing forever
        # print("\nRecording... Speak now!")
        frames = []  # List to store audio data chunks

        # Record audio for the specified number of seconds
        # We calculate how many chunks we need: (samples/second * seconds) / chunk_size
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)  # Read one chunk from the microphone
            frames.append(data)        # Add it to our list


        # Convert the recorded audio to a format Whisper can understand
        # First, join all the chunks into one big block of audio data
        audio_data = b''.join(frames)
        # Convert to numpy array: from 16-bit integers to 32-bit floats, normalized to -1 to 1
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        # Send the audio to Whisper AI for transcription
        segments, info = model.transcribe(audio_np, language="en", beam_size=5)

        # (Optional) Show what language Whisper detected
        # print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

        # Combine all the transcribed text segments into one string
        transcribed_text = ""
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            transcribed_text += segment.text + " "

        # Print the final transcribed text
        print(f"Transcribed: {transcribed_text.strip()}")

        # Wait 1 second before starting the next recording
        # This gives you time to see the result and prepare for the next chunk
        # time.sleep(1)

except KeyboardInterrupt:  # This catches when you press Ctrl+C
    print("\nStopping...")

finally:  # This always runs, even if there's an error
    # Clean up: close the microphone stream and PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()