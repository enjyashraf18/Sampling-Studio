import numpy as np
from scipy.interpolate import CubicSpline
import pyqtgraph as pg
from composer import SignalComposer



def whittaker_shannon_interpolation(sampled_x, sampled_y, reconstructed_time):
    interval_time = sampled_x[1] - sampled_x[0]
    reconstructed_y = np.array([np.sum(sampled_y * np.sinc((t - sampled_x) / interval_time))
                                for t in reconstructed_time])
    return reconstructed_y


def cubic_spline_interpolation(x_points,sampled_x, sampled_y):
    cs_func = CubicSpline(sampled_x, sampled_y)
    reconstructed_y = cs_func(x_points)
    return reconstructed_y


def lanczos_interpolation(x_points, sampled_x, sampled_y, a=3):
    def lanczos_kernel(x, a):
        if x == 0:
            return 1
        elif -a < x < a:
            return a * np.sin(np.pi * x) * np.sin(np.pi * x / a) / (np.pi ** 2 * x ** 2)
        else:
            return 0

    # initialise to fill
    reconstructed_y = np.zeros_like(x_points)

    for i, t in enumerate(x_points):
        # Sum contributions from all sampled points, weighted by the Lanczos kernel
        for j, t_j in enumerate(sampled_x):
            x = (t - t_j) / (sampled_x[1] - sampled_x[0])  # Relative distance
            reconstructed_y[i] += sampled_y[j] * lanczos_kernel(x, a)
    return reconstructed_y


