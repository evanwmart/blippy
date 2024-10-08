from typing import List, Optional, Tuple
from pathlib import Path
from PIL import Image
import numpy as np
import pygame
import time
import sys
import cv2
import os
import ctypes
import subprocess

# Function to set the window always on top for Windows
def set_window_always_on_top_windows():
    hwnd = pygame.display.get_wm_info()['window']
    SetWindowPos = ctypes.windll.user32.SetWindowPos
    SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

# Function to set the window always on top for macOS
def set_window_always_on_top_macos():
    from AppKit import NSApplication, NSApp, NSWindow
    app = NSApplication.sharedApplication()
    app.activateIgnoringOtherApps_(True)
    window = NSApp.windows()[0]
    window.setLevel_(NSWindow.LevelFloating)

# Function to set the window always on top for Linux (GNOME)
def set_window_always_on_top_linux():
    window_id = pygame.display.get_wm_info()['window']
    subprocess.call(['wmctrl', '-i', '-r', str(window_id), '-b', 'add,above'])

# Function to set the window always on top based on the OS
def set_window_always_on_top():
    if sys.platform.startswith('win'):
        set_window_always_on_top_windows()
    elif sys.platform.startswith('darwin'):
        set_window_always_on_top_macos()
    elif sys.platform.startswith('linux'):
        set_window_always_on_top_linux()

# Function to reset the window to normal state for Linux (GNOME)
def reset_window_normal_state_linux():
    window_id = pygame.display.get_wm_info()['window']
    subprocess.call(['wmctrl', '-i', '-r', str(window_id), '-b', 'remove,above'])

# Function to set window transparency on Linux
def set_window_transparency_linux(opacity: float):
    window_id = pygame.display.get_wm_info()['window']
    opacity_value = int(opacity * 0xFFFFFFFF)
    subprocess.call(['xprop', '-id', str(window_id), '-f', '_NET_WM_WINDOW_OPACITY', '32c', '-set', '_NET_WM_WINDOW_OPACITY', str(opacity_value)])

def load_gif(gif_path: str) -> List[Image.Image]:
    """
    Load a GIF file and return its frames.
    
    Args:
        gif_path (str): Path to the GIF file
    
    Returns:
        List[Image.Image]: A list of PIL Image objects representing the GIF frames
    """
    try:
        gif = Image.open(gif_path)
        frames: List[Image.Image] = []
        while True:
            frame = gif.copy()
            frame = frame.convert("RGBA")
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        print(f"Error loading GIF: {e}")
    return frames

def load_webp(webp_path: str) -> pygame.Surface:
    """
    Load a WebP file and return it as a Pygame surface.
    
    Args:
        webp_path (str): Path to the WebP file
    
    Returns:
        pygame.Surface: A Pygame surface representing the WebP image
    """
    try:
        image = Image.open(webp_path)
        image = image.convert("RGBA")
        mode = image.mode
        size = image.size
        data = image.tobytes()
        return pygame.image.fromstring(data, size, mode)
    except Exception as e:
        print(f"Error loading WebP: {e}")
        return None

