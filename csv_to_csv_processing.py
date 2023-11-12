import os
import pandas as pd

# Function to get full paths of all PNG files in a directory (including subdirectories)
def get_image_full_directory(directory):
    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Load the CSV file
root_directory = ""
csv_path = "MURA-v1.1/valid_labeled_studies.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_path, header=None)

# Assuming the 0th column has image paths and the 1st column has image classes
image_directory = df[0].tolist()
image_classes = df[1].tolist()

# Create an empty DataFrame
df_output = pd.DataFrame(columns=['image', 'class'])

# Loop through image directories
for i in range(0, len(image_directory)):
    png_files = get_image_full_directory(os.path.join(root_directory, image_directory[i]))

    # Append values to the DataFrame
    temp_df = pd.DataFrame({'image': png_files, 'class': image_classes[i]})
    df_output = pd.concat([df_output, temp_df], ignore_index=True)

    # Save the DataFrame to a CSV file after each iteration
    df_output.to_csv('output.csv', index=False)

# Display the final DataFrame
print(df_output)
