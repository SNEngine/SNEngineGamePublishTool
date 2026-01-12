# SNEngine Game Publish Tool

SNEngine Game Publish Tool is an application for managing and publishing game information. The tool provides a convenient interface for viewing, editing, and exporting game data in JSON format.

## Features

- Opening JSON files with game information
- Viewing a list of games with platform icons
- Adding, editing, and deleting games
- Importing and exporting game data
- Multi-language support (EN/RU)
- Support for various platforms (Windows, macOS, Linux, Android, iOS, etc.)

## Requirements

- Python 3.6+
- PyQt5
- PyInstaller (for building executables)

## Installing Dependencies

```bash
pip install pyqt5 pyinstaller
```

## Project Structure

```
SNEngineGamePublishTool/
├── mainwindow.py          # Main application window
├── gamelist.py            # Game list window
├── mainwindow.spec        # PyInstaller configuration for main window
├── gamelist.spec          # PyInstaller configuration for game list
├── icon.png               # Application icon
├── games_platforms/       # Platform icons
│   ├── android.png
│   ├── browser.png
│   ├── ios.png
│   ├── linux.png
│   ├── macos.png
│   ├── nintendo_switch.png
│   └── playstation.png
└── README.md              # Documentation (this file)
```

## Building Executables

To create executable files, use the following commands:

### Main Window (SNEngineGamePublisher.exe)
```bash
pyinstaller mainwindow.spec
```

### Game List Window (GamePublisher.exe)
```bash
pyinstaller gamelist.spec
```

Files will be created in the `dist/` folder.

## Usage

1. Launch `SNEngineGamePublisher.exe`
2. Click "Open JSON" to load a file with game information
3. Use "Add Game", "Edit Game", "Delete Game" buttons to manage data
4. Use "Import Binary" to import data from a binary file
5. Use "Export JSON" to export all data to a JSON file

## Implementation Details

- The application uses a dark theme interface
- Platform icons are displayed in the game list
- Support for game statuses (released, in-development, pre-release, planned, cancelled, beta)
- Support for game preview images
- Multi-language support (EN/RU)

## Known Issues

- To correctly display icons in executables, `sys._MEIPASS` is used to access resources
- To correctly display the taskbar icon in Windows, `SetCurrentProcessExplicitAppUserModelID` is used

## License

The project is distributed without a license.