import librosa
import soundfile as sf
import json

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
if __name__ == '__main__':
    # Load original metadata from JSON file
    try:
        with open('metadata.json', 'r') as f:
            original_metadata = json.load(f)
    except FileNotFoundError:
        original_metadata= {'sample_rate': 48000, 'channels': 1, 'duration': 5.64}
        print("Error: 'metadata.json' file not found using manual metadata.")

    # Restore the original voice
    restore_original_voice('changed_audio.mp3', 'restored_audio.mp3', original_metadata)
