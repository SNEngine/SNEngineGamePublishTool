import sys
import json
import pickle
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QMessageBox, QListWidget, QHBoxLayout, QDialog,
    QLabel, QLineEdit, QTextEdit, QFormLayout, QComboBox, QListWidgetItem,
    QListWidget, QAbstractItemView, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon


class PlatformIconWidget(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)

        # Game info
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignVCenter)

        # Game title
        title_label = QLabel(f"{self.game.get('id', 'N/A')} - {self.game.get('name', {}).get('en', 'No name')}")

        # Добавляем статус к названию
        status = self.game.get('status', 'Unknown')
        if status == 'released':
            status_indicator = "●"
            status_color = "#2ecc71"
        elif status == 'in-development':
            status_indicator = "○"
            status_color = "#3498db"
        elif status == 'pre-release':
            status_indicator = "○"
            status_color = "#f1c40f"
        elif status == 'planned':
            status_indicator = "○"
            status_color = "#9b59b6"
        elif status == 'cancelled':
            status_indicator = "○"
            status_color = "#e74c3c"
        elif status == 'beta':
            status_indicator = "○"
            status_color = "#f39c12"
        else:
            status_indicator = "○"
            status_color = "#aaa"

        title_with_status = f"{status_indicator} {self.game.get('id', 'N/A')} - {self.game.get('name', {}).get('en', 'No name')}"
        title_label = QLabel(title_with_status)

        title_label.setStyleSheet(f"""
            QLabel {{
                color: #ddd;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }}
        """)
        info_layout.addWidget(title_label)

        # Platforms
        platforms_layout = QHBoxLayout()
        platforms_layout.setAlignment(Qt.AlignLeft)
        platforms = self.game.get('platforms', [])

        for platform in platforms:
            import os
            import sys
            if getattr(sys, 'frozen', False):
                # Если приложение запущено из EXE
                icon_path = os.path.join(sys._MEIPASS, 'games_platforms', f"{platform.lower()}.png")
            else:
                # Если приложение запущено из исходного кода
                icon_path = f"games_platforms/{platform.lower()}.png"

            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    # Scale the image to fit
                    pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    platform_icon = QLabel()
                    platform_icon.setPixmap(pixmap)
                    platform_icon.setMaximumSize(64, 64)
                    platform_icon.setToolTip(platform.upper())
                    platforms_layout.addWidget(platform_icon)
                else:
                    # Если не удалось загрузить изображение, показываем текст
                    platform_label = QLabel(f"[{platform.upper()}]")
                    platform_label.setStyleSheet("""
                        QLabel {
                            color: #aaa;
                            font-size: 12px;
                            background: transparent;
                            padding: 2px 4px;
                        }
                    """)
                    platforms_layout.addWidget(platform_label)
            else:
                # Если файл не существует, показываем текст
                platform_label = QLabel(f"[{platform.upper()}]")
                platform_label.setStyleSheet("""
                    QLabel {
                        color: #aaa;
                        font-size: 12px;
                        background: transparent;
                        padding: 2px 4px;
                    }
                """)
                platforms_layout.addWidget(platform_label)

        info_layout.addLayout(platforms_layout)

        layout.addLayout(info_layout)
        layout.addStretch()

        self.setLayout(layout)


