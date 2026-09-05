import os, json

from format_readers.reader_class import Reader

class INIReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.ini'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        data = {
            'content': {
                'content': text,
            },
        }

        cached = ''
        current_section = None
        for line in text.split('\n'):
            line = line.strip()

            if len(line) == 0:
                continue

            elif line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                data['content'][current_section] = {}
            
            elif line.endswith('\\'):
                cached += line[:-1].strip()
            
            elif line.startswith(';') or line.startswith('#'):
                continue

            elif '=' in line:
                key = line.split('=')[0].strip()
                value = '='.join(line.split('=')[1:]).strip().split(' ;')[0].split(' #')[0].replace('"', '').replace('\'', '')

                if current_section == None:
                    data['content'][key] = value
                else:
                    data['content'][current_section][key] = value
                
        self.data.update(data)
    