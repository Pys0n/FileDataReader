import os, json

class SVGReader:
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        if not isinstance(file, str):
            raise TypeError(f'Expected `file` to be a str, got {type(file).__name__}')
        if not os.path.isfile(file):
            raise ValueError(f'file "{file}" does not exist')
        if not ignore_extension and (not file.endswith('.svg') and not file.endswith('.svgz')):
            raise ValueError(f'Expected `file` to be a .svg or .svgz, got {file.split('.')[-1]}')

        self.file = file
        self.file_name = file.replace('\\', '/').split('/')[-1]
        self._load_data()


    def get_content(self) -> str:
        return self.data['content']
    

    def get_data(self) -> dict:
        return self.data
    

    def to_json(self, file_name: str = None) -> None:
        if file_name == None:
            file_name = self.file + '.json'
        if not isinstance(file_name, str):
            raise TypeError(f'Expected `file_name` to be a str, got {type(file_name).__name__}')
        if not file_name.endswith('.json'):
            file_name += '.json'

        with open(file_name, 'w') as file:
            json.dump(self.data, file, indent=4)


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