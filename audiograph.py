import sys
import wave
import matplotlib.pyplot as plt
from pathlib import Path

def readfile():
    file = input("Enter the relative filepath of a .wav file. EX: ~/Desktop/myfile.wav \n")
    file = Path(file).expanduser()  # Convert to absolute path

    if not file.exists():
        sys.exit(f"Error: The file {file} does not exist.")

    return str(file)  # Return file path as a string

def plot_waveform(audio_data, channel_count, frequency):
    """Plots the waveform with a black background, white grid, and neon blue wave."""
    time = [i / frequency for i in range(len(audio_data[0]))]  # Generate time axis

    fig, axes = plt.subplots(channel_count, 1, figsize=(12, 6), sharex=True)
    fig.patch.set_facecolor('#2b2d30')  # Set figure background to black

    if channel_count == 1:
        axes = [axes]  # Ensure axes is iterable for mono audio

    for ch in range(channel_count):
        axes[ch].set_facecolor('#2b2d30')  # ✅ Set the actual plot (axes) background to black
        axes[ch].plot(time, audio_data[ch], color='#4470AD', label=f"Channel {ch + 1}")  # Neon blue wave
        axes[ch].set_ylabel("Amplitude", color='white')
        axes[ch].set_ylim(-1, 1)
        axes[ch].legend(loc="upper right", facecolor='black', edgecolor='white', labelcolor='white')

        # White grid with slightly dim color for better contrast
        axes[ch].grid(color='#BBBBBB', linestyle='--', linewidth=0.7, alpha=0.6)

        # Set axes spines (borders) to white
        for spine in axes[ch].spines.values():
            spine.set_color('white')

        axes[ch].tick_params(axis='both', colors='white')  # Make tick labels white

    axes[-1].set_xlabel("Time (seconds)", color='white')
    plt.suptitle("Waveform of the Audio File (Normalized)", color='white')
    plt.show()

def main():
    file = readfile()
    wav_file = wave.open(file, 'rb')

    # Read metadata
    metadata = {
        "Channel Count": wav_file.getnchannels(),
        "Sample Width (bytes)": wav_file.getsampwidth(),
        "Sample Rate (Hz)": wav_file.getframerate(),
        "Total Samples Per Channel": wav_file.getnframes(),
        "Compression Type": wav_file.getcomptype(),
    }

    # Print metadata in a clean format
    print("\nAudio File Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Extract important values
    channel_count = metadata["Channel Count"]
    sample_width = metadata["Sample Width (bytes)"]
    frequency = metadata["Sample Rate (Hz)"]
    total_samples_per_channel = metadata["Total Samples Per Channel"]

    # Read raw audio data
    raw_data = wav_file.readframes(total_samples_per_channel * channel_count)
    wav_file.close()

    # Prepare list to store audio samples for each channel
    audio_data = [[] for _ in range(channel_count)]
    frame_size = sample_width * channel_count  # Bytes per frame

    # Process raw audio data frame by frame
    for frame_start in range(0, len(raw_data), frame_size):
        for ch in range(channel_count):
            sample_start = frame_start + (ch * sample_width)
            sample_end = sample_start + sample_width

            # Extract sample bytes
            sample_bytes = raw_data[sample_start:sample_end]

            # Convert bytes to integer (handle signed PCM)
            if sample_width == 1:  # 8-bit PCM is unsigned
                sample_value = int.from_bytes(sample_bytes, byteorder='little', signed=False) - 128
            else:  # 16-bit and higher PCM is signed
                sample_value = int.from_bytes(sample_bytes, byteorder='little', signed=True)

            audio_data[ch].append(sample_value)

    # Normalize the audio data to the range [-1, 1]
    max_amplitude = (2 ** (8 * sample_width - 1)) - 1  # Calculate max amplitude based on bit depth
    audio_data = [[sample / max_amplitude for sample in channel] for channel in audio_data]

    # Plot the waveform
    plot_waveform(audio_data, channel_count, frequency)

if __name__ == "__main__":
    main()