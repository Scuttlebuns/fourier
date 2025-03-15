# Audio Waveform Visualizer

## Overview
This script reads a `.wav` file and extracts the waveform data visualizing it using `matplotlib`. Eventually a Fourier Transform representation will be supported.

## Features
-  **Reads `.wav` files** (supports mono and multi-channel audio)
-  **Extracts audio metadata** (sample rate, bit depth, number of channels, etc.)
-  **Normalizes waveform data** to the range `-1 to 1`
-  **Plots waveform with Matplotlib** in a visually appealing way
-  **Handles different sample widths** (8-bit, 16-bit, 24-bit, 32-bit PCM)

## Installation
Ensure you have Python installed along with `matplotlib`. You can install the required dependency using:

```sh
pip install matplotlib
```

## Usage
Run the script with:

```sh
python audiograph.py
```

Then, enter the path to your `.wav` file when prompted.

## Example Output
When you run the script, it will print the important metadata from the header of the file:

```sh
Audio File Metadata:
Channel Count: 2
Sample Width (bytes): 2
Sample Rate (Hz): 44100
Total Samples Per Channel: 123456
Compression Type: NONE
```

And display a **waveform plot** with a **gray background** and ** blue visualization**.

## Code Breakdown
###  1. Read the WAV File
- Prompts the user to enter a file path.
- Ensures the file exists before processing.

###  2. Extract Audio Metadata
- Reads **sample rate, channels, bit depth, total samples**.
- Converts multi-channel data correctly.

###  3. Process & Normalize Audio Data
- Extracts waveform samples.
- Converts **8-bit unsigned PCM** to signed format.
- Normalizes values to the range **`[-1, 1]`**.

###  4. Visualize the Waveform
- Uses `matplotlib` to generate a **dark-themed** graph.
- Supports **multi-channel visualization**.

## Future Enhancements
- ✅ **Additional frequency domain analysis (FFT)**
---

This project is a simple but effective way to **visualize audio waveforms in Python**!

