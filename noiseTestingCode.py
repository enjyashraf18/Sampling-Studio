import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore 

import pandas as pd


csv_path = "Signals/ECG_DATA.csv"
csvFile = pd.read_csv(csv_path)   
x= csvFile.iloc[:, 0].values
y= csvFile.iloc[:, 1].values



# User-defined SNR value in dB
snr_db = float(10)
# snr range from -10 to 50 dB
# Calculate signal power as the mean square of the signal
signal_power = np.mean(y ** 2)

# Calculate noise power based on desired SNR
snr_linear = 10 ** (snr_db / 10)  # Convert dB to linear scale
noise_power = signal_power / snr_linear

# Generate Gaussian noise and scale it to match the desired noise power
noise = np.random.normal(0, np.sqrt(noise_power), y.shape)

# Create the noisy signal by adding noise to the y-axis values
noisy_y = y + noise

# Initialize the PyQt application
app = QtWidgets.QApplication([])

# Set up the plot window
win = pg.GraphicsLayoutWidget(show=True, title="Signal with Noise")
win.resize(800, 500)
win.setWindowTitle('Signal Plot')

# Create a plot within the window
plot = win.addPlot(title="Original Signal vs Noisy Signal")
plot.setLabel('left', "Amplitude")
plot.setLabel('bottom', "Time", units='s')

# Plot the original signal
original_pen = pg.mkPen(color=(0, 0, 255, 150), width=2)  # Blue with some transparency
plot.plot(x, y, pen=original_pen, name="Original Signal")

# Plot the noisy signal
noisy_pen = pg.mkPen(color=(255, 0, 0, 100), width=2, dash=[4, 2])  # Red with more transparency
plot.plot(x, noisy_y, pen=noisy_pen, name="Noisy Signal")
# Add a legend
plot.addLegend()

if __name__ == '__main__':
    app.exec()