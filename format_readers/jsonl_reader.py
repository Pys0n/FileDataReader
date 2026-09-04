import os, json

from format_readers.reader_class import Reader

class JSONLReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.ndjson', '.ldjson', '.jsonl'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        with open(self.file, 'r') as file:
            formated = []
            for line in text.split('\n'):
                formated.append(json.loads(line))
        
        file_extension = '.' + self.file_name.split('.')[-1]
        if file_extension not in ['.ndjson', '.ldjson', '.jsonl']:
            file_extension = '.jsonl'

        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': file_extension,
            'content': text,
            'formated': formated,
        }