import sys
import joblib

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QProgressBar
)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

pipeline = joblib.load(
    "house_price_pipeline.pkl"
)

class HousePricePredictor(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("House Price Predictor")
        self.resize(700, 700)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        title = QLabel("House Price Prediction System")
        title.setFont(
            QFont(
                "Arial",
                18,
                QFont.Bold
            )
        )
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        self.area = QLineEdit()
        self.area.setPlaceholderText("Enter Area")
        main_layout.addWidget(QLabel("Area"))
        main_layout.addWidget(self.area)
        self.bedrooms = QLineEdit()
        main_layout.addWidget(QLabel("Bedrooms"))
        main_layout.addWidget(self.bedrooms)
        self.bathrooms = QLineEdit()
        main_layout.addWidget(QLabel("Bathrooms"))
        main_layout.addWidget(self.bathrooms)
        self.stories = QLineEdit()
        main_layout.addWidget(QLabel("Stories"))
        main_layout.addWidget(self.stories)
        self.parking = QLineEdit()
        main_layout.addWidget(QLabel("Parking"))
        main_layout.addWidget(self.parking)
        self.mainroad = self.create_dropdown()
        self.guestroom = self.create_dropdown()
        self.basement = self.create_dropdown()
        self.hotwater = self.create_dropdown()
        self.aircondition = self.create_dropdown()
        self.prefarea = self.create_dropdown()
        self.furnishing = QComboBox()
        self.furnishing.addItems([
            "Furnished",
            "Semi-Furnished",
            "Unfurnished"
        ])
        main_layout.addWidget(QLabel("Main Road"))
        main_layout.addWidget(self.mainroad)
        main_layout.addWidget(QLabel("Guest Room"))
        main_layout.addWidget(self.guestroom)
        main_layout.addWidget(QLabel("Basement"))
        main_layout.addWidget(self.basement)
        main_layout.addWidget(QLabel("Hot Water Heating"))
        main_layout.addWidget(self.hotwater)
        main_layout.addWidget(QLabel("Air Conditioning"))
        main_layout.addWidget(self.aircondition)
        main_layout.addWidget(QLabel("Preferred Area"))
        main_layout.addWidget(self.prefarea)
        main_layout.addWidget(QLabel("Furnishing Status"))
        main_layout.addWidget(self.furnishing)
        self.predict_button = QPushButton("Predict House Price")
        self.predict_button.clicked.connect(self.predict_price)
        main_layout.addWidget(self.predict_button)
        self.result = QLabel("Predicted Price Will Appear Here")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setFont(
            QFont(
                "Arial",
                14,
                QFont.Bold
            )
        )
        main_layout.addWidget(self.result)
        score_label = QLabel("Model Reliability (R² Score)")
        self.score_bar = QProgressBar()
        self.score_bar.setMaximum(100)
        self.score_bar.setValue(76)
        self.score_bar.setFormat("R² = 0.762")
        main_layout.addWidget(score_label)
        main_layout.addWidget(self.score_bar)
        self.setLayout(main_layout)

    def create_dropdown(self):
        combo = QComboBox()
        combo.addItems(["No", "Yes"])
        return combo

    def predict_price(self):
        house = [[
            int(self.area.text()),
            int(self.bedrooms.text()),
            int(self.bathrooms.text()),
            int(self.stories.text()),
            self.mainroad.currentIndex(),
            self.guestroom.currentIndex(),
            self.basement.currentIndex(),
            self.hotwater.currentIndex(),
            self.aircondition.currentIndex(),
            int(self.parking.text()),
            self.prefarea.currentIndex(),
            self.furnishing.currentIndex()
        ]]

        prediction = pipeline.predict(house)[0]
        self.result.setText(f"Predicted Price: ₹ {prediction:,.0f}")

app = QApplication(sys.argv)
window = HousePricePredictor()
window.show()
sys.exit(
    app.exec_()
)