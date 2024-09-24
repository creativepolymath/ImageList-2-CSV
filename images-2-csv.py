import os
import csv
from datetime import datetime

def images_to_csv(folder_path, output_csv):
    """
    Create a CSV file containing information about all images in a specified folder.

    This function walks through the given folder and its subfolders, identifies image files
    based on their extensions, collects relevant information about each image, and writes
    this information to a CSV file.

    Parameters:
    folder_path (str): The path to the folder containing the images.
    output_csv (str): The name of the output CSV file.

    Returns:
    None

    Side effects:
    - Creates a CSV file with the specified name in the current working directory.
    - Prints confirmation messages to the console.
    """
    # List of common image file extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    # List to store image information
    images = []
    
    # Check if the provided folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file has an image extension
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(root, file)
                file_stats = os.stat(file_path)
                
                # Collect image information
                image_info = {
                    'filename': file,
                    'path': file_path,
                    'size_bytes': file_stats.st_size,
                    'last_modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Add the image information to the list
                images.append(image_info)
    
    # Check if any images were found
    if not images:
        print(f"No images found in the folder: {folder_path}")
        return

    # Write the collected information to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        # Define the CSV columns
        fieldnames = ['filename', 'path', 'size_bytes', 'last_modified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        # Write a row for each image
        for image in images:
            writer.writerow(image)
    
    # Print confirmation messages
    print(f"CSV file created: {output_csv}")
    print(f"Total images found: {len(images)}")

# Example usage
if __name__ == "__main__":
    # Get user input for the folder path and output CSV filename
    folder_path = input("Enter the path to the image folder: ")
    output_csv = input("Enter the name for the output CSV file (e.g., image_list.csv): ")
    
    # Call the function to create the CSV
    images_to_csv(folder_path, output_csv)