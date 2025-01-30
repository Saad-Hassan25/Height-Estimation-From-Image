# Height Estimation from Image with GUI

This project enables users to estimate their height based on an image uploaded from their mobile camera. The system uses the height of an object of known size as a reference to calculate the user's height. The project includes a GUI where users can interact with the system to upload their image and input reference data for height estimation.

## Features

- **Image Upload**: Users can upload an image of themselves taken with a mobile camera.
- **Reference Object for Scaling**: Users are required to input the height of a reference object (e.g., a known object in the image).
- **Height Calculation**: The program calculates the user's height based on the reference object using image processing techniques.
- **Graphical User Interface**: A GUI built using Python's Tkinter to guide the user through the process.

## Requirements

- Python 3.x
- Tkinter (for GUI)
- OpenCV (for image processing)
- Pillow (for image manipulation)
- NumPy (for numerical calculations)

To install the necessary dependencies, run:

```bash
pip install opencv-python tkinter pillow numpy
