import cv2
import os
import argparse
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser(description='Build a Python script that detects faces in an image using OpenCV, and saves the headshots of the detected faces to a specified directory.')

parser.add_argument('--input',help='a file path to an image to detect faces')

parser.add_argument('--output',default="/output",
                    help='a directory path to save the headshots')

# python problem1.py --input "faces.jpg" --output "output"
# If you run the command above without giving number argument the NUMBER_OF_FACES will be 5 as a default option.
parser.add_argument('--number',type=int,default=5,
                    help='number of faces to detect')

args = parser.parse_args()

# python problem1.py --input "faces.jpg" --output "output" --number 7
# For the command above the values:

IMAGE_PATH = args.input # "faces.jpg"
OUTPUT_DIR = args.output # "/output"
NUMBER_OF_FACES = args.number # 7

def clearDirectory(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def detect_and_save_faces(image_path, save_directory):
    """From a spesific image file it detects faces with opencv. 
    Then it crops the faces from that image and save them in a particular directory for the amount of time has given by the user.

    Parameters
    ----------
    image_path : string
        A file path to detect faces with the help of cv2 haarcascade.
    save_directory : string
        A directory to save cropped faces from input image.

    Returns
    -------
    Number
        The number of faces that has been cropped and saved to a directory.
    """
    _, file_extension = os.path.splitext(image_path)

    if file_extension.lower() in ('.jpeg', '.jpg', '.png', '.gif'):
        # Open the image using the Image.open() function
        with Image.open(image_path) as image:
            # Print the image mode and size
            print(f"Mode: {image.mode}")
            print(f"Size: {image.size}")
            # Load the cascade classifier
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            # Convert the image to a numpy array
            image_array = np.array(image)
            # Convert the image to RGB. If not converting then the cropped images will be saved in BGR format.
            image_array = cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

            # Detect faces in the image
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

            # Iterate through the faces and save each one to the specified directory
            headshot_count = 0
            for (x, y, w, h) in faces:
                headshot = image_array[y:y+h, x:x+w]
                headshot_path = os.path.join(save_directory, 'face_{}.jpg'.format(headshot_count+1))
                cv2.imwrite(headshot_path, headshot)
                headshot_count += 1
                if headshot_count >= NUMBER_OF_FACES:
                    break
            return headshot_count
    else:
        print(f"{file_extension} file format not supported")
        return 0
    

# Example usage
clearDirectory(OUTPUT_DIR) # We clear the directory to save new files everytime.
headshot_count = detect_and_save_faces(IMAGE_PATH, OUTPUT_DIR)
print('{} headshots saved to {}'.format(headshot_count, OUTPUT_DIR))