import librosa
import soundfile as sf
import json

# Function to restore the original voice using metadata
def restore_original_voice(modified_file, output_file, original_metadata, pitch_shift=4):
    # Load the modified audio file
    audio, sr = librosa.load(modified_file, sr=None)

    # Reverse the pitch shift
    restored_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=-pitch_shift)

    # Ensure the sample rate matches the original
    if sr != original_metadata["sample_rate"]:
        restored_audio = librosa.resample(restored_audio, orig_sr=sr, target_sr=original_metadata["sample_rate"])

    # Save the restored audio
    sf.write(output_file, restored_audio, original_metadata["sample_rate"])
    print(f"Original voice restored and saved as '{output_file}'")

# Main script execution
if __name__ == '__main__':
    # Load original metadata from JSON file
    try:
        with open('metadata.json', 'r') as f:
            original_metadata = json.load(f)
    except FileNotFoundError:
        print("Error: 'metadata.json' file not found.")
        exit(1)

    # Restore the original voice
    restore_original_voice('changed_audio.wav', 'restored_audio.mpr', original_metadata)
