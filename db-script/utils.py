from datetime import datetime

def create_folder_name():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")