class GameListWindow(QMainWindow):
    def __init__(self, games, file_path):
        super().__init__()
        self.games = games
        self.file_path = file_path
        # Применяем темные стили, совместимые с Qt5
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ddd;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QPushButton {
                background-color: #d60000;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 16px;
                border-radius: 6px;
                font-weight: 600;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QPushButton:hover {
                background-color: #b10000;
            }

            QListWidget {
                background-color: #2d2d2d;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
            }

            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QListWidget::item:selected {
                background-color: #d60000;
                color: white;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #2d2d2d;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QLabel {
                font-family: 'Roboto', Arial, sans-serif;
                color: #ddd;
            }

            QMessageBox {
                background-color: #1e1e1e;
                color: #ddd;
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
        self.setWindowTitle(f"Games List - {self.file_path}")
        self.setGeometry(200, 200, 1000, 700)
        self.center_window()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()

        # Left sidebar for game list
        left_sidebar = QWidget()
        left_sidebar.setFixedWidth(350)
        left_sidebar.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-right: 1px solid #444;
            }
        """)
        left_layout = QVBoxLayout()

        # Title for the left panel
        left_title = QLabel("Games")
        font = QFont("Roboto", 16, QFont.Bold)
        left_title.setFont(font)
        left_title.setStyleSheet("""
            QLabel {
                color: #d60000;
                font-family: 'Roboto', Arial, sans-serif;
                padding: 10px;
                border-bottom: 1px solid rgba(214, 0, 0, 0.2);
            }
        """)
        left_layout.addWidget(left_title)

        # List of games
        self.games_list = QListWidget()
        self.populate_games_list()
        self.games_list.itemSelectionChanged.connect(self.on_game_selected)  # Connect selection change
        left_layout.addWidget(self.games_list)

        # Add buttons to left panel
        button_layout = QVBoxLayout()  # Change to vertical layout to accommodate more buttons

        add_btn = QPushButton("Add Game")
        add_btn.clicked.connect(self.add_game)
        button_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit Game")
        edit_btn.clicked.connect(self.edit_game)
        button_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete Game")
        delete_btn.clicked.connect(self.delete_game)
        button_layout.addWidget(delete_btn)

        import_btn = QPushButton("Import Binary")
        import_btn.clicked.connect(self.import_game)
        button_layout.addWidget(import_btn)

        export_json_btn = QPushButton("Export JSON")
        export_json_btn.clicked.connect(self.export_games_json)
        button_layout.addWidget(export_json_btn)

        left_layout.addLayout(button_layout)
        left_sidebar.setLayout(left_layout)

        # Right panel for details
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        right_layout = QVBoxLayout()

        # Placeholder for game details
        self.details_label = QLabel("Select a game to view details")
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 14px;
                font-family: 'Roboto', Arial, sans-serif;
            }
        """)
        right_layout.addWidget(self.details_label)

        self.right_panel.setLayout(right_layout)

        # Add panels to main layout
        layout.addWidget(left_sidebar)
        layout.addWidget(self.right_panel)

        central_widget.setLayout(layout)

    def center_window(self):
        """Center the window on the screen"""
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_game_selected(self):
        """Handle game selection and display details"""
        current_row = self.games_list.currentRow()
        if current_row >= 0 and current_row < len(self.games):
            game = self.games[current_row]
            self.show_game_details(game)

    def show_game_details(self, game):
        """Display detailed information about the selected game"""
        # Clear the right panel
        for i in reversed(range(self.right_panel.layout().count())):
            self.right_panel.layout().itemAt(i).widget().setParent(None)

        # Create a scroll area for the details
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QWidget {
                background: transparent;
            }
        """)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        # Game title
        title_label = QLabel(f"{game.get('name', {}).get('en', 'No name')}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #ddd;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Roboto', Arial, sans-serif;
                margin: 5px;
            }
        """)
        scroll_layout.addWidget(title_label)

        # Game status
        status = game.get('status', 'Unknown')
        status_label = QLabel(f"Status: {status}")

        # Установка стиля в зависимости от статуса
        if status == 'released':
            status_style = """
                QLabel {
                    color: #2ecc71;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """
        elif status == 'in-development':
            status_style = """
                QLabel {
                    color: #3498db;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """
        elif status == 'pre-release':
            status_style = """
                QLabel {
                    color: #f1c40f;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """
        elif status == 'planned':
            status_style = """
                QLabel {
                    color: #9b59b6;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """
        elif status == 'cancelled':
            status_style = """
                QLabel {
                    color: #e74c3c;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """
        elif status == 'beta':
            status_style = """
                QLabel {
                    color: #f39c12;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """
        else:
            status_style = """
                QLabel {
                    color: #aaa;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 3px 5px;
                }
            """

        status_label.setStyleSheet(status_style)
        scroll_layout.addWidget(status_label)

        # Description (English)
        desc_en = game.get('description', {}).get('en', 'No description')
        if desc_en:
            desc_label = QLabel(f"Description: {desc_en}")
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("""
                QLabel {
                    color: #ddd;
                    font-size: 14px;
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 5px;
                }
            """)
            scroll_layout.addWidget(desc_label)

        # Preview image
        preview_path = game.get('preview', '')
        if preview_path:
            try:
                import os
                # Сначала проверяем абсолютный путь
                if os.path.exists(preview_path):
                    pixmap = QPixmap(preview_path)
                else:
                    # Если файл не найден по абсолютному пути, ищем относительно файла JSON
                    json_dir = os.path.dirname(self.file_path)
                    relative_path = os.path.join(json_dir, preview_path)
                    if os.path.exists(relative_path):
                        pixmap = QPixmap(relative_path)
                    else:
                        # Если и относительный путь не найден, показываем ошибку
                        pixmap = None

                if pixmap and not pixmap.isNull():
                    # Scale the image to fit
                    scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    preview_label = QLabel()
                    preview_label.setPixmap(scaled_pixmap)
                    preview_label.setAlignment(Qt.AlignCenter)
                    preview_label.setStyleSheet("""
                        QLabel {
                            border: 1px solid #444;
                            margin: 5px;
                        }
                    """)
                    scroll_layout.addWidget(preview_label)
                else:
                    # If image loading fails, show a placeholder
                    preview_placeholder = QLabel("Preview image not found")
                    preview_placeholder.setAlignment(Qt.AlignCenter)
                    preview_placeholder.setStyleSheet("""
                        QLabel {
                            color: #aaa;
                            font-size: 12px;
                            font-family: 'Roboto', Arial, sans-serif;
                            margin: 5px;
                        }
                    """)
                    scroll_layout.addWidget(preview_placeholder)
            except Exception as e:
                # If image loading fails, show a placeholder
                preview_placeholder = QLabel(f"Preview image error: {str(e)}")
                preview_placeholder.setAlignment(Qt.AlignCenter)
                preview_placeholder.setStyleSheet("""
                    QLabel {
                        color: #aaa;
                        font-size: 12px;
                        font-family: 'Roboto', Arial, sans-serif;
                        margin: 5px;
                    }
                """)
                scroll_layout.addWidget(preview_placeholder)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        # Add the scroll area to the right panel
        self.right_panel.layout().addWidget(scroll_area)

    def populate_games_list(self):
        self.games_list.clear()
        for game in self.games:
            # Создаем виджет для элемента списка
            widget = PlatformIconWidget(game, self)

            # Создаем элемент списка
            item = QListWidgetItem()

            # Устанавливаем высоту элемента в соответствии с высотой виджета
            item.setSizeHint(widget.sizeHint())

            # Добавляем виджет в список
            self.games_list.addItem(item)
            self.games_list.setItemWidget(item, widget)

    def add_game(self):
        dialog = GameEditDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            new_game = dialog.get_game_data()
            # Генерируем новый ID
            if self.games:
                new_id = max([g.get('id', 0) for g in self.games]) + 1
            else:
                new_id = 1
            new_game['id'] = new_id
            self.games.append(new_game)
            self.save_games()
            self.populate_games_list()

    def edit_game(self):
        current_row = self.games_list.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "Information", "Please select a game to edit")
            return

        game = self.games[current_row]
        dialog = GameEditDialog(game_data=game, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            updated_game = dialog.get_game_data()
            # Сохраняем ID оригинальной игры
            updated_game['id'] = game['id']
            self.games[current_row] = updated_game
            self.save_games()
            self.populate_games_list()

    def delete_game(self):
        current_row = self.games_list.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "Information", "Please select a game to delete")
            return

        game = self.games[current_row]
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Are you sure you want to delete the game '{game.get('name', {}).get('en', 'N/A')}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            del self.games[current_row]
            self.save_games()
            self.populate_games_list()

    def import_game(self):
        """Import a game from a binary file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Game Data", "", "Binary Files (*.bin);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    game_data = pickle.load(f)

                # Добавляем ID к импортированной игре
                if self.games:
                    new_id = max([g.get('id', 0) for g in self.games]) + 1
                else:
                    new_id = 1
                game_data['id'] = new_id

                self.games.append(game_data)
                self.save_games()
                self.populate_games_list()

                QMessageBox.information(self, "Success", "Game data imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import game data:\n{str(e)}")

    def export_games_json(self):
        """Export all games to a JSON file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Games JSON", "games.json", "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.games, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "Success", "Games exported to JSON successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export games to JSON:\n{str(e)}")

    def save_games(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.games, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")


class PlatformSelector(QWidget):
    def __init__(self, selected_platforms=None, parent=None):
        super().__init__(parent)
        self.selected_platforms = selected_platforms or []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Available platforms
        self.platforms = ['windows', 'macos', 'linux', 'android', 'ios', 'xbox', 'playstation', 'nintendo_switch', 'browser']

        # Create checkboxes for each platform
        self.checkboxes = {}
        for platform in self.platforms:
            checkbox = QCheckBox(platform.upper())
            checkbox.setChecked(platform in self.selected_platforms)
            self.checkboxes[platform] = checkbox
            layout.addWidget(checkbox)

        self.setLayout(layout)

    def get_selected_platforms(self):
        selected = []
        for platform, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected.append(platform)
        return selected


class GameEditDialog(QDialog):
    def __init__(self, game_data=None, parent=None):
        super().__init__(parent)
        self.game_data = game_data or {}
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ddd;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #2d2d2d;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QLabel {
                color: #ddd;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QCheckBox {
                color: #ddd;
                font-family: 'Roboto', Arial, sans-serif;
            }

            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }

            QScrollArea > QWidget {
                background-color: #1e1e1e;
            }

            QScrollArea > QWidget > QWidget {
                background-color: #1e1e1e;
            }

            QMessageBox {
                background-color: #1e1e1e;
                color: #ddd;
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

        self.center_dialog()
        self.init_ui()

    def center_dialog(self):
        """Center the dialog on the screen"""
        # Получаем геометрию главного окна
        main_window = self.parent()
        if main_window:
            # Центрируем относительно родительского окна
            parent_geometry = main_window.frameGeometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        else:
            # Если нет родителя, центрируем на экране
            qr = self.frameGeometry()
            cp = self.screen().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def init_ui(self):
        self.setWindowTitle("Edit Game" if self.game_data else "Add New Game")
        self.setGeometry(300, 300, 500, 700)

        layout = QVBoxLayout()

        # Scroll area for form
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        form_layout = QFormLayout()

        # ID field
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        if self.game_data.get('id'):
            self.id_input.setText(str(self.game_data['id']))
        form_layout.addRow("ID:", self.id_input)

        # Name fields
        self.name_en_input = QLineEdit()
        if self.game_data.get('name'):
            self.name_en_input.setText(self.game_data['name'].get('en', ''))
        form_layout.addRow("Name (EN):", self.name_en_input)

        self.name_ru_input = QLineEdit()
        if self.game_data.get('name'):
            self.name_ru_input.setText(self.game_data['name'].get('ru', ''))
        form_layout.addRow("Name (RU):", self.name_ru_input)

        # Description fields
        self.desc_en_input = QTextEdit()
        if self.game_data.get('description'):
            self.desc_en_input.setPlainText(self.game_data['description'].get('en', ''))
        form_layout.addRow("Description (EN):", self.desc_en_input)

        self.desc_ru_input = QTextEdit()
        if self.game_data.get('description'):
            self.desc_ru_input.setPlainText(self.game_data['description'].get('ru', ''))
        form_layout.addRow("Description (RU):", self.desc_ru_input)

        # Preview path
        preview_layout = QHBoxLayout()
        self.preview_input = QLineEdit()
        if self.game_data.get('preview'):
            self.preview_input.setText(self.game_data['preview'])
        preview_button = QPushButton("Browse...")
        preview_button.clicked.connect(self.browse_preview)
        preview_layout.addWidget(self.preview_input)
        preview_layout.addWidget(preview_button)
        form_layout.addRow("Preview Path:", preview_layout)

        # Platform selector
        selected_platforms = self.game_data.get('platforms', [])
        self.platform_selector = PlatformSelector(selected_platforms, self)
        form_layout.addRow("Platforms:", self.platform_selector)

        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["released", "in-development", "pre-release", "planned", "cancelled", "beta"])
        if self.game_data.get('status'):
            index = self.status_combo.findText(self.game_data['status'])
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
            else:
                # Если статус не найден в новом списке, добавляем его как опцию
                self.status_combo.addItem(self.game_data['status'])
                index = self.status_combo.findText(self.game_data['status'])
                if index >= 0:
                    self.status_combo.setCurrentIndex(index)
        form_layout.addRow("Status:", self.status_combo)

        # Download URL
        self.url_input = QLineEdit()
        if self.game_data.get('downloadUrl'):
            self.url_input.setText(self.game_data['downloadUrl'])
        form_layout.addRow("Download URL:", self.url_input)

        scroll_content.setLayout(form_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)

        # Buttons
        button_layout = QHBoxLayout()
        from PyQt5.QtWidgets import QDialogButtonBox
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Export button
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_game)
        button_layout.addWidget(export_button)
        button_layout.addWidget(button_box)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def browse_preview(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "", "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            # Пытаемся получить относительный путь от директории JSON файла
            try:
                import os
                json_dir = os.path.dirname(self.parent().file_path)  # Получаем директорию JSON файла
                relative_path = os.path.relpath(file_path, json_dir)
                # Заменяем обратные слэши на прямые для JSON
                relative_path = relative_path.replace('\\', '/')
                self.preview_input.setText(relative_path)
            except:
                # Если не удалось получить относительный путь, используем абсолютный
                # Заменяем обратные слэши на прямые для JSON
                file_path = file_path.replace('\\', '/')
                self.preview_input.setText(file_path)

    def export_game(self):
        """Export the current game data to a binary file"""
        import pickle
        game_data = self.get_game_data()

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Game Data", "", "Binary Files (*.bin);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(game_data, f)
                QMessageBox.information(self, "Success", "Game data exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export game data:\n{str(e)}")

    def get_game_data(self):
        return {
            "name": {
                "en": self.name_en_input.text(),
                "ru": self.name_ru_input.text()
            },
            "description": {
                "en": self.desc_en_input.toPlainText(),
                "ru": self.desc_ru_input.toPlainText()
            },
            "preview": self.preview_input.text(),
            "platforms": self.platform_selector.get_selected_platforms(),
            "status": self.status_combo.currentText(),
            "downloadUrl": self.url_input.text()
        }


def main():
    app = QApplication(sys.argv)

    # Устанавливаем атрибуты приложения для правильного отображения иконки на панели задач в Windows
    if sys.platform == 'win32':  # Только для Windows
        import ctypes
        myappid = 'com.snengine.gamepublisher.1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = GameListWindow([], "games.json")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()