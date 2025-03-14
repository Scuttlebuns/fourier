import sys
import wave
from pathlib import Path


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

def main():
    file = readfile()
    wav_file = wave.open(file, 'rb')  # Ensure the file path is a string
    print(f"File: \"{file}\" opened successfully!")

    # print(wav_file.getparams())
    channel_count = wav_file.getnchannels() #Mono/Stereo/Spacial
    sample_width =  wav_file.getsampwidth() #Bit depth (2 is 16bit, 3 is 24 bit, 4 is 32 bit)
    frequency = wav_file.getframerate()
    total_samples_per_channel = wav_file.getnframes()
    compression_type = wav_file.getcomptype()
    comppression_name = wav_file.getcompname()

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
    wav_file.close()



if __name__=="__main__":
    main()