import os

def traverse_and_read_files(directory):
    for root, dirs, files in os.walk(directory):
        print(f"Current directory: {root}")
        for dir_name in dirs:
            print(f"Subdirectory: {dir_name}")
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"File: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    print(f"Contents of {file_name}:")
                    print(file.read())
                    print('-' * 40)  # Separator for clarity
            except Exception as e:
                print(f"Could not read {file_name}: {e}")

# Replace 'your_directory_path' with the path to the directory you want to traverse
traverse_and_read_files('templates')
