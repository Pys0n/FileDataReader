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
        
        data = {
            'content': text,
        }

        if not '?xml' in declaration:
            data['declaration'] = None
            data['version'] = None
            data['encoding'] = None
            data['standalone'] = None
        else:
            data['declaration'] = declaration

            dec = declaration.replace(' ', '').replace('\'', '"')
            for attribute in ['version', 'encoding', 'standalone']:
                if attribute not in declaration:
                    data[attribute] = None
                    continue
                d = dec.split(attribute+'="')
                val = ''
                for x in d[1]:
                    if x == '"':
                        break
                    val += x
                
                data[attribute] = val

        self.data.update(data)
