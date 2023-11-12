#This code will read image path from a csv file and save images to a new directory. The directory name will be considered as class name of these images.
import os
import pandas as pd
import shutil
from PIL import Image
import torch
from torchvision import transforms

#function for saving images to its required directory
def save_image_to_directory(image_path, output_directory):
    # Check if the image path exists
    if not os.path.exists(image_path):
        print(f"Error: Image path '{image_path}' does not exist.")
        return
    
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get the base filename from the image path
    image_filename = os.path.basename(image_path)

    # Generate a unique filename in case of conflicts
    unique_filename = 1
    while os.path.exists(os.path.join(output_directory, f"{unique_filename}_{image_filename}")):
        unique_filename += 1

    # Build the destination path in the output directory
    destination_path = os.path.join(output_directory, f"{unique_filename}_{image_filename}")

    try:
        # Use PyTorch to load and preprocess the image
        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

        img = Image.open(image_path)
        img_tensor = preprocess(img)

        # Save the preprocessed image
        torch.save(img_tensor, destination_path)
        print(f"Image '{image_filename}' successfully saved to '{output_directory}'.")
    except Exception as e:
        print(f"Error: Unable to save image to '{output_directory}': {e}")
      
#function for reading image from csv file and setting up a conditon where the image directory will be stored!!
def process_csv(csv_file, output_directory):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    positive_dir = "positive/"
    negative_dir = "negative/"
    positive_des = os.path.join(output_directory, positive_dir)
    negative_des = os.path.join(output_directory, negative_dir)

    # Ensure the "image" column exists in the DataFrame
    if 'image' not in df.columns:
        print("Error: 'image' column not found in the CSV file.")
        return

    # Iterate through the rows and save each image to the output directory
    for index, row in df.iterrows():
        image_path = row['image']
        if row['class'] == 1:
            save_image_to_directory(image_path, positive_des)
        elif row['class'] == 0:
            save_image_to_directory(image_path, negative_des)
        else:
            print("Class mismatch")

# Example usage:
csv_file_path = "output.csv"
output_directory = "MURA/test/"
process_csv(csv_file_path, output_directory)
