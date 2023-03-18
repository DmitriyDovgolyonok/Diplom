import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt
import os
import shutil

import predict


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'App'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.button = QPushButton('Select Image', self)
        self.button.setToolTip('Select an image')
        self.button.move(self.width / 2 - self.button.width() / 2, self.height / 3 - self.button.height() / 2)
        self.button.setStyleSheet("background-color: green;")
        self.button.clicked.connect(self.showDialog)

        self.browser_button = QPushButton('Open Browser', self)
        self.browser_button.setToolTip('Open Browser')
        self.browser_button.move(self.width / 2 - self.browser_button.width() / 2,
                                 self.height / 3 * 2 - self.browser_button.height() / 2)
        self.browser_button.setStyleSheet("background-color: blue;")
        self.browser_button.clicked.connect(self.open_browser)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, self.width - 20, self.height - 150)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px solid gray;")
        self.label.setText("No image selected")

        self.filename_label = QLabel(self)
        self.filename_label.setGeometry(10, self.height - 40, self.width - 20, 20)
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.filename_label.setStyleSheet("border: none; font-weight: bold;")
        self.filename_label.setText("No file selected")

        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.browser_button)
        vbox.addWidget(self.label)
        vbox.addWidget(self.filename_label)


        self.setLayout(vbox)

        self.show()

    def open_browser(self):
        import webbrowser
        url = 'https://www.google.com'
        webbrowser.open(url)

    def showDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Images (*.png *.xpm *.jpg *.bmp)')

        if fname:
            check_dir = 'check'
            if not os.path.exists(check_dir):
                os.makedirs(check_dir)

            shutil.copy(fname, os.path.join(check_dir, 'image.jpg'))

            result = predict.predict_single()
            result_string = "\n".join([f"{label}: {prob:.4f}" for label, prob in result])

            self.filename_label.setText(f'\n{result_string}')

            image = QImage(fname)
            pixmap = QPixmap.fromImage(image)

            self.label.setPixmap(
                pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.label.setText("")
            self.button.move(self.width / 2 - self.button.width() / 2, self.height / 2 - self.button.height() / 2)
        else:
            self.label.setText("No image selected")
            self.button.move(self.width / 2 - self.button.width() / 2, self.height / 3 - self.button.height() / 2)
            self.filename_label.setText("No file selected")

        self.filename_label.adjustSize()

        self.button.setStyleSheet("background-color: green;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
