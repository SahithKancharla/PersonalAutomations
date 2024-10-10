import sys
import plotly.express as px
import pandas as pd
import seaborn as sns
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QStackedWidget,
    QFileDialog,
    QLabel,
    QFrame,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization and Machine Learning App")
        self.setGeometry(100, 100, 1000, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Collapsible sidebar menu
        self.sidebar = QFrame()
        self.sidebar.setStyleSheet("background-color: #2A2A2A;")
        self.sidebar.setFixedWidth(200)

        # Navigation layout
        self.navigation_layout = QVBoxLayout(self.sidebar)

        # Home page button
        home_button = QPushButton("Home")
        home_button.setStyleSheet("color: white;")
        home_button.clicked.connect(self.show_home_page)
        self.navigation_layout.addWidget(home_button)

        # Machine Learning page button
        ml_button = QPushButton("Machine Learning")
        ml_button.setStyleSheet("color: white;")
        ml_button.clicked.connect(self.show_ml_page)
        self.navigation_layout.addWidget(ml_button)

        # Create a hamburger menu button
        self.hamburger_button = QPushButton("☰")  # Unicode for hamburger icon
        self.hamburger_button.setStyleSheet(
            "font-size: 24px; color: white; background-color: #2A2A2A;"
        )
        self.hamburger_button.clicked.connect(self.toggle_sidebar)
        self.hamburger_button.setFixedSize(50, 50)
        layout.addWidget(self.hamburger_button, alignment=Qt.AlignLeft)

        # Stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stacked_widget)

        # Create pages
        self.home_page = HomePage()
        self.ml_page = MLPage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.ml_page)

    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.setVisible(False)
        else:
            self.sidebar.setVisible(True)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_ml_page(self):
        self.stacked_widget.setCurrentWidget(self.ml_page)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a button to show Plotly visualization
        self.plot_button = QPushButton("Show Plotly Visualization")
        self.plot_button.setStyleSheet("color: white;")
        self.plot_button.clicked.connect(self.show_plotly_visualization)
        layout.addWidget(self.plot_button)

        # Create a QWebEngineView to hold the plot
        self.plot_view = QWebEngineView()
        layout.addWidget(self.plot_view)

        self.setLayout(layout)

        # Set dark theme for the home page
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

    def show_plotly_visualization(self):
        print("Button clicked! Generating plot...")  # Debug statement

        # Sample data for the Plotly visualization
        df = px.data.iris()

        # Create a Plotly figure
        fig = px.scatter(
            df,
            x="sepal_width",
            y="sepal_length",
            color="species",
            title="Iris Dataset Scatter Plot",
        )

        # Convert the Plotly figure to HTML with embedded resources
        html = fig.to_html(include_plotlyjs="cdn", full_html=True)

        # Load the HTML in the QWebEngineView
        self.plot_view.setHtml(html)
        print("Plot generated and set in the QWebEngineView.")  # Debug statement


class MLPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a button to upload an Excel file
        upload_button = QPushButton("Upload Excel File")
        upload_button.setStyleSheet("color: white;")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)

        # Create a QLabel to display results
        self.result_label = QLabel("Results will be displayed here.")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # Set dark theme for the machine learning page
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

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

    # Set dark theme for the entire application
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: #1E1E1E;
        }
        QPushButton {
            background-color: #3C3C3C;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #5C5C5C;
        }
        QLabel {
            color: white;
        }
    """
    )

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
