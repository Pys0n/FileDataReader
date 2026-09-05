import os, json

from format_readers.reader_class import Reader

class JSONReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.json'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        with open(self.file, 'r') as file:
            json_formated = json.load(file)
        
        data = {
            'content': text,
            'formated': json_formated,
        }

        self.data.update(data)
