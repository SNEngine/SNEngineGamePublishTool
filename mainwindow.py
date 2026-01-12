import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Применяем темные стили, совместимые с Qt5
        self.setStyleSheet("""
            QMainWindow {
                background: #1e1e1e;
                color: #ddd;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QPushButton {
                background: #d60000;
                color: white;
                border: none;
                padding: 12px 26px;
                font-size: 16px;
                border-radius: 6px;
                font-weight: 600;
                font-family: 'Roboto', Arial, sans-serif;
                min-width: 120px;
                text-align: center;
            }

            QPushButton:hover {
                background: #b10000;
            }
        """)

        # Устанавливаем иконку окна
        from PyQt5.QtGui import QIcon
        import os
        import sys
        if getattr(sys, 'frozen', False):
            # Если приложение запущено из EXE
            icon_path = os.path.join(sys._MEIPASS, 'icon.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        else:
            # Если приложение запущено из исходного кода
            if os.path.exists("icon.png"):
                self.setWindowIcon(QIcon("icon.png"))

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SNEngine Game Publisher")
        self.setGeometry(100, 100, 400, 300)
        self.center_window()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Open JSON button
        self.open_json_btn = QPushButton("Open JSON")
        self.open_json_btn.clicked.connect(self.open_json_file)
        layout.addWidget(self.open_json_btn)

        central_widget.setLayout(layout)

    def center_window(self):
        """Center the window on the screen"""
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_json_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open JSON File", "", "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    games = json.load(f)

                # Импортируем GameListWindow из другого файла
                from gamelist import GameListWindow
                self.list_window = GameListWindow(games, file_path)
                self.list_window.show()

                # Скрываем всё окно после успешной загрузки
                self.hide()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")


def main():
    app = QApplication(sys.argv)

    # Устанавливаем атрибуты приложения для правильного отображения иконки на панели задач в Windows
    if sys.platform == 'win32':  # Только для Windows
        import ctypes
        myappid = 'com.snengine.gamepublisher.1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()