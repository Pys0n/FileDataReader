import os, json

from format_readers.reader_class import Reader

class TSVReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.tsv', '.tab'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = ''
            table = []
            for line in file.readlines():
                text += line + '\n'
                table.append(line.split('\t'))

        file_extension = '.' + self.file_name.split('.')[-1]
        if file_extension not in ['.tsv', '.tab']:
            file_extension = '.tsv'
        
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': file_extension,
            'content': text[:-1],
            'table': table,
        }