def react_to_key(key: int) -> Tuple[Optional[pygame.Surface], Optional[float], Optional[list], Optional[list], Optional[float]]:
    """
    Return reaction image and time to display it based on key press.
    
    Args:
        key (int): The key that was pressed

    Returns:
        Tuple[Optional[pygame.Surface], Optional[float], Optional[list], Optional[list], Optional[float]]: 
        A tuple containing the reaction image, the time to display it, gif frames, gif surfaces, and gif time.
    """
    image_source = None
    image_time = None
    gif_surfaces = None
    gif_time = None

    # Define the reactions folder as a fixed path
    if sys.platform.startswith("win"):
        reactions_folder = Path("reactions")
    else:
        reactions_folder = Path("/usr/local/bin/reactions")

    file_name = str(reactions_folder / key)
    png_file = f'{file_name}.png'
    gif_file = f'{file_name}.gif'
    webp_file = f'{file_name}.webp'

    try:
        if os.path.exists(png_file):
            image_source = pygame.image.load(png_file)
            image_time = time.time()
        elif os.path.exists(gif_file):
            gif_frames = load_gif(gif_file)
            gif_surfaces = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) for frame in gif_frames]
            gif_time = time.time()
        elif os.path.exists(webp_file):
            image_source = load_webp(webp_file)
            image_time = time.time()
        else:
            raise FileNotFoundError(f"File not found: {png_file}, {gif_file}, or {webp_file}")
    except FileNotFoundError as e:
        print(e)
    except pygame.error as e:
        print(f"Error loading image with Pygame: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return image_source, image_time, gif_surfaces, gif_time

def main() -> None:
    print("\033[106m----------------------------\033[0m")
    print("\n\033[1m\033[94mBlippy\033[0m")
    print("\033[96mJust a little webcam viewer\033[0m\n")
    print("\033[1m\033[94mInstructions:\033[0m")
    print("\033[94m\u2009Space\033[0m\033[96m\ttoggle window frame")
    print("\033[94m\u2009\u2009\u2009\u2009\u2009F\033[0m\033[96m\ttoggle fullscreen\n")
    print("\033[94m\u2009\u2009\u2009\u2009\u2009Reactions:\033[0m")
    print("\033[94m\u2009\u2009\u2009\u2009\u2009Q, W, E\033[0m")
    print("\033[94m\u2009\u2009\u2009\u2009\u2009A, S, D\033[0m")
    print("\033[94m\u2009\u2009\u2009\u2009\u2009Z, X, C\033[0m")
    print("\033[94m\u2009\u2009\u2009\u2009\u20090 - 9\033[0m")
    print("\033[96mName image as x.png or x.gif in folder 'reactions'\n")
    print("\033[94m\u2009\u2009\u2009ESC\033[0m\033[96m\tquit\n")
    print("\033[106m----------------------------\033[0m")

    # Define the reactions folder as a fixed path
    if sys.platform.startswith("win"):
        reactions_folder = Path("reactions")
    else:
        reactions_folder = Path("/usr/local/bin/reactions")
    if not os.path.exists(reactions_folder):
        current_directory = os.getcwd()
        print(f"\033[1;31m{'Folder not found:'}\033[0m {reactions_folder}")
        print(f"\033[1;33m{'Please create the folder at:'}\033[0m {current_directory}")
        print(f"\033[1;33m{'Add some images to it.'}\033[0m")
        return
    
    # Show found images
    images = [f for f in os.listdir(reactions_folder) if os.path.isfile(os.path.join(reactions_folder, f))]
    if len(images) == 0:
        print(f"\033[91mNo images found in folder '{reactions_folder}'!\033[0m")
        print("\033[93mPlease add some images to it.\033[0m")
        return
    print(f"\033[1;32mFound images in folder '{reactions_folder}':\033[0m")
    for image in images:
        print(f"\033[1;34m• {image}\033[0m")
    print("\n")

    # Initialize Pygame
    pygame.init()

    # Variables to track window state
    always_on_top = False
    window_frame_visible = True

    # Set up display without title bar
    width, height = 500, 500
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Blippy")
    green = (0, 255, 0)

    # Capture video from webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("\033[91mError: Could not open webcam\033[0m")
        return

    # Variables to handle zoom
    zoom_level = 1.0
    zoom_step = 0.1

    circle_view = False
    window_transparency = 1

    image_source: Optional[pygame.Surface] = None
    image_time: Optional[float] = None

    gif_surfaces: Optional[List[pygame.Surface]] = None
    gif_time: Optional[float] = None

    frame_index = 0
    clock = pygame.time.Clock()

    while True:
        # Capture frame from camera
        ret, frame = cap.read()
        if not ret:
            print("\033[91mError: Could not read camera frame\033[0m")
            break

        # Get the window dimensions
        width, height = pygame.display.get_surface().get_size()

        # Get frame dimensions
        frame_height, frame_width, _ = frame.shape

        # Ensure zoom level is within bounds
        zoom_level = max(1.0, min(zoom_level, 5))

        # Apply zoom
        zoomed_width = int(frame_width / zoom_level)
        zoomed_height = int(frame_height / zoom_level)
        x_start = (frame_width - zoomed_width) // 2
        y_start = (frame_height - zoomed_height) // 2
        zoomed_frame = frame[y_start:y_start + zoomed_height, x_start:x_start + zoomed_width]

        # Resize frame to maintain aspect ratio
        if width > height:
            ratio = width / height
            new_frame_width = zoomed_width
            new_frame_height = int(new_frame_width / ratio)
            height_a = int((zoomed_height - new_frame_height) / 2)
            height_b = height_a + new_frame_height
            resized_frame = zoomed_frame[height_a:height_b, :]
        else:
            ratio = height / width
            new_frame_height = zoomed_height
            new_frame_width = int(new_frame_height / ratio)
            width_a = int((zoomed_width - new_frame_width) / 2)
            width_b = width_a + new_frame_width
            resized_frame = zoomed_frame[:, width_a:width_b]

        # Convert to RGB and handle potential empty frame
        if resized_frame.size != 0:
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            surface = pygame.surfarray.make_surface(rgb_frame)
            surface = pygame.transform.rotate(surface, -90)

            # Scale the frame to fit the screen
            resized_surface = pygame.transform.scale(surface, (width, height))

        # If circle view is enabled, create a circular mask
        if circle_view:
            # Create a blank surface with per-pixel alpha
            backdrop = pygame.Surface((width, height), pygame.SRCALPHA)

            # Fill the surface with a transparent background
            screen.fill((0, 0, 0, 0))

            backdrop.fill((0, 0, 0, 0))

            # Draw a white circle on the transparent surface
            pygame.draw.circle(backdrop, (255, 255, 255), (width // 2, height // 2), height // 2, 0)

            # Blit the frame onto the transparent surface blend based on white color (max)
            backdrop.blit(resized_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # Blit the backdrop onto the screen
            screen.blit(backdrop, (0, 0))
        else:  
            screen.blit(resized_surface, (0, 0))


            # Handle image display
            if image_time is not None and time.time() - image_time <= 5:
                span = min(width, height) // 3
                image_scaled = pygame.transform.scale(image_source, (span, span))
                screen.blit(image_scaled, (width - span, 0))

            # Handle GIF display
            if gif_time is not None and time.time() - gif_time <= 5:
                gif_surface = gif_surfaces[frame_index % len(gif_surfaces)]

                span = min(width, height) // 2

                new_width = span
                new_height = span

                if gif_surface.get_width() > gif_surface.get_height():
                    scale = span / gif_surface.get_width()
                    new_height = (int(gif_surface.get_height() * scale))
                    new_width = span
                else:
                    scale = span / gif_surface.get_height()
                    new_width = (int(gif_surface.get_width() * scale))
                    new_height = span

                gif_surface = pygame.transform.scale(gif_surface, (new_width, new_height))
                screen.blit(gif_surface, (width - span, 0))
                frame_index += 1
                clock.tick(30)  # Limit to 30 FPS


        # Update the entire screen
        pygame.display.flip()

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_SPACE:
                    window_frame_visible = not window_frame_visible
                    pygame.display.set_caption("Blippy" if window_frame_visible else "")
                    pygame.display.flip()
                    if not window_frame_visible:
                        pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.NOFRAME)
                    else:
                        pygame.display.set_mode((width, height), pygame.RESIZABLE)
                        # Reset window to normal state 
                        if sys.platform.startswith('win'):
                            hwnd = pygame.display.get_wm_info()['window']
                            SetWindowPos = ctypes.windll.user32.SetWindowPos
                            SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)
                        elif sys.platform.startswith('linux'):
                            reset_window_normal_state_linux()
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    zoom_level = min(zoom_level + zoom_step, 5)
                elif event.key == pygame.K_DOWN:
                    zoom_level = max(zoom_level - zoom_step, 1.0)
                elif event.key == pygame.K_LEFT:
                    window_transparency = max(window_transparency - 0.1, 0.1)
                    window_id = pygame.display.get_wm_info()['window']
                    opacity_value = int(window_transparency * 0xFFFFFFFF)
                    subprocess.call(['xprop', '-id', str(window_id), '-f', '_NET_WM_WINDOW_OPACITY', '32c', '-set', '_NET_WM_WINDOW_OPACITY', str(opacity_value)])
                elif event.key == pygame.K_RIGHT:
                    window_transparency = min(window_transparency + 0.1, 1.0)
                    window_id = pygame.display.get_wm_info()['window']
                    opacity_value = int(window_transparency * 0xFFFFFFFF)
                    subprocess.call(['xprop', '-id', str(window_id), '-f', '_NET_WM_WINDOW_OPACITY', '32c', '-set', '_NET_WM_WINDOW_OPACITY', str(opacity_value)])
                elif event.key == pygame.K_o:
                    zoom_level = 1.0
                elif event.key == pygame.K_i:
                    zoom_level = 5.0
                elif event.key == pygame.K_q:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('q')
                elif event.key == pygame.K_w:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('w')
                elif event.key == pygame.K_e:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('e')
                elif event.key == pygame.K_a:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('a')
                elif event.key == pygame.K_s:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('s')
                elif event.key == pygame.K_d:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('d')
                elif event.key == pygame.K_z:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('z')
                elif event.key == pygame.K_x:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('x')
                elif event.key == pygame.K_c:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('c')
                elif event.key == pygame.K_1:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('1')
                elif event.key == pygame.K_2:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('2')
                elif event.key == pygame.K_3:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('3')
                elif event.key == pygame.K_4:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('4')
                elif event.key == pygame.K_5:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('5')
                elif event.key == pygame.K_6:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('6')
                elif event.key == pygame.K_7:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('7')
                elif event.key == pygame.K_8:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('8')
                elif event.key == pygame.K_9:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('9')
                elif event.key == pygame.K_0:
                    image_source, image_time, gif_surfaces, gif_time = react_to_key('0')
                elif event.key == pygame.K_t:
                    always_on_top = not always_on_top
                    window_frame_visible = False
                    if always_on_top:
                        pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.NOFRAME)
                        set_window_always_on_top()
                    else:
                        # Reset window to normal state
                        if sys.platform.startswith('win'):
                            hwnd = pygame.display.get_wm_info()['window']
                            SetWindowPos = ctypes.windll.user32.SetWindowPos
                            SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)
                        elif sys.platform.startswith('linux'):
                            reset_window_normal_state_linux()
                elif event.key == pygame.K_u:
                    circle_view = not circle_view

if __name__ == "__main__":
    main()
