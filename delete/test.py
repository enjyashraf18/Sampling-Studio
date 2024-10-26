import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog


class SignalReconstructionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Reconstruction with Shannon-Whittaker")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a button to load CSV and reconstruct the signal
        self.button_load = QPushButton("Load CSV and Reconstruct Signal")
        self.button_load.clicked.connect(self.load_csv_and_reconstruct)
        self.layout.addWidget(self.button_load)

        # Create a matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def shannon_whittaker_reconstruction(self, sampled_y, sampled_x, reconstruction_points):
        """ Perform the Shannon-Whittaker reconstruction """
        sinc_matrix = np.tile(reconstruction_points, (len(sampled_x), 1)) - np.tile(sampled_x[:, np.newaxis], (1, len(reconstruction_points)))
        return np.dot(sampled_y, np.sinc(sinc_matrix / (sampled_x[1] - sampled_x[0])))

    def load_csv_and_reconstruct(self):
        """ Load CSV file and reconstruct the signal """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            # Read the CSV file
            data = pd.read_csv(file_name)
            sampled_x = data['time'].values  # Assuming the column is named 'time'
            sampled_y = data['magnitude'].values  # Assuming the column is named 'magnitude'

            # Define reconstruction points based on the time range
            reconstruction_points = np.linspace(sampled_x.min(), sampled_x.max(), num=len(sampled_x))

            # Perform reconstruction
            reconstructed_signal = self.shannon_whittaker_reconstruction(sampled_y, sampled_x, reconstruction_points)

            # Plotting
            self.figure.clear()
            ax1 = self.figure.add_subplot(311)
            ax1.plot(sampled_x, sampled_y, label='Sampled Signal', color='red', marker='o', linestyle='None')
            ax1.set_title('Sampled Signal')
            ax1.set_xlabel('Time (s)')
            ax1.set_ylabel('Magnitude')
            ax1.grid()

            ax2 = self.figure.add_subplot(312)
            ax2.plot(reconstruction_points, reconstructed_signal, label='Reconstructed Signal', color='green')
            ax2.set_title('Reconstructed Signal')
            ax2.set_xlabel('Time (s)')
            ax2.set_ylabel('Magnitude')
            ax2.grid()

            self.canvas.draw()  # Refresh the canvas


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalReconstructionApp()
    window.show()
    sys.exit(app.exec_())