class SignalClass:
    def __init__(self, data_x, data_y, signal_type, plot_widget, color, signal_id, name):
        self.data_x = data_x
        self.data_y = data_y
        self.type = signal_type  # original, reconstructed, difference, composed
        self.plot_widget = plot_widget
        self.color = color
        self.signal_id = signal_id
        self.maximum_frequency = None
        self.sampling_frequency = None
        self.sampling_period = None
        self.x_sampled = None
        self.y_sampled = None
        self.y_reconstructed = None
        self.start_time = None
        self.end_time = None
        self.frequencies = []
        self.amplitude = []
        self.before_band_width_line = None
        self.after_band_width_line = None
        self.frequency_line = None
        self.snr = None
        self.noisy_data_y = self.data_y
        self.current_snr_CheckBox = False
        self.current_snr_value = 0
        self.current_frequency = self.maximum_frequency
        self.current_reconstruction_method = "shannon"
        self.current_amplitude = 0
        self.current_normalize_checkbox = False
        self.frequencies_composed = []
        self.amp_composed = []

        self.name = name

    def calculate_maximum_frequency(self):
        if self.type != 'composed':
            time = np.array(self.data_x)
            magnitude = np.array(self.noisy_data_y)
            fft_result = np.fft.fft(magnitude)  # time domain to freq domain
            frequencies = np.fft.fftfreq(len(fft_result), time[1] - time[0])
            positive_frequencies = frequencies[frequencies >= 0]
            self.maximum_frequency = positive_frequencies[-1]
            print(f"hena fmax composed {self.maximum_frequency}")
            self.sampling_frequency = 2*self.maximum_frequency
            print(f"SAMPLING FREQUENCY: {self.sampling_frequency}")
            self.sampling_period = 1/self.sampling_frequency

    def plot_original_signal(self):
        self.plot_widget.plot(self.data_x[100:-100], self.noisy_data_y[100:-100], pen=self.color)

    def plot_sample_points(self):
        self.start_time = np.min(self.data_x)
        self.end_time = np.max(self.data_x)
        self.x_sampled = np.arange(self.start_time, self.end_time, self.sampling_period)
        self.y_sampled = np.interp(self.x_sampled, self.data_x, self.noisy_data_y)
        # for x, y in zip(self.data_x, self.data_y):
        #     if x in x_sampled:
        #         y_sampled.append(y)
        self.plot_widget.plot(self.x_sampled, self.y_sampled, pen=None, symbol='o', symbolSize=4, symbolBrush='w')

    def plot_reconstructed_signal(self, second_plot_widget, method):
        self.reconstructed_time = np.linspace(self.start_time, self.end_time, len(self.data_x))

        if method == 'Whittaker-Shannon':
            print("Reconstruction Method: Whittaker-Shannon")
            self.y_reconstructed = whittaker_shannon_interpolation(self.x_sampled, self.y_sampled, self.reconstructed_time)
        elif method == 'Lanczos':
            print("Reconstruction Method: Lanczos")
            self.y_reconstructed = lanczos_interpolation(self.reconstructed_time, self.x_sampled, self.y_sampled, a=3)
        elif method == 'Cubic Spline':
            print("Reconstruction Method: Cubic Spline")
            self.y_reconstructed = cubic_spline_interpolation(self.reconstructed_time, self.x_sampled, self.y_sampled)
        else:
            raise ValueError("Invalid reconstruction method. Choose 'Whittaker-Shannon', 'Lanczos', or 'Cubic Spline'.")

        # Plot the reconstructed signal
        second_plot_widget.plot(self.reconstructed_time[100:-100], self.y_reconstructed[100:-100], pen=(50,100,240))
        return self.y_reconstructed

    import numpy as np

    def plot_difference(self, third_plot_widget, y_reco):
        difference_y = self.data_y - y_reco
        min_y = min(difference_y)
        max_y = max(difference_y)
        avg_difference = np.mean(np.abs(self.data_y - self.y_reconstructed))
        print(f"Average difference: {avg_difference}")
        plot_item = third_plot_widget.getPlotItem()
        plot_item.clear()
        # Add the plot for the difference
        curve = plot_item.plot(self.data_x[100:-100], difference_y[100:-100], pen=(200, 50, 50), name="Difference")
        legend = plot_item.addLegend()
        legend.clear()
        legend.addItem(curve, f"Avg Difference: {avg_difference:.6f}")

    def create_frequency_domain(self, plot_widget_frequency_domain, calculates_freq):
        fft_result = np.fft.fft(self.data_y)
        frequencies = np.fft.fftfreq(len(fft_result), self.reconstructed_time[1]-self.reconstructed_time[0])
        magnitude = (np.abs(fft_result)[:len(fft_result)])/3000
        frequencies = frequencies[:len(frequencies)]
        print(f"the freq  is {self.frequencies}")
        self.frequency_line = plot_widget_frequency_domain.plot(
            frequencies,
            magnitude,
            pen=pg.mkPen(color="green", width=2.5),
        )
        self.after_band_width_line = plot_widget_frequency_domain.plot(
            frequencies + self.sampling_frequency+0.1, magnitude, pen=pg.mkPen(color="red")
        )
        self.before_band_width_line = plot_widget_frequency_domain.plot(
            frequencies - self.sampling_frequency-0.1 , magnitude , pen = pg.mkPen(color = "red")
        )
        plot_widget_frequency_domain.autoRange()

    def adding_noise(self):
        snr_db = float(self.snr)

        signal_power = np.mean(self.data_y ** 2)

        # Calculate noise power based on desired SNR
        snr_linear = 10 ** (snr_db / 10)  # Convert dB to linear scale
        noise_power = signal_power / snr_linear

        # Generate Gaussian noise and scale it to match the desired noise power
        noise = np.random.normal(0, np.sqrt(noise_power), self.data_y.shape)

        # Create the noisy signal by adding noise to the y-axis values
        self.noisy_data_y = self.data_y + noise

        # return noisy_y

    def update_data(self, data_x, data_y, max_freq):
        self.type = 'composed'
        self.data_x = data_x
        self.data_y = data_y
        self.maximum_frequency = max_freq
        self.sampling_frequency = 2*self.maximum_frequency
        self.sampling_period = 1 / self.sampling_frequency
    
    def remove_noise(self):
        self.noisy_data_y = self.data_y


