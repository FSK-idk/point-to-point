import configparser
import os
import sys


def resource_path(relative_path):
    try:
        return sys._MEIPASS + relative_path[1::]
    except Exception:
        return relative_path


class Config:
    def __init__(self):
        if not os.path.isdir(resource_path("./point_to_point/")): 
            os.mkdir(resource_path("./point_to_point/"))

        if not os.path.isdir(resource_path("./point_to_point/data/")): 
            os.mkdir(resource_path("./point_to_point/data/"))

        self.config = configparser.ConfigParser()
        self.filepath = resource_path("./point_to_point/data/config.ini")

        if not os.path.isfile(self.filepath):
            self.createConfig()
        
        self.config.read(self.filepath)

    def createConfig(self):
        self.config["Settings"] = {
            "Text": "Point to Point",
        }

        with open(self.filepath, 'w') as file:
            self.config.write(file)

    def __getitem__(self, index):
        return self.config[index]
    
    def items(self, section: str) -> list[tuple[str, str]]:
        return self.config.items(section)
    
    def write(self):
        with open(self.filepath, 'w') as file:
            self.config.write(file)


config = Config()
