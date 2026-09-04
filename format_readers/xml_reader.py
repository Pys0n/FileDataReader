import os, json

from format_readers.reader_class import Reader

class XMLReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.xml'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
            declaration = text.split('\n')[0]
        
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': '.xml',
            'content': text,
        }

        if not '?xml' in declaration:
            self.data['declaration'] = None
            self.data['version'] = None
            self.data['encoding'] = None
            self.data['standalone'] = None
        else:
            self.data['declaration'] = declaration

            dec = declaration.replace(' ', '').replace('\'', '"')
            for attribute in ['version', 'encoding', 'standalone']:
                if attribute not in declaration:
                    self.data[attribute] = None
                    continue
                d = dec.split(attribute+'="')
                val = ''
                for x in d[1]:
                    if x == '"':
                        break
                    val += x
                
                self.data[attribute] = val