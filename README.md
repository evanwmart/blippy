# Blippy

Blippy is a lightweight webcam viewer application built with Python, Pygame, and OpenCV. It provides a simple interface to capture and display live video feed from your webcam, along with customizable reaction images and GIFs.

## Features

- Live webcam streaming
- Customizable reaction images and GIFs
- Toggleable window frame
- Fullscreen support
- Zoom functionality
- Keyboard shortcuts for easy navigation

## Installation

### Prerequisites

- Python 3.7+
- Pygame
- Pillow
- OpenCV

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blippy.git
   ```

2. Navigate to the project directory:
   ```
   cd blippy
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Build the executable:
   ```
   pyinstaller --onefile --windowed blippy.py
   ```

6. Move the generated executable to a location in your PATH:
   ```
   sudo mv dist/blippy /usr/local/bin/
   ```

## Usage

Run Blippy by executing:
```
blippy
```

Use the following keyboard shortcuts:
- Space: Toggle window frame
- F: Toggle fullscreen
- Q, W, E: Select reaction images
- A, S, D: Select reaction GIFs
- 1-9: Select numbered reactions
- ESC: Quit the application

## Development Environment Setup

To set up a development environment:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blippy.git
   ```

2. Install Python and necessary libraries:
   ```
   sudo pacman -S python python-pygame python-pillow python-opencv
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the application:
   ```
   python blippy.py
   ```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
