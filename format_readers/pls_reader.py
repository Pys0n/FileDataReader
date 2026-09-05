import os, json

from format_readers.reader_class import Reader

class PLSReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.pls'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        data = {
            'content': {
                'content': text,
            },
        }

        for line in text.split('\n'):
            if '=' in line:
                key = line.split('=')[0]
                val = '='.join(line.split('=')[1:])

                data['content'][key] = val


        self.data.update(data)
