import sounddevice as sd
import numpy as np
import scipy.signal

# Audio settings
SAMPLERATE = 44100  # Sample rate (Hz)
BLOCKSIZE = 1024    # Block size for real-time processing
PITCH_SHIFT = 0.9   # Pitch shift factor (1.0 = no change, >1.0 = higher, <1.0 = lower)
REVERB_DECAY = 0.9  # Reverb decay factor (0.0 to 1.0)

# Function to apply pitch shift
def pitch_shift(audio_block, pitch_factor):
    return scipy.signal.resample(audio_block, int(len(audio_block) * pitch_factor))

# Function to apply reverb effect
def apply_reverb(audio_block, decay):
    delay_samples = int(0.03 * SAMPLERATE)  # 30ms delay
    reverb_signal = np.zeros(len(audio_block) + delay_samples)
    reverb_signal[:len(audio_block)] = audio_block
    for i in range(delay_samples, len(reverb_signal)):
        reverb_signal[i] += decay * reverb_signal[i - delay_samples]
    return reverb_signal[:len(audio_block)]

# Real-time audio processing function
def real_time_voice_changer(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Flatten audio input to 1D array
    audio_block = indata[:, 0]

    # Apply pitch shift
    shifted_audio = pitch_shift(audio_block, PITCH_SHIFT)

    # Apply reverb
    reverb_audio = apply_reverb(shifted_audio, REVERB_DECAY)

    # Make sure the output array matches the expected size
    outdata[:, 0] = np.resize(reverb_audio, len(outdata))

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
