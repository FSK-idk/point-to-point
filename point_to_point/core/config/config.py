from typing import List, Tuple
import configparser
import os


class Config:
    def __init__(self):
        if not os.path.isdir("./point_to_point/data/"): 
            os.mkdir("./point_to_point/data/")

        self.config = configparser.ConfigParser()
        self.filepath = "./point_to_point/data/config.ini"

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
    
    def items(self, section: str) -> List[Tuple[str, str]]:
        return self.config.items(section)
    
    def write(self):
        with open(self.filepath, 'w') as file:
            self.config.write(file)


config = Config()
