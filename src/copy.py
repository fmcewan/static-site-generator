import os 
import shutil

def copy_directory(source, destination):
    
    working_directory = os.getcwd()
    possible_paths = os.listdir(path=working_directory)

    if source in possible_paths:
      
        if os.path.exists(working_directory+destination):
            shutil.rmtree(working_directory+destination)
        
        shutil.copytree(source, destination, copy_function=shutil.copy)

    else:
        raise ValueError("Source directory does not exist.")
