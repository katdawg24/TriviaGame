# settings.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QSpinBox
from PyQt5.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self, settings_callback):
        super().__init__()
        self.setWindowTitle("Game Settings")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #1E1E1E; color: white; font-family: 'Arial';")

        self.settings_callback = settings_callback

        layout = QVBoxLayout()

        self.difficulty_label = QLabel("Select Difficulty:")
        self.difficulty_label.setStyleSheet("margin-bottom: 5px;")
        layout.addWidget(self.difficulty_label)

        self.difficulty_dropdown = QComboBox()
        self.difficulty_dropdown.addItems(["Normal (4 answers)", "Easy (2 answers)"])
        layout.addWidget(self.difficulty_dropdown)

        self.question_label = QLabel("Number of Questions (3-10):")
        self.question_label.setStyleSheet("margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(self.question_label)

        self.question_count = QSpinBox()
        self.question_count.setRange(3, 10)
        self.question_count.setValue(5)
        layout.addWidget(self.question_count)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setStyleSheet(
            "*{background: '#BC006C'; padding: 10px; border-radius: 10px;} *:hover{background: '#ff1b9e';}"
        )
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        difficulty = self.difficulty_dropdown.currentText()
        num_questions = self.question_count.value()
        self.settings_callback(difficulty, num_questions)
        self.close()
