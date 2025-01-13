import json
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import convolve

# Function to extract metadata from the original audio file
def get_audio_metadata(file_path):
    # Load the audio file to get sample rate and duration
    audio, sample_rate = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=audio, sr=sample_rate)
    channels = sf.info(file_path).channels

    # Create metadata dictionary
    metadata = {
        "sample_rate": sample_rate,
        "channels": channels,
        "duration": duration,
        "pitch_shift": 0,
    }

    return metadata

# Function to modify the voice (e.g., pitch shift and reverb)
def change_voice(input_file, output_file, pitch_shift=4, apply_reverb=False):
    # Load audio file
    audio, sr = librosa.load(input_file, sr=None)

    # Apply pitch shifting
    modified_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_shift)

   
    # Save the modified audio
    sf.write(output_file, modified_audio, sr)

    # Update metadata
    metadata = get_audio_metadata(input_file)
    metadata["pitch_shift"] = pitch_shift
   
    # Save metadata to JSON
    with open('metadata.json', 'w') as metadatafile:
        json.dump(metadata, metadatafile)

    print(f"Voice changed and saved as '{output_file}'")

# Function to restore the original voice using metadata
def restore_original_voice(modified_file, output_file, original_metadata):
    # Load the modified audio file
    audio, sr = librosa.load(modified_file, sr=None)

    # Reverse the pitch shift
    pitch_shift = original_metadata.get("pitch_shift", 0)
    restored_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=-pitch_shift)


    # Ensure the sample rate matches the original
    if sr != original_metadata["sample_rate"]:
        restored_audio = librosa.resample(restored_audio, orig_sr=sr, target_sr=original_metadata["sample_rate"])

    # Save the restored audio
    sf.write(output_file, restored_audio, original_metadata["sample_rate"])
    print(f"Original voice restored and saved as '{output_file}'")

# Main script execution
if __name__ == "__main__":
    original_file = "Test-Audio-1.mp3"
    modified_file = "changed_audio.mp3"

    # Step 1: Extract metadata from the original audio file
    metadata = get_audio_metadata(original_file)
    print("Metadata:", metadata)

    # Step 2: Change the voice and save the modified audio (with reverb)
    change_voice(original_file, modified_file, pitch_shift=10, apply_reverb=False)
