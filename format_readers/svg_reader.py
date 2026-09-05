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


        data = {
            'content': {
                'content': text,
            },
        }

        if not '?xml' in declaration:
            data['declaration'] = None
            data['xml-version'] = None
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
                
                if attribute == 'version':
                    data['xml-' + attribute] = val
                else:
                    data[attribute] = val
        
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

                data['content'][key] = val[1:-1] if val.startswith('"') or val.startswith('\'') else val

        self.data.update(data)
