import os, json

from format_readers.reader_class import Reader

class MDReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.md', '.markdown'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        data = {
            'content': text,
        }

        self.data.update(data)
