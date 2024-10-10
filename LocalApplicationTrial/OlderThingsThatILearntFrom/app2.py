import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QStackedWidget,
    QFileDialog,
    QLabel,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd


# Define Dash app
def create_dash_app():
    app = dash.Dash(__name__)

    # Sample data for the Plotly visualization
    df = px.data.iris()

    app.layout = html.Div(
        [
            dcc.Graph(
                id="iris-scatter",
                figure=px.scatter(
                    df,
                    x="sepal_width",
                    y="sepal_length",
                    color="species",
                    title="Iris Dataset Scatter Plot",
                ),
            )
        ]
    )

    return app


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization and Machine Learning App")
        self.setGeometry(100, 100, 800, 600)

        # Create a stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.home_page = HomePage()
        self.ml_page = MLPage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.ml_page)

        # Navigation layout
        self.navigation_layout = QVBoxLayout()

        # Home page button
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.show_home_page)
        self.navigation_layout.addWidget(home_button)

        # Machine Learning page button
        ml_button = QPushButton("Machine Learning")
        ml_button.clicked.connect(self.show_ml_page)
        self.navigation_layout.addWidget(ml_button)

        # Create a QWidget for the navigation buttons
        navigation_widget = QWidget()
        navigation_widget.setLayout(self.navigation_layout)

        # Add navigation widget to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(navigation_widget)
        main_layout.addWidget(self.stacked_widget)

        # Set main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_ml_page(self):
        self.stacked_widget.setCurrentWidget(self.ml_page)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a QWebEngineView to hold the Dash app
        self.dash_view = QWebEngineView()
        layout.addWidget(self.dash_view)

        self.setLayout(layout)
        self.load_dash_app()

    def load_dash_app(self):
        # Create and run the Dash app in a separate thread
        dash_app = create_dash_app()
        dash_app.run_server(port=8050, use_reloader=False)  # Disable reloader

        # Load the Dash app in QWebEngineView
        self.dash_view.setUrl("http://127.0.0.1:8050")


class MLPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a button to upload an Excel file
        upload_button = QPushButton("Upload Excel File")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)

        # Create a QLabel to display results
        self.result_label = QLabel("Results will be displayed here.")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def upload_file(self):
        # Open a file dialog to select an Excel file
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_name:
            self.generate_seaborn_plot(file_name)

    def generate_seaborn_plot(self, file_name):
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file_name)

        # Example: Generate a seaborn plot for demonstration
        # Assuming the DataFrame has columns 'x' and 'y' for plotting
        if "x" in df.columns and "y" in df.columns:
            # Create a seaborn scatter plot
            sns_plot = sns.scatterplot(data=df, x="x", y="y")
            sns_plot.set_title("Seaborn Scatter Plot")
            sns_plot.figure.show()
            self.result_label.setText("Plot generated successfully!")
        else:
            self.result_label.setText(
                "Error: DataFrame must contain 'x' and 'y' columns."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
