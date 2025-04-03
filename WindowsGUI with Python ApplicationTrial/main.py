from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView 
import plotly.express as px
import json
import os
import plotly
import numpy as np

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton("Plot", self)
        self.browser = QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        self.button.clicked.connect(self.show_graph)
        self.resize(1000, 800)

    def show_graph(self):
        # Generate the Plotly figure
        df = px.data.tips()
        fig = px.box(df, x="day", y="total_bill", color="smoker")
        fig.update_traces(quartilemethod="exclusive")

        # Serialize the Plotly figure to JSON
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Load the HTML file using setUrl()
        html_file = os.path.join(os.path.dirname(__file__), 'home.html')
        self.browser.setUrl(QtCore.QUrl.fromLocalFile(html_file))

        # Inject the JSON data into the JavaScript function after the page loads
        def inject_plot_data():
            self.browser.page().runJavaScript(f'renderPlot(`{fig_json}`);')

        # Ensure the JavaScript is called after the page has fully loaded
        self.browser.loadFinished.connect(inject_plot_data)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
