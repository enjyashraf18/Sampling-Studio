import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QMessageBox, QFileDialog, QSlider, QWidget, QVBoxLayout, QLabel, QComboBox,QCheckBox
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from SignalClass import SignalClass
from composer import SignalComposer
import math

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("SamplingStudio.ui", self)
        self.setWindowTitle("Sampling Studio")
        window_icon = QIcon("Deliverables/sampling_icon.png")
        self.setWindowIcon(window_icon)

        self.current_original_signal = None
        self.original_signals_list = []
        self.signals_uploaded_count = 0
        self.mixer_window = None
        self.composed_datax = []
        self.composed_datay = []
        self.signal_states = {}

        

        self.upload_button = self.findChild(QPushButton, 'uploadButton')
        self.upload_button.clicked.connect(self.upload_signal)

        self.frequency_slider = self.findChild(QSlider, 'frequencyCombobox')
        self.frequency_slider.valueChanged.connect(self.change_sampling_frequency)
        self.frequency_label = self.findChild(QLabel, 'frequencyQuantity')
        self.frequency_unit = self.findChild(QLabel,'hz')

        self.normalize_frequency = self.findChild(QCheckBox, 'normalize')
        self.normalize_frequency.stateChanged.connect(self.update_frequency_range)

        self.reconstruction_method = self.findChild(QComboBox, 'reconstructionComboBox')
        self.reconstruction_method.addItems(["Whittaker-Shannon", "Cubic Spline", "Lanczos"])
        current_reconstruction_method = self.reconstruction_method.currentText()
        self.reconstruction_method.currentIndexChanged.connect(lambda: self.update_reconstruction_method(
                                                               current_reconstruction_method))

        self.vertical_layout_11 = self.findChild(QVBoxLayout, 'verticalLayout_11')
        self.vertical_layout_10 = self.findChild(QVBoxLayout, 'verticalLayout_10')
        self.vertical_layout_8 = self.findChild(QVBoxLayout, 'verticalLayout_8')
        self.vertical_layout_9 = self.findChild(QVBoxLayout, 'verticalLayout_9')

        self.first_plot_widget = self.findChild(QWidget, 'originalWindow')
        self.second_plot_widget = self.findChild(QWidget, 'reconstructedWindow')
        self.third_plot_widget = self.findChild(QWidget, 'differenceWindow')
        self.fourth_plot_widget = self.findChild(QWidget, 'frequencyWindow')
        self.phase_slider = self.findChild(QSlider, 'phaseSlider')
        self.phase_label = self.findChild(QLabel, 'phaseQuantity')
        self.phase_slider.setRange(0, 360)
        self.signal_type = self.findChild(QComboBox, 'waveCompobox')
        self.signal_type.addItem('Sine')
        self.signal_type.addItem('Cosine')



        

        self.signalCombobox = self.findChild(QComboBox, 'signalComboBox')
        self.signalCombobox.setStyleSheet("""
            QComboBox {
                color: rgb(255, 255, 255);
                font-size: 18px;
                background-color: rgb(24, 24, 24);
                padding-left: 15px;
                border: 1px solid transparent;
                border-radius: 15px; /* Rounded corners */
            }
            
            QComboBox QAbstractItemView {
                background-color: #444444;    /* Dropdown list background */
                color: #ffffff;               /* Dropdown list text color */
                selection-background-color: #555555;  /* Highlight background */
                selection-color: #FF5757;     /* Highlighted text color */
                border: None;
            }

            /* Remove the default arrow */
            QComboBox::drop-down {
                margin-right: 10px;
                border-top-right-radius: 15px; /* Apply radius to the top-right */
                border-bottom-right-radius: 15px; /* Apply radius to the bottom-right */
            }

            /* Customize the arrow (triangle) */
            QComboBox::down-arrow {
                image: url(Deliverables/down-arrow.png); /* Optional: use a custom image for the arrow */
                width: 10px;
                height: 10px;
                margin-right: 10px; /* Moves the arrow more to the right */
            }
        """)

        
        self.signalCombobox.setEditable(False)
        self.signalCombobox.currentIndexChanged.connect(self.update_signal)

        self.removeButton = self.findChild(QPushButton, 'binButton')
        self.addNoiseCheckBox = self.findChild(QCheckBox, 'addNoise')
        self.snrSlider = self.findChild(QSlider, 'snr')
        self.snrLabel = self.findChild(QtWidgets.QLabel, 'snrQuantity')

        self.removeButton.clicked.connect(self.delete_signal)
        self.addNoiseCheckBox.stateChanged.connect(
            lambda state: self.snr_state(state))
        self.snrSlider.setEnabled(False)

        # Composer Controls

        self.amplitude_slider = self.findChild(QSlider, 'amplitudeCombobox_3')
        self.amplitude_slider_value = 1
        self.amplitude_slider.setValue(1)
        self.amplitude_slider.setRange(1,10 )

        self.frequency_slider2 = self.findChild(QSlider, 'frequencyCombobox_3')
        # self.frequency_slider.setValue(1)
        # self.frequency_slider.setRange(1, 100)
        self.frequency_label = self.findChild(QLabel, 'frequencyQuantity_3')
        self.amplitude_label = self.findChild(QLabel, 'ampQuantity_3')

        self.signals = self.findChild(QComboBox,'reconstructionComboBox_3')

        
        self.delete_button = self.findChild(QPushButton, 'pushButton')
        self.add_button = self.findChild(QPushButton, 'pushButton_2')
        self.save_button = self.findChild(QPushButton, 'pushButton_3')
        # self.plot_graph = self.findChild(QWidget, 'widget_3')

        # self.ay_7aga = self.findChild(QVBoxLayout, 'verticalLayout')
        # self.ay_7aga .removeWidget(self.plot_graph)
        # self.plot_graph = pg.PlotWidget()
        # self.ay_7aga.addWidget(self.plot_graph)

        
        

        # Removing the QWidgets from ui file to add PlotWidgets
        self.vertical_layout_11.removeWidget(self.first_plot_widget)
        self.vertical_layout_10.removeWidget(self.second_plot_widget)
        self.vertical_layout_10.removeWidget(self.third_plot_widget)
        self.vertical_layout_9.removeWidget(self.fourth_plot_widget)
        self.first_plot_widget.deleteLater()
        self.second_plot_widget.deleteLater()
        self.third_plot_widget.deleteLater()
        self.fourth_plot_widget.deleteLater()

        # Adding PlotWidgets to layouts
        self.first_plot = pg.PlotWidget()
        self.second_plot = pg.PlotWidget()
        self.third_plot = pg.PlotWidget()
        self.fourth_plot = pg.PlotWidget()

        self.vertical_layout_11.addWidget(self.first_plot)
        self.vertical_layout_10.addWidget(self.second_plot)
        self.vertical_layout_8.addWidget(self.third_plot)
        self.vertical_layout_9.addWidget(self.fourth_plot)

        self.mixer_window = SignalComposer(self, self.signals, self.first_plot,  self.frequency_slider2,
                                           self.amplitude_label, self.frequency_label, self.phase_slider,
                                           self.phase_label, self.signal_type)

        self.add_button.clicked.connect(self.add_composed_signal)
        self.delete_button.clicked.connect(self.delete_composed_signal)
        self.save_button.clicked.connect(self.save_composed_signal)
        self.amplitude_slider.valueChanged.connect(self.update_amplitude)

        self.frequency_label = self.findChild(QLabel, 'frequencyQuantity')

        # the zoomin into the orignal signal
        self.zoomIn_originalSignal = self.findChild(QPushButton, 'zoomIn1')
        self.zoomOut_origninalSignal = self.findChild(QPushButton, 'zoomOut1')


        # the zooming into the reconstructed signal
        self.zoomIn_reconstructedSignal = self.findChild(QPushButton, 'zoomIn2')
        self.zoomOut_reconstructedSignal = self.findChild(QPushButton, 'zoomOut2')


        # the zooming into the difference signal
        self.zoomIn_differenceSignal = self.findChild(QPushButton, 'zoomIn3')
        self.zoomOut_differenceSignal = self.findChild(QPushButton, 'zoomOut3')


        # the zooming into the frequency graph
        self.zoomIn_frequencySignal = self.findChild(QPushButton, 'zoomIn4')
        self.zoomOut_frequencySignal = self.findChild(QPushButton, 'zoomOut4')


        # link the zooming buttons to function

        self.zoomIn_originalSignal.clicked.connect(lambda: self.zoom(self.first_plot, True))
        self.zoomOut_origninalSignal.clicked.connect(lambda: self.zoom(self.first_plot, False))

        self.zoomIn_reconstructedSignal.clicked.connect(lambda: self.zoom(self.second_plot, True))
        self.zoomOut_reconstructedSignal.clicked.connect(lambda: self.zoom(self.second_plot, False))

        self.zoomIn_differenceSignal.clicked.connect(lambda: self.zoom(self.third_plot, True))
        self.zoomOut_differenceSignal.clicked.connect(lambda: self.zoom(self.third_plot, False))

        self.zoomIn_frequencySignal.clicked.connect(lambda: self.zoom(self.fourth_plot, True))
        self.zoomOut_frequencySignal.clicked.connect(lambda: self.zoom(self.fourth_plot, False))

        # remove the plots
        self.remove_plots = self.findChild(QPushButton, "bin1")
        self.remove_plots.clicked.connect(lambda : self.clear_plots())
    def save_states(self):
        signal_id = int(self.current_original_signal.name.split()[1])-1
        self.signal_states[signal_id] = {
            'snr_checkbox': self.addNoiseCheckBox.isChecked(),
            'snr_value': self.snrSlider.value(),
            'frequency': self.frequency_slider.value(),
            'reconstruction_method': self.reconstruction_method.currentText(),
            'normalize_checkbox': self.normalize_frequency.isChecked()
        }

    def restore_states(self):
        signal_id = self.signalCombobox.currentIndex()
        if signal_id in self.signal_states:
            state = self.signal_states[signal_id]
            self.addNoiseCheckBox.setChecked(state['snr_checkbox'])
            self.snrSlider.setValue(state['snr_value'])
            self.frequency_slider.setValue(state['frequency'])
            self.reconstruction_method.setCurrentText(state['reconstruction_method'])
            self.normalize_frequency.setChecked(state['normalize_checkbox'])
        else:
            self.addNoiseCheckBox.setChecked(False)
            self.snrSlider.setValue(0)
            self.frequency_slider.setValue(int(self.current_original_signal.sampling_frequency))
            self.reconstruction_method.setCurrentIndex(0)
            self.normalize_frequency.setChecked(False)

    def reset_controls(self):
        self.addNoiseCheckBox.setChecked(False)
        self.snrSlider.setValue(1)
        self.snrSlider.setEnabled(False)
        self.frequency_slider.setValue(self.current_original_signal.sampling_frequency)
        self.reconstruction_method.setCurrentIndex(0)  # Default to the first method
        self.normalize_frequency.setChecked(False)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        path = filename[0]
        if path:
            try:
                data = pd.read_csv(path)
                x = data.iloc[:, 0].values
                y = data.iloc[:, 1].values
                return x, y
            except Exception as e:
                print(f"Error, couldn't upload: {e}")
                return None, None
        else:
            return None, None

    def upload_signal(self):
        # Save the current state before changing to a new signal
        if self.current_original_signal is not None:
            self.save_states()

        data_x, data_y = self.open_file()
        if len(data_x) != 1000:
            self.popup_messages("Please upload data of size <b>1000x2</b>.")
        elif data_x is not None and data_y is not None:
            original_color = (20, 200, 150)
            self.signals_uploaded_count += 1
            new_signal_label = f"signal {self.signals_uploaded_count}"
            original_signal = SignalClass(data_x, data_y, 'original', self.first_plot, original_color,
                                          self.signals_uploaded_count, new_signal_label)
            self.original_signals_list.append(original_signal)
            self.current_original_signal = original_signal

            self.signalCombobox.addItem(new_signal_label)
            self.signalCombobox.setCurrentIndex(self.signalCombobox.count() - 1)
            self.clear_plots()
            self.initialise_signals()

            # Reset controls to default values
            self.reset_controls()

    def update_signal(self):
        if self.current_original_signal is not None:
            self.save_states()
        self.clear_plots()
        self.signal_id= self.signalCombobox.currentIndex()
        self.current_original_signal = self.original_signals_list[self.signal_id]
        self.initialise_signals()
        self.restore_states()

    def initialise_signals(self):
        self.current_original_signal.calculate_maximum_frequency()
        self.frequency_slider.setRange(1, 4 * int(self.current_original_signal.maximum_frequency))
        self.frequency_slider.setValue(int(self.current_original_signal.sampling_frequency))

        self.set_axes_limits(self.current_original_signal.data_x, self.current_original_signal.data_y)

        reconstruction_method = self.reconstruction_method.currentText()
        self.plot_signals(reconstruction_method)  # initial reconstruction method
        print(f"max freq: {self.current_original_signal.maximum_frequency}")

    def set_axes_limits(self, data_x, data_y):
        print("INSIDE SET AXES LIMITS")
        min_x = min(data_x)
        max_x = max(data_x)
        min_y = min(data_y)
        max_y = max(data_y)
        print(f"min x: {min_x}")
        print(f"max x: {max_x}")
        print(f"min y: {min_y}")
        print(f"max y: {max_y}")

        self.first_plot.setLimits(xMin=min_x, xMax=max_x, yMin=min_y, yMax=max_y)
        self.second_plot.setLimits(xMin=min_x, xMax=max_x, yMin=min_y, yMax=max_y)
        self.first_plot.setXRange(min_x, max_x)
        self.second_plot.setXRange(min_x,max_x)


    def plot_signals(self,reconstruction_method):
        self.current_original_signal.plot_original_signal()
        self.current_original_signal.plot_sample_points()
        self.current_original_signal.plot_reconstructed_signal(self.second_plot, reconstruction_method)  # replace with choice from dropdown
        self.current_original_signal.plot_difference(self.third_plot)
        self.current_original_signal.create_frequency_domain(self.fourth_plot)


    def clear_plots(self):
        self.first_plot.clear()
        self.second_plot.clear()
        self.third_plot.clear()
        self.fourth_plot.clear()

    def change_sampling_frequency(self):
        try:
            self.current_original_signal.sampling_frequency = self.frequency_slider.value()
        except AttributeError as e:
            print(e)
        if self.normalize_frequency.isChecked():
            self.current_original_signal.sampling_period = 1 / (
                        self.frequency_slider.value() * self.current_original_signal.maximum_frequency)
            self.current_original_signal.sampling_frequency = self.frequency_slider.value() * self.current_original_signal.maximum_frequency
        else:
            self.current_original_signal.sampling_period = 1 / self.frequency_slider.value()
        self.frequency_label.setText(str(self.frequency_slider.value()))
        reconstruction_method = self.reconstruction_method.currentText()
        self.clear_plots()
        self.set_axes_limits(self.current_original_signal.data_x, self.current_original_signal.data_y)
        self.plot_signals(reconstruction_method)

        print(f"sampling frequency: {self.current_original_signal.sampling_frequency}")

    def delete_signal(self):
        
        self.original_signals_list.pop(self.signalCombobox.currentIndex())
        self.signalCombobox.removeItem(self.signalCombobox.currentIndex())
        self.clear_plots()
        if len(self.original_signals_list) == 0:
            return
        self.current_original_signal = self.original_signals_list[0]
        
        self.initialise_signals()

    # def open_mixer_window(self):
    #     # if self.mixer_window is None:
    #     self.mixer_window = SignalComposer()
    #     self.mixer_window.composition_complete.connect(self.handle_composed_signal)
    #     self.mixer_window.show()



    def save_composed_signal(self):
        composed_data_x, composed_data_y, composed_max_freq = self.mixer_window.enter_file_name()

        self.handle_composed_signal(composed_data_x, composed_data_y, composed_max_freq)

    def update_amplitude(self):
        self.mixer_window.update_amplitude_slider(self.amplitude_slider.value())

    def handle_composed_signal(self, data_x, data_y, composed_max_freq):
        original_color = (20, 200, 150)
        self.signals_uploaded_count += 1
        composed_signal = SignalClass(data_x, data_y, 'composed', self.first_plot, original_color,
                                      self.signals_uploaded_count,f"signal {self.signals_uploaded_count}")
        self.original_signals_list.append(composed_signal)
        self.current_original_signal = composed_signal
        self.current_original_signal.maximum_frequency = composed_max_freq
        self.current_original_signal.sampling_frequency = composed_max_freq * 2
        print(f'ay 7aga {self.current_original_signal.maximum_frequency}, {self.current_original_signal.sampling_frequency}')
        self.current_original_signal.sampling_period = 1 / self.current_original_signal.sampling_frequency
        new_signal_label = f"signal {self.signals_uploaded_count}"
        self.signalCombobox.addItem(new_signal_label)
        self.signalCombobox.setCurrentIndex(self.signalCombobox.count() - 1)
        self.clear_plots()
        self.initialise_signals()


    def add_composed_signal(self):
        self.mixer_window.add_signal()
        composed_data_x, composed_data_y, composed_max_freq = self.mixer_window.return_composed_data()
        self.handle_update_composed_signal(composed_data_x, composed_data_y, composed_max_freq)

    def delete_composed_signal(self):
        self.mixer_window.delete_signal()
        composed_data_x, composed_data_y, composed_max_freq = self.mixer_window.return_composed_data()
        self.handle_update_composed_signal(composed_data_x, composed_data_y, composed_max_freq)

    def handle_update_composed_signal(self, data_x, data_y, composed_max_freq):
        self.current_original_signal.update_data(data_x, data_y, composed_max_freq)
        # self.current_original_signal.data_y = data_y
        # self.current_original_signal.data_x = data_x
        # self.current_original_signal.maximum_frequency = composed_max_freq
        # self.current_original_signal.sampling_frequency = composed_max_freq * 2
        # print(f'ay 7aga {self.current_original_signal.maximum_frequency}, {self.current_original_signal.sampling_frequency}')
        # self.current_original_signal.sampling_period = 1 / self.current_original_signal.sampling_frequency
        self.clear_plots()
        self.initialise_signals()

    def create_default_signal(self):
        original_color = (20, 200, 150)
        data_x, data_y, composed_max_freq = self.mixer_window.add_signal()
        composed_signal = SignalClass(data_x, data_y, 'composed', self.first_plot, original_color,
                                      self.signals_uploaded_count, f"signal {self.signals_uploaded_count}")
        self.original_signals_list.append(composed_signal)
        self.current_original_signal = composed_signal
        self.current_original_signal.maximum_frequency = composed_max_freq
        self.current_original_signal.sampling_frequency = composed_max_freq * 2
        print(
            f'ay 7aga {self.current_original_signal.maximum_frequency}, {self.current_original_signal.sampling_frequency}')
        self.current_original_signal.sampling_period = 1 / self.current_original_signal.sampling_frequency
        new_signal_label = f"signal {self.signals_uploaded_count}"
        self.signalCombobox.addItem(new_signal_label)
        self.signalCombobox.setCurrentIndex(self.signalCombobox.count() - 1)






    def snr_state(self,state):
        if state == Qt.Checked:  # checked, so apply noise
            self.snrSlider.setRange(1,50)
            self.snrSlider.setEnabled(True)
            self.snrSlider.setValue(100)
            self.snrLabel.setText(str(self.snrSlider.value()))
            self.snrSlider.valueChanged.connect(self.snr_slider)
        elif state == Qt.Unchecked:  # unchecked, so remove noise
            self.snrSlider.setValue(0)
            self.snrSlider.setEnabled(False)
            self.snrSlider.valueChanged.disconnect()
            self.current_original_signal.remove_noise()
            self.clear_plots()
            self.initialise_signals()

    def snr_slider(self):
        try:
            self.current_original_signal.snr = self.snrSlider.value()
        except AttributeError as e:
            print(e)
        
        self.current_original_signal.adding_noise()
        self.snrLabel.setText(str(self.snrSlider.value()))
        self.clear_plots()
        self.initialise_signals()

    def zoom(self,plot_graph, zoomIn=True):
        # Get the current view range
        x_range, y_range = plot_graph.viewRange()

        self.min_x_range = 0.1
        self.max_x_range = 10
        self.min_y_range = 0.1
        self.max_y_range = 50

        x_center = (x_range[0] + x_range[1]) / 2
        y_center = (y_range[0] + y_range[1]) / 2
        zoom_factor = 0.8

        if zoomIn:
            new_x_range = [(x_center - (x_center - x_range[0]) * zoom_factor),
                           (x_center + (x_range[1] - x_center) * zoom_factor)]
            new_y_range = [(y_center - (y_center - y_range[0]) * zoom_factor),
                           (y_center + (y_range[1] - y_center) * zoom_factor)]
        else:
            new_x_range = [(x_center - (x_center - x_range[0]) / zoom_factor),
                           (x_center + (x_range[1] - x_center) / zoom_factor)]
            new_y_range = [(y_center - (y_center - y_range[0]) / zoom_factor),
                           (y_center + (y_range[1] - y_center) / zoom_factor)]

        new_x_span = new_x_range[1] - new_x_range[0]
        new_y_span = new_y_range[1] - new_y_range[0]

        # Apply limits to x-axis
        if new_x_span < self.min_x_range:
            new_x_range = [x_center - self.min_x_range / 2, x_center + self.min_x_range / 2]

        elif new_x_span > self.max_x_range:
            new_x_range = [x_center - self.max_x_range / 2, x_center + self.max_x_range / 2]

        # Apply limits to y-axis
        if new_y_span < self.min_y_range:
            new_y_range = [y_center - self.min_y_range / 2, y_center + self.min_y_range / 2]

        elif new_y_span > self.max_y_range:
            new_y_range = [y_center - self.max_y_range / 2, y_center + self.max_y_range / 2]

        plot_graph.setXRange(new_x_range[0], new_x_range[1], padding=0)
        plot_graph.setYRange(new_y_range[0], new_y_range[1], padding=0)
        


    def update_frequency_range(self):
        if self.normalize_frequency.isChecked():
            current_value = self.frequency_slider.value()
            self.frequency_slider.setRange(1, 4)
            four_fmax = 4* self.current_original_signal.maximum_frequency
            # if current_value > (3/4) * four_fmax:
            #     self.frequency_slider.setValue(4)
            # elif (3 / 4) * four_fmax > current_value > (1 / 2) * four_fmax:
            #     self.frequency_slider.setValue(3)
            mapped_value = (current_value - 1) * 4 // four_fmax + 1
            self.frequency_slider.setValue(int(mapped_value))
            self.frequency_unit.setText('Fmax')
            self.frequency_unit.setGeometry(200, 350, 40, 21)
        else:
            current_value = self.frequency_slider.value()
            self.frequency_slider.setRange(1, 4 * int(self.current_original_signal.maximum_frequency))
            self.frequency_slider.setValue(int(current_value * self.current_original_signal.maximum_frequency))
            self.frequency_unit.setText('Hz')
            self.frequency_unit.setGeometry(220, 350, 21, 21)

    def update_reconstruction_method(self, previous_value):
        reconstruction_method = self.reconstruction_method.currentText()
        try:
            self.clear_plots()
            self.set_axes_limits(self.current_original_signal.data_x, self.current_original_signal.data_y)
            self.plot_signals(reconstruction_method)
        except AttributeError:
            print(previous_value)
            # To avoid a double popup
            self.reconstruction_method.blockSignals(True)
            self.reconstruction_method.setCurrentText(previous_value)
            self.reconstruction_method.blockSignals(False)

            self.popup_messages('Please upload a signal first.')

    def popup_messages(self, message):
        print("inside popup")
        error_message = QMessageBox()
        error_icon = QIcon("Deliverables/error_icon.png")
        error_message.setWindowIcon(error_icon)
        error_message.setWindowTitle('Error')
        error_message.setText(message)
        error_message.exec_()


app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()
