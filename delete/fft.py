import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV Data
ecg_data = pd.read_csv('../Signals/ECG_DATA1000.csv')  # Replace with your actual CSV file path
time = np.array(ecg_data['time'])  # Adjust column names as needed
magnitude = np.array(ecg_data['signal'])

# Perform FFT
fft_result = np.fft.fft(magnitude)
frequencies = np.fft.fftfreq(len(fft_result), time[1] - time[0])

# Only consider positive frequencies
magnitude_spectrum = np.abs(fft_result)
positive_frequencies = frequencies[frequencies >= 0]
positive_magnitude_spectrum = magnitude_spectrum[frequencies >= 0]

# Find the peak frequency
peak_freq = positive_frequencies[np.argmax(positive_magnitude_spectrum)]

print(f"The peak frequency is: {peak_freq} Hz")

# Optional: Plot the magnitude spectrum
plt.plot(positive_frequencies, positive_magnitude_spectrum)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Magnitude Spectrum')
plt.show()
