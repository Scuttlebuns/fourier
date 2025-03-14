import sys
import wave
# import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from enum import Enum

#wav form data is stored in bit notation,
#to make it easier to represent with correct depth
#this enum helps map it with the sample_width value
# class SampleWidth(Enum):
#     INT8 = 1
#     INT16 = 2
#     INT24 = 3
#     INT32 =4

def readfile():
    choice = input("Would you like to enter a file?: y/n \n")
    if choice == "y":
        print("Enter the relative filepath of a .wav file. EX: ~/Desktop/myfile.wav")
        file = input()
    else:
        file = "ImitationLover_1.wav"
    file = Path(file).expanduser()  # adds full file path

    # Prevents trying to open a non-existent file
    if not file.exists():
        sys.exit(f"Error: The file {file} does not exist.")

    return str(file) #converts to string


import matplotlib.pyplot as plt


def plot_waveform(audio_data, channel_count, frequency):
    time = [i / frequency for i in range(len(audio_data[0]))]  # Generate time axis

    fig, axes = plt.subplots(channel_count, 1, figsize=(12, 6), sharex=True)  # One row per channel

    # Ensure `axes` is always iterable (needed for single-channel case)
    if channel_count == 1:
        axes = [axes]

    for ch in range(channel_count):
        axes[ch].plot(time, audio_data[ch], label=f"Channel {ch + 1}")
        axes[ch].set_ylabel("Amplitude")
        axes[ch].legend(loc="upper right")
        axes[ch].grid()

    axes[-1].set_xlabel("Time (seconds)")  # Label only the last subplot's x-axis
    plt.suptitle("Waveform of the Audio File")
    plt.show()

def main():
    file = readfile()
    wav_file = wave.open(file, 'rb')  # Ensure the file path is a string
    print(f"File: \"{file}\" opened successfully!")

    # print(wav_file.getparams())

    #Read Meta-data in
    channel_count = wav_file.getnchannels() #Mono/Stereo/Spacial
    sample_width =  wav_file.getsampwidth() #Bit depth (1 is 8bit, 2 is 16bit, 3 is 24 bit, 4 is 32 bit)
    frequency = wav_file.getframerate() #48000
    total_samples_per_channel = wav_file.getnframes() #Total samples in song
    compression_type = wav_file.getcomptype() #compression
    comppression_name = wav_file.getcompname() #compression name
    raw_data = wav_file.readframes(total_samples_per_channel * channel_count) #bit representation of data

    metadata = {
        "Channel Count": wav_file.getnchannels(),
        "Sample Width": wav_file.getsampwidth(),
        "Sample Rate (Hz)": wav_file.getframerate(),
        "Total Samples Per Channel": wav_file.getnframes(),
        "Compression Type": wav_file.getcomptype(),
        "Compression Name": wav_file.getcompname(),
    }

    for key, value in metadata.items():
        print(f"{key}: {value}")


    # Read raw audio data in
    print(f"Raw data length: {len(raw_data)}")

    wav_file.close()
    # Create a list to store audio data for each channel
    #An arr of audio channels with each having its own arr of audio data
    audio_data = [[] for _ in range(channel_count)]

    # Process raw audio data frame by frame
    frame_size = sample_width * channel_count  # Number of bytes per frame

    for frame_start in range(0, len(raw_data), frame_size):  # Iterate over frames
        for ch in range(channel_count):  # Iterate over each channel in the frame
            # Find the start of this channel's sample within the frame
            sample_start = frame_start + (ch * sample_width)
            sample_end = sample_start + sample_width  # Stop index (not included in slice)

            # Extract the sample bytes
            sample_bytes = raw_data[sample_start:sample_end]

            # Convert bytes to an integer (handling signed PCM)
            if sample_width == 1:  # 8-bit PCM is unsigned
                sample_value = int.from_bytes(sample_bytes, byteorder='little', signed=False)
                sample_value -= 128  # Convert to signed (-128 to +127)
            else:  # 16-bit and higher are already signed
                sample_value = int.from_bytes(sample_bytes, byteorder='little', signed=True)

            # Store the sample in the corresponding channel list
            audio_data[ch].append(sample_value)

    # normalize the audio data
    #16-bit audio: max_amplitude = 2^(16 - 1) - 1 = 32,767
    #24-bit audio: max_amplitude = 2^(24 - 1) - 1 = 8,388,607
    #32-bit audio: max_amplitude = 2^(32 - 1) - 1 = 2,147,483,647
    max_amplitude = (2 ** (8 * sample_width - 1)) - 1

    scale_factor = 200
    for ch in range(channel_count):
        audio_data[ch] = [  # Store normalized values in place
            (sample / max_amplitude) * scale_factor  # Normalize and scale each sample
            for sample in audio_data[ch]
        ]

    #2 turtle graphics
    #3 start with

    plot_waveform(audio_data, channel_count, frequency)

if __name__=="__main__":
    main()