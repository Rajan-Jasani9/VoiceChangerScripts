import sounddevice as sd
import numpy as np
import scipy.signal

# Audio settings
SAMPLERATE = 44100  # Sample rate (Hz)
BLOCKSIZE = 1024    # Block size for real-time processing
PITCH_SHIFT = 0.5   # Pitch shift factor (1.0 = no change, >1.0 = higher, <1.0 = lower)

# Function to change pitch without affecting speed
def pitch_shift(audio_block, pitch_factor):
    return scipy.signal.resample(audio_block, int(len(audio_block) * pitch_factor))

# Real-time audio processing function
def real_time_voice_changer(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Flatten audio input to 1D array
    audio_block = indata[:, 0]

    # Apply pitch shift
    shifted_audio = pitch_shift(audio_block, PITCH_SHIFT)

    # Make sure the output array matches the expected size
    outdata[:, 0] = np.resize(shifted_audio, len(outdata))

# Start the audio stream
with sd.Stream(
    samplerate=SAMPLERATE,
    blocksize=BLOCKSIZE,
    dtype="float32",
    channels=1,
    callback=real_time_voice_changer
):
    print("🎤 Speak into the microphone... (Press Ctrl+C to stop)")
    sd.sleep(100000)  # Keep the stream running for a long time
