import sys
import json
import pickle
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QMessageBox, QListWidget, QHBoxLayout, QDialog,
    QLabel, QLineEdit, QTextEdit, QFormLayout, QComboBox, QListWidgetItem,
    QListWidget, QAbstractItemView, QScrollArea, QCheckBox
)
from PyQt5.QtGui import QFontDatabase
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
                font-family: 'Roboto';
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
                        font-family: 'Roboto';
                    }
                """)
                platforms_layout.addWidget(platform_label)

        info_layout.addLayout(platforms_layout)

        layout.addLayout(info_layout)
        layout.addStretch()

        self.setLayout(layout)


class GameListWindow(QMainWindow):
    def __init__(self, games=None, file_path=None):
        super().__init__()
        self.games = games if games is not None else []
        self.file_path = file_path if file_path is not None else ""

        # Save to session if a file path is provided
        if self.file_path:
            set_last_opened_file(self.file_path)
        # Применяем темные стили, совместимые с Qt5
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ddd;
                font-family: 'Roboto';
            }

            QPushButton {
                background-color: #d60000;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 16px;
                border-radius: 6px;
                font-weight: 600;
                font-family: 'Roboto';
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
                font-family: 'Roboto';
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
                font-family: 'Roboto';
            }

            QLabel {
                font-family: 'Roboto';
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
                # Если иконка не найдена в ресурсах EXE, пробуем найти рядом с EXE
                exe_dir = os.path.dirname(sys.executable)
                fallback_icon_path = os.path.join(exe_dir, 'icon.png')
                if os.path.exists(fallback_icon_path):
                    self.setWindowIcon(QIcon(fallback_icon_path))
        else:
            # Если приложение запущено из исходного кода
            if os.path.exists("icon.png"):
                self.setWindowIcon(QIcon("icon.png"))

        self.init_ui()

    def init_ui(self):
        title = f"Games List - {self.file_path}" if self.file_path else "Games List"
        self.setWindowTitle(title)

        # Проверяем, была ли уже восстановлена геометрия из сессии
        session_data = get_session_data()
        if 'window_geometry' in session_data:
            # Если геометрия была сохранена в сессии, восстанавливаем её
            self.restore_window_state()
        else:
            # Если геометрия не была восстановлена, устанавливаем стандартные размеры
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
                font-family: 'Roboto';
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

        import_btn = QPushButton("Import ZIP")
        import_btn.clicked.connect(self.import_game)
        button_layout.addWidget(import_btn)

        export_games_btn = QPushButton("Export Games")
        export_games_btn.clicked.connect(self.export_games_json)
        button_layout.addWidget(export_games_btn)

        import_games_btn = QPushButton("Import Games")
        import_games_btn.clicked.connect(self.import_games_json)
        button_layout.addWidget(import_games_btn)

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
                font-family: 'Roboto';
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
        else:
            # If no valid game is selected, clear the details panel
            self.clear_details_panel()

    def show_game_details(self, game):
        """Display detailed information about the selected game"""
        # Clear the right panel
        self.clear_details_panel()

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
                font-family: 'Roboto';
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
                    font-family: 'Roboto';
                    margin: 3px 5px;
                }
            """
        elif status == 'in-development':
            status_style = """
                QLabel {
                    color: #3498db;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto';
                    margin: 3px 5px;
                }
            """
        elif status == 'pre-release':
            status_style = """
                QLabel {
                    color: #f1c40f;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto';
                    margin: 3px 5px;
                }
            """
        elif status == 'planned':
            status_style = """
                QLabel {
                    color: #9b59b6;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto';
                    margin: 3px 5px;
                }
            """
        elif status == 'cancelled':
            status_style = """
                QLabel {
                    color: #e74c3c;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto';
                    margin: 3px 5px;
                }
            """
        elif status == 'beta':
            status_style = """
                QLabel {
                    color: #f39c12;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto';
                    margin: 3px 5px;
                }
            """
        else:
            status_style = """
                QLabel {
                    color: #aaa;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Roboto';
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
                    font-family: 'Roboto';
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
                            font-family: 'Roboto';
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
                        font-family: 'Roboto';
                        margin: 5px;
                    }
                """)
                scroll_layout.addWidget(preview_placeholder)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        # Add the scroll area to the right panel
        self.right_panel.layout().addWidget(scroll_area)

    def clear_details_panel(self):
        """Clear the details panel and show the placeholder message"""
        # Check if right_panel exists before trying to access it
        if hasattr(self, 'right_panel') and self.right_panel.layout():
            # Clear the right panel
            for i in reversed(range(self.right_panel.layout().count())):
                self.right_panel.layout().itemAt(i).widget().setParent(None)

            # Add the placeholder label back
            self.details_label = QLabel("Select a game to view details")
            self.details_label.setAlignment(Qt.AlignCenter)
            self.details_label.setStyleSheet("""
                QLabel {
                    color: #aaa;
                    font-size: 14px;
                    font-family: 'Roboto';
                }
            """)
            self.right_panel.layout().addWidget(self.details_label)

    def restore_window_state(self):
        """Restore window geometry from session"""
        session_data = get_session_data()
        if 'window_geometry' in session_data:
            try:
                geometry = session_data['window_geometry']
                if isinstance(geometry, list):
                    # Convert list back to bytes
                    geometry_bytes = bytes(geometry)
                    self.restoreGeometry(geometry_bytes)
            except Exception as e:
                print(f"Could not restore window geometry: {str(e)}")

    def save_window_state(self):
        """Save window geometry to session"""
        session_data = get_session_data()
        session_data['window_geometry'] = list(self.saveGeometry().data())
        set_session_data(session_data)

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

        # Если список игр пуст, очистить панель деталей (только если right_panel уже существует)
        if not self.games and hasattr(self, 'right_panel'):
            self.clear_details_panel()

    def closeEvent(self, event):
        """Save window state before closing"""
        self.save_window_state()
        event.accept()

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

            # Check if preview image has changed and delete the old one
            old_preview = game.get('preview', '')
            new_preview = updated_game.get('preview', '')

            self.games[current_row] = updated_game
            self.save_games()
            self.populate_games_list()

            # Delete the old preview image if it exists and it's different from the new one
            if old_preview and new_preview and old_preview != new_preview and old_preview.startswith('images/'):
                import os
                # Construct the full path to the old image file
                if self.file_path:
                    json_dir = os.path.dirname(self.file_path)
                    full_image_path = os.path.join(json_dir, old_preview)
                else:
                    # Try to get the last opened file from session
                    last_file = get_last_opened_file()
                    if last_file and os.path.exists(last_file):
                        json_dir = os.path.dirname(last_file)
                        full_image_path = os.path.join(json_dir, old_preview)
                    else:
                        # Use current directory as fallback
                        full_image_path = old_preview

                # Delete the old image file if it exists
                if os.path.exists(full_image_path):
                    try:
                        os.remove(full_image_path)
                        print(f"Deleted old preview image: {full_image_path}")
                    except Exception as e:
                        print(f"Could not delete old preview image {full_image_path}: {str(e)}")

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
            # Get the preview image path before deleting the game
            preview_path = game.get('preview', '')

            # Delete the game
            del self.games[current_row]
            self.save_games()
            self.populate_games_list()
            # Clear the details panel after deletion
            self.clear_details_panel()

            # Delete the preview image from the images folder if it exists
            if preview_path and preview_path.startswith('images/'):
                import os
                # Construct the full path to the image file
                if self.file_path:
                    json_dir = os.path.dirname(self.file_path)
                    full_image_path = os.path.join(json_dir, preview_path)
                else:
                    # Try to get the last opened file from session
                    last_file = get_last_opened_file()
                    if last_file and os.path.exists(last_file):
                        json_dir = os.path.dirname(last_file)
                        full_image_path = os.path.join(json_dir, preview_path)
                    else:
                        # Use current directory as fallback
                        full_image_path = preview_path

                # Delete the image file if it exists
                if os.path.exists(full_image_path):
                    try:
                        os.remove(full_image_path)
                        print(f"Deleted preview image: {full_image_path}")
                    except Exception as e:
                        print(f"Could not delete preview image {full_image_path}: {str(e)}")

    def import_game(self):
        """Import a game from a binary file or ZIP archive"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Game Data", "", "Game Files (*.zip *.bin);;ZIP Files (*.zip);;Binary Files (*.bin);;All Files (*)"
        )

        if file_path:
            try:
                import zipfile
                import pickle
                import os
                from datetime import datetime

                # Check if it's a ZIP file
                if file_path.lower().endswith('.zip'):
                    # Get the parent window to access the current JSON file path
                    parent_window = self.parent()
                    # Use the current JSON file path from the parent window
                    if parent_window and hasattr(parent_window, 'file_path') and parent_window.file_path:
                        json_dir = os.path.dirname(parent_window.file_path)
                        images_dir = os.path.join(json_dir, "images")
                    else:
                        # If no JSON file is currently loaded in parent, try to get the last opened file from session
                        last_file = get_last_opened_file()
                        if last_file and os.path.exists(last_file):
                            json_dir = os.path.dirname(last_file)
                            images_dir = os.path.join(json_dir, "images")
                        else:
                            # If no file path is available, use the current working directory
                            images_dir = "images"

                    with zipfile.ZipFile(file_path, 'r') as zipf:
                        # Extract game data
                        bin_data = zipf.read('gamedata.bin')
                        game_data = pickle.loads(bin_data)

                        # Look for image files in the ZIP
                        image_files = [f for f in zipf.namelist() if f != 'gamedata.bin' and any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp'])]

                        if image_files:
                            # Create images folder if it doesn't exist
                            if not os.path.exists(images_dir):
                                os.makedirs(images_dir)

                            # Extract the first image file found
                            image_name = image_files[0]
                            image_data = zipf.read(image_name)

                            # Generate a unique filename to avoid conflicts
                            name, ext = os.path.splitext(image_name)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            unique_filename = f"{name}_{timestamp}{ext}"
                            destination_path = os.path.join(images_dir, unique_filename)

                            # Write the image to the images folder
                            with open(destination_path, 'wb') as img_file:
                                img_file.write(image_data)

                            # Update the preview path in the game data to be relative to JSON file location
                            game_data['preview'] = f"images/{unique_filename}"
                        else:
                            # If no image files found in ZIP, check if game_data already has a preview path
                            # and if so, try to copy it to the images folder
                            preview_path = game_data.get('preview', '')
                            if preview_path and os.path.exists(preview_path):
                                # Create images folder if it doesn't exist
                                if not os.path.exists(images_dir):
                                    os.makedirs(images_dir)

                                # Generate a unique filename to avoid conflicts
                                original_filename = os.path.basename(preview_path)
                                name, ext = os.path.splitext(original_filename)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                                unique_filename = f"{name}_{timestamp}{ext}"
                                destination_path = os.path.join(images_dir, unique_filename)

                                # Copy the image to the images folder
                                import shutil
                                shutil.copy2(preview_path, destination_path)

                                # Update the preview path in the game data to be relative to JSON file location
                                game_data['preview'] = f"images/{unique_filename}"
                else:
                    # Handle legacy binary file import
                    with open(file_path, 'rb') as f:
                        game_data = pickle.load(f)

                    # If the preview path exists and points to an image file, copy it to images folder
                    preview_path = game_data.get('preview', '')
                    if preview_path and os.path.exists(preview_path):
                        # Determine where to create the images folder based on parent window's file path
                        parent_window = self.parent()
                        if parent_window and hasattr(parent_window, 'file_path') and parent_window.file_path:
                            json_dir = os.path.dirname(parent_window.file_path)
                            images_dir = os.path.join(json_dir, "images")
                        else:
                            # If no JSON file is currently loaded in parent, try to get the last opened file from session
                            last_file = get_last_opened_file()
                            if last_file and os.path.exists(last_file):
                                json_dir = os.path.dirname(last_file)
                                images_dir = os.path.join(json_dir, "images")
                            else:
                                # If no file path is available, use the current working directory
                                images_dir = "images"

                        # Create images folder if it doesn't exist
                        if not os.path.exists(images_dir):
                            os.makedirs(images_dir)

                        # Generate a unique filename to avoid conflicts
                        original_filename = os.path.basename(preview_path)
                        name, ext = os.path.splitext(original_filename)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        unique_filename = f"{name}_{timestamp}{ext}"
                        destination_path = os.path.join(images_dir, unique_filename)

                        # Copy the image to the images folder
                        import shutil
                        shutil.copy2(preview_path, destination_path)

                        # Update the preview path in the game data to be relative to JSON file location
                        game_data['preview'] = f"images/{unique_filename}"

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
        """Export all games to a file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Games", self.file_path or "games.json", "Game Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.games, f, ensure_ascii=False, indent=2)

                # If we exported to the current file, update the window title and session
                if file_path == self.file_path:
                    self.update_window_title()
                    set_last_opened_file(self.file_path)

                QMessageBox.information(self, "Success", "Games exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export games:\n{str(e)}")

    def import_games_json(self):
        """Import games from a JSON file or ZIP archive"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Games", "", "Game Files (*.json *.zip);;JSON Files (*.json);;ZIP Files (*.zip);;All Files (*)"
        )

        if file_path:
            try:
                import zipfile
                import pickle
                import os
                from datetime import datetime

                # Check if it's a ZIP file
                if file_path.lower().endswith('.zip'):
                    imported_games = []

                    # Use the current JSON file path from this window
                    if self.file_path:
                        json_dir = os.path.dirname(self.file_path)
                        images_dir = os.path.join(json_dir, "images")
                    else:
                        # If no JSON file is currently loaded in this window, try to get the last opened file from session
                        last_file = get_last_opened_file()
                        if last_file and os.path.exists(last_file):
                            json_dir = os.path.dirname(last_file)
                            images_dir = os.path.join(json_dir, "images")
                        else:
                            # If no file path is available, use the current working directory
                            images_dir = "images"

                    with zipfile.ZipFile(file_path, 'r') as zipf:
                        # Look for JSON files or game data in the ZIP
                        json_files = [f for f in zipf.namelist() if f.endswith('.json')]

                        if json_files:
                            # If there are JSON files, import from the first one
                            json_content = zipf.read(json_files[0])
                            imported_games = json.loads(json_content.decode('utf-8'))

                            # If the imported data is a single game object, wrap it in a list
                            if isinstance(imported_games, dict):
                                imported_games = [imported_games]
                        else:
                            # Look for binary game data files
                            bin_files = [f for f in zipf.namelist() if f.endswith('.bin')]

                            if bin_files:
                                # Import from binary file
                                bin_content = zipf.read(bin_files[0])
                                game_data = pickle.loads(bin_content)

                                # Look for image files in the ZIP to handle preview
                                image_files = [f for f in zipf.namelist() if f != bin_files[0] and any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp'])]

                                if image_files:
                                    # Create images folder relative to the JSON file location
                                    if not os.path.exists(images_dir):
                                        os.makedirs(images_dir)

                                    # Extract the first image file found
                                    image_name = image_files[0]
                                    image_data = zipf.read(image_name)

                                    # Generate a unique filename to avoid conflicts
                                    name, ext = os.path.splitext(image_name)
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                                    unique_filename = f"{name}_{timestamp}{ext}"
                                    destination_path = os.path.join(images_dir, unique_filename)

                                    # Write the image to the images folder
                                    with open(destination_path, 'wb') as img_file:
                                        img_file.write(image_data)

                                    # Update the preview path in the game data to be relative to JSON file location
                                    game_data['preview'] = f"images/{unique_filename}"
                                else:
                                    # If no image files found in ZIP, check if game_data already has a preview path
                                    # and if so, try to copy it to the images folder
                                    preview_path = game_data.get('preview', '')
                                    if preview_path and os.path.exists(preview_path):
                                        # Create images folder relative to the JSON file location
                                        if not os.path.exists(images_dir):
                                            os.makedirs(images_dir)

                                        # Generate a unique filename to avoid conflicts
                                        original_filename = os.path.basename(preview_path)
                                        name, ext = os.path.splitext(original_filename)
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                                        unique_filename = f"{name}_{timestamp}{ext}"
                                        destination_path = os.path.join(images_dir, unique_filename)

                                        # Copy the image to the images folder
                                        import shutil
                                        shutil.copy2(preview_path, destination_path)

                                        # Update the preview path in the game data to be relative to JSON file location
                                        game_data['preview'] = f"images/{unique_filename}"

                                imported_games = [game_data]
                            else:
                                raise ValueError("No supported game data files found in the ZIP archive")
                else:
                    # Handle JSON file import
                    with open(file_path, 'r', encoding='utf-8') as f:
                        imported_games = json.load(f)

                    # Validate that the imported data is a list of games
                    if not isinstance(imported_games, list):
                        # If it's a single game object, wrap it in a list
                        if isinstance(imported_games, dict):
                            imported_games = [imported_games]
                        else:
                            raise ValueError("JSON file must contain an array of games or a single game object")

                # If the current list is empty, just replace without asking
                if not self.games:
                    # Replace the games
                    self.games = imported_games
                    self.file_path = file_path
                    self.update_window_title()  # Update window title when replacing
                    set_last_opened_file(self.file_path)  # Save to session when replacing
                else:
                    # Ask user if they want to merge or replace
                    reply = QMessageBox.question(
                        self, "Import Option",
                        "Do you want to merge the imported games with the current list?\n(Select No to replace current games)",
                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                    )

                    if reply == QMessageBox.Yes:
                        # Merge the games
                        # Generate new IDs for imported games to avoid conflicts
                        max_id = max([g.get('id', 0) for g in self.games])

                        for game in imported_games:
                            max_id += 1
                            game['id'] = max_id

                        self.games.extend(imported_games)
                    elif reply == QMessageBox.No:
                        # Replace the games
                        self.games = imported_games
                        self.file_path = file_path
                        self.update_window_title()  # Update window title when replacing
                        set_last_opened_file(self.file_path)  # Save to session when replacing
                    elif reply == QMessageBox.Cancel:
                        return

                # Handle preview images for imported games (if they exist outside images/ folder)
                for game in self.games:
                    preview_path = game.get('preview', '')
                    if preview_path and os.path.exists(preview_path) and not preview_path.startswith('images/'):
                        # Create images folder relative to the JSON file location
                        if self.file_path:
                            json_dir = os.path.dirname(self.file_path)
                            images_dir = os.path.join(json_dir, "images")
                        else:
                            # If no JSON file is currently loaded in this window, try to get the last opened file from session
                            last_file = get_last_opened_file()
                            if last_file and os.path.exists(last_file):
                                json_dir = os.path.dirname(last_file)
                                images_dir = os.path.join(json_dir, "images")
                            else:
                                # If no file path is available, use the current working directory
                                images_dir = "images"

                        if not os.path.exists(images_dir):
                            os.makedirs(images_dir)

                        # Generate a unique filename to avoid conflicts
                        original_filename = os.path.basename(preview_path)
                        name, ext = os.path.splitext(original_filename)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        unique_filename = f"{name}_{timestamp}{ext}"
                        destination_path = os.path.join(images_dir, unique_filename)

                        # Copy the image to the images folder
                        import shutil
                        shutil.copy2(preview_path, destination_path)

                        # Update the preview path in the game data to be relative to JSON file
                        game['preview'] = f"images/{unique_filename}"

                self.save_games()
                self.populate_games_list()
                QMessageBox.information(self, "Success", f"Successfully imported {len(imported_games)} games!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import games:\n{str(e)}")

    def save_games(self):
        try:
            if not self.file_path:
                # If no file path is set, ask user to save as new file
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Save Games", "games.json", "Game Files (*.json);;All Files (*)"
                )

                if file_path:
                    self.file_path = file_path
                else:
                    # User cancelled, don't save
                    return

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.games, f, ensure_ascii=False, indent=2)

            # Update window title after saving
            self.update_window_title()

            # Save to session
            set_last_opened_file(self.file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def update_window_title(self):
        """Update the window title to reflect the current file path"""
        title = f"Games List - {self.file_path}" if self.file_path else "Games List"
        self.setWindowTitle(title)


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
                font-family: 'Roboto';
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #2d2d2d;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Roboto';
            }

            QLabel {
                color: #ddd;
                font-family: 'Roboto';
            }

            QCheckBox {
                color: #ddd;
                font-family: 'Roboto';
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
                # Если иконка не найдена в ресурсах EXE, пробуем найти рядом с EXE
                exe_dir = os.path.dirname(sys.executable)
                fallback_icon_path = os.path.join(exe_dir, 'icon.png')
                if os.path.exists(fallback_icon_path):
                    self.setWindowIcon(QIcon(fallback_icon_path))
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
            import os
            import shutil
            from datetime import datetime

            # Determine where to create the images folder based on parent window's file path
            parent_window = self.parent()
            if parent_window and hasattr(parent_window, 'file_path') and parent_window.file_path:
                json_dir = os.path.dirname(parent_window.file_path)
                images_dir = os.path.join(json_dir, "images")
            else:
                # If no JSON file is currently loaded in parent, try to get the last opened file from session
                last_file = get_last_opened_file()
                if last_file and os.path.exists(last_file):
                    json_dir = os.path.dirname(last_file)
                    images_dir = os.path.join(json_dir, "images")
                else:
                    # If no file path is available, use the current working directory
                    images_dir = "images"

            # Create images folder if it doesn't exist
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)

            # Get the filename from the selected path
            original_filename = os.path.basename(file_path)
            name, ext = os.path.splitext(original_filename)

            # Generate a unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            unique_filename = f"{name}_{timestamp}{ext}"
            destination_path = os.path.join(images_dir, unique_filename)

            # Copy the image to the images folder
            shutil.copy2(file_path, destination_path)

            # Set the preview input to the relative path starting with "images/"
            relative_path = f"images/{unique_filename}"
            self.preview_input.setText(relative_path)

    def export_game(self):
        """Export the current game data as a ZIP archive containing binary and preview image"""
        import pickle
        import zipfile
        import os
        from datetime import datetime

        game_data = self.get_game_data()

        # Ask user for ZIP file location
        zip_path, _ = QFileDialog.getSaveFileName(
            self, "Export Game Data as ZIP", "", "ZIP Files (*.zip);;All Files (*)"
        )

        if zip_path:
            try:
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    # Add the game data as a binary file
                    bin_data = pickle.dumps(game_data)
                    zipf.writestr('gamedata.bin', bin_data)

                    # Add the preview image if it exists
                    preview_path = game_data.get('preview', '')
                    if preview_path and os.path.exists(preview_path):
                        zipf.write(preview_path, os.path.basename(preview_path))

                QMessageBox.information(self, "Success", "Game data exported as ZIP successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export game data as ZIP:\n{str(e)}")

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


def load_fonts():
    """Load custom fonts from the fonts directory"""
    try:
        # Define the fonts directory path
        if getattr(sys, 'frozen', False):
            # If running as compiled executable
            fonts_dir = os.path.join(sys._MEIPASS, 'fonts')
        else:
            # If running from source
            fonts_dir = os.path.join(os.getcwd(), 'fonts')

        if os.path.exists(fonts_dir):
            for font_file in os.listdir(fonts_dir):
                if font_file.lower().endswith(('.ttf', '.otf')):
                    font_path = os.path.join(fonts_dir, font_file)
                    QFontDatabase.addApplicationFont(font_path)
    except Exception as e:
        print(f"Could not load fonts: {str(e)}")


def main():
    app = QApplication(sys.argv)

    # Load custom fonts
    load_fonts()

    # Устанавливаем атрибуты приложения для правильного отображения иконки на панели задач в Windows
    if sys.platform == 'win32':  # Только для Windows
        import ctypes
        myappid = 'com.snengine.gamepublisher.1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Try to load the last opened file from session
    last_file_path = get_last_opened_file()

    if last_file_path and os.path.exists(last_file_path):
        try:
            with open(last_file_path, 'r', encoding='utf-8') as f:
                games = json.load(f)

            window = GameListWindow(games, last_file_path)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load last file:\n{str(e)}")
            # Start with empty list if file loading fails
            window = GameListWindow([], "")
    else:
        # Start with empty list if no last file or it doesn't exist
        window = GameListWindow([], "")

    window.show()
    sys.exit(app.exec_())


def get_session_file_path():
    """Get the path to the session file"""
    # If running as compiled executable, store session next to the EXE
    if getattr(sys, 'frozen', False):
        # If running as compiled executable
        exe_dir = os.path.dirname(sys.executable)
        session_dir = exe_dir
    else:
        # If running from source, store in current directory
        session_dir = os.getcwd()

    # Create directory if it doesn't exist
    os.makedirs(session_dir, exist_ok=True)

    return os.path.join(session_dir, 'session.json')


def get_session_data():
    """Get the session data from file"""
    session_file = get_session_file_path()
    if os.path.exists(session_file):
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def set_session_data(session_data):
    """Set the session data to file"""
    session_file = get_session_file_path()
    try:
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save session: {str(e)}")  # Just print error, don't interrupt user


def get_last_opened_file():
    """Get the last opened file path from session"""
    session_data = get_session_data()
    return session_data.get('last_opened_file', '')


def set_last_opened_file(file_path):
    """Set the last opened file path in session"""
    session_data = get_session_data()
    session_data['last_opened_file'] = file_path
    set_session_data(session_data)


if __name__ == "__main__":
    main()