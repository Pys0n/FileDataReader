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
        
        data = {
            'content': text,
            'formated': formated,
        }

        self.data.update(data)
