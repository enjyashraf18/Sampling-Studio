import pandas as pd
from PyQt5.QtWidgets import QFileDialog

def upload_csv(widget):
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(widget, "Open CSV File", "", "CSV Files (*.csv)", options=options)
    if file_name:
        dataframe = pd.read_csv(file_name)
        data_x = dataframe.iloc[:, 0].values
        data_y = dataframe.iloc[:, 1].values
        # plot_original_signal(data_x, data_y)
        # plot_reconstructed_signal(data_x, data_y, 1/500)