
# Blippy

Blippy is a simple-made application that allows users to display reaction images and GIFs with various keyboard shortcuts. It is built using Python and leverages libraries: Pygame, Pillow, and OpenCV.

## Installation

### Prerequisites

- Python 3.7+
- Pygame
- Pillow
- OpenCV

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/evanwmart/blippy.git
   ```

2. Navigate to the project directory:
   ```
   cd blippy
   ```

3. For macOS/Linux users, check if the setup script exists:
   ```
   ls | grep setup_blippy.sh
   ```
   If the script exists, proceed to step 4. Otherwise, continue with manual setup.

4. If the setup script exists, run it (macOS/Linux only):
   ```
   ./setup_blippy.sh
   ```
   If not, skip to step 5.

5. Create and activate a virtual environment:
   - On macOS/Linux:
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```
     python -m venv .venv
     .\venv\Scripts\activate
     ```

6. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

7. Build the executable:
   ```
   pyinstaller --onefile --windowed blippy.py
   ```

8. Move the generated executable to a location in your PATH:
   - On macOS/Linux:
     ```
     sudo mv dist/blippy /usr/local/bin/
     ```
   - On Windows:
     ```
     move dist\blippy.exe %APPDATA%\Microsoft\Windows\Start Menu\Programs\Blippy.lnk
     ```

## Usage

Run Blippy by executing:
```
blippy
```

Use the following keyboard shortcuts:
- Space: Toggle window frame
- F: Toggle fullscreen
- Q, W, E, A, S, D: Select reaction images
- Z, X, C: Select reaction GIFs
- 0-9: Select versatile reactions
- ESC: Quit the application

Before running Blippy, make sure to have a ```reactions/``` folder in the same directory as the executable. You can use the default/example reactions.zip file to test this, but feel free to replace images with the naming scheme: ```X.png``` or ```X.gif``` where X represents the toggle key (see above for the 19 key options).

To unzip the file:
1. Extract the contents of ```reactions.zip``` to a folder named ```reactions```.
2. Place the extracted ```reactions``` folder next to the ```blippy``` executable.

After setting up the reactions folder correctly, run Blippy as usual:

```
blippy
```

Now you should be able to use the reaction images and GIFs in Blippy!

## Development Environment Setup

To set up a development environment:

1. Clone the repository:
   ```
   git clone https://github.com/evanwmart/blippy.git
   ```

2. Install Python and necessary libraries:
   - On macOS/Linux:
     ```
     sudo pacman -S python python-pygame python-pillow python-opencv
     ```
   - On Windows:
     ```
     pip install pygame pillow opencv-python
     ```

3. Create and activate a virtual environment:
   - On macOS/Linux:
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```
     python -m venv .venv
     .\venv\Scripts\activate
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
