import os, json

from format_readers.reader_class import Reader

class SVGReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.svg', '.svgz'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
            declaration = text.split('\n')[0]

        file_extension = '.' + self.file_name.split('.')[-1]
        if file_extension not in ['.svg', '.svgz']:
            file_extension = '.svg'
        
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': file_extension,
            'content': {
                'content': text,
            },
        }

        if not '?xml' in declaration:
            self.data['declaration'] = None
            self.data['xml-version'] = None
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
                
                if attribute == 'version':
                    self.data['xml-' + attribute] = val
                else:
                    self.data[attribute] = val
        
        svg = False
        for line in text.split('\n')[1:]:
            if '<svg' in line:
                svg = True
            if '>' in line:
                svg = False
            
            if svg and not line.startswith('<!--') and '=' in line:
                line = line.strip()
                key = line.split('=')[0]
                val = '='.join(line.split('=')[1:])

                self.data['content'][key] = val[1:-1] if val.startswith('"') or val.startswith('\'') else val