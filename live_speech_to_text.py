# Live Speech-to-Text using Faster-Whisper
# This program captures audio from your microphone in real-time,
# breaks it into chunks, and uses AI (Whisper) to convert speech to text.
# Install dependencies: pip install faster-whisper pyaudio numpy

import pyaudio  # Library for recording audio from microphone
import numpy as np  # Library for numerical operations on audio data
from faster_whisper import WhisperModel  # AI model for speech-to-text
import time  # For adding pauses between recordings

# Function to calculate RMS (Root Mean Square) power - used to detect silence
def calculate_rms(audio_chunk):
    """Calculate RMS power of audio chunk to determine noise level."""
    audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32)
    rms = np.sqrt(np.mean(audio_np ** 2))
    return rms

# Function to detect silence
def is_silence(audio_chunk, threshold=500):
    """
    Check if audio chunk is silent (below threshold).
    threshold: RMS value below which audio is considered silent (default 500)
    """
    rms = calculate_rms(audio_chunk)
    return rms < threshold

# Initialize the Whisper AI model
# "tiny.en" is a small, fast model optimized for English
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
SILENCE_THRESHOLD = 1.5 # Seconds of silence needed to trigger transcription

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
print("The script will auto-transcribe when it detects XX second of silence.")
print("Press Ctrl+C to stop.\n")

try:
    while True:  # Main loop - keeps recording and transcribing forever
        frames = []  # List to store audio data chunks
        silence_duration = 0  # Track consecutive silence time in seconds
        
        
        while True:  # Inner loop - records until silence is detected
            data = stream.read(CHUNK)  # Read one chunk from the microphone
            frames.append(data)
            
            # Check if this chunk is silent
            if is_silence(data, threshold=500):
                silence_duration += (CHUNK / RATE)  # Add chunk duration to silence counter
            else:
                silence_duration = 0  # Reset if sound is detected
            
            # If silence has lasted long enough, stop recording and transcribe
            if silence_duration >= SILENCE_THRESHOLD:
                # print("\r" + " " * 30 + "\r", end="")  # Clear "Listening" text
                # print("Silence detected. Processing...")
                break
        
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
            # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            transcribed_text += segment.text + " "
        
        print(transcribed_text.strip())

except KeyboardInterrupt:  # This catches when you press Ctrl+C
    print("\nStopping...")

finally:  # This always runs, even if there's an error
    # Clean up: close the microphone stream and PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()
