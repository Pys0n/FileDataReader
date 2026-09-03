import os, json

from readers import *

class FileDataReader:
    def __init__(self, file: str, file_extension: str = None) -> None:
        if not isinstance(file, str):
            raise TypeError(f'Expected `file` to be a str, got {type(file).__name__}')
        if not os.path.isfile(file):
            raise ValueError(f'file "{file}" does not exist')
        if file_extension != None and not isinstance(file_extension, str):
            raise TypeError(f'Expected `file_extension` to be a str, got {type(file_extension).__name__}')
        
        self.file = file
        if file_extension != None:
            self.file_extension = file_extension if not file_extension.startswith('.') else file_extension[1:]
        else:
            self.file_extension = self.file.split('.')[-1]
        self._load_data()
    

    def get_data(self) -> dict:
        return self.data


    def to_json(self, file_name: str = None) -> None:
        if file_name == None:
            file_name = self.file + '.json'
        if not isinstance(file_name, str):
            raise TypeError(f'Expected `file_name` to be a str, got {type(file_name).__name__}')
        if not file_name.endswith('.json'):
            file_name += '.json'

        with open(file_name, 'w') as file:
            json.dump(self.data, file, indent=4)

    
    def _load_data(self) -> None:
        if self.file_extension in ['bmp', 'dib']:
            reader = BMPReader(self.file)
        elif self.file_extension in ['csv']:
            reader = CSVReader(self.file)
        elif self.file_extension in ['html', 'htm']:
            reader = HTMLReader(self.file)
        elif self.file_extension in ['ini']:
            reader = INIReader(self.file)
        elif self.file_extension in ['json']:
            reader = JSONReader(self.file)
        elif self.file_extension in ['psv']:
            reader = PSVReader(self.file)
        elif self.file_extension in ['ssv']:
            reader = SSVReader(self.file)
        elif self.file_extension in ['tsv', 'tab']:
            reader = TSVReader(self.file)
        elif self.file_extension in ['txt']:
            reader = TXTReader(self.file)
        elif self.file_extension in ['xml']:
            reader = XMLReader(self.file)
        else:
            raise ValueError(f'Unknown file format: {self.file_extension}')

        self.data = reader.get_data()