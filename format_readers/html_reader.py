import os, json

class HTMLReader:
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        if not isinstance(file, str):
            raise TypeError(f'Expected `file` to be a str, got {type(file).__name__}')
        if not os.path.isfile(file):
            raise ValueError(f'file "{file}" does not exist')
        if not ignore_extension and not file.endswith('.html'):
            raise ValueError(f'Expected `file` to be a .html, got {file.split('.')[-1]}')

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
            splited = text.split('>')
            doctype = splited[0] + '>'
        
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': '.html',
            'content': text,
            'DOCTYPE': doctype,
        }
    
        for value in splited:
            if 'lang' in value:
                value = value.replace(' ', '').replace('\'', '"')

                if 'lang="' not in value:
                    continue

                self.data['lang'] = value.split('lang="')[1].split('"')[0]
            if '<meta' in value:
                value = value.strip()[6:].strip().replace(' ', '').replace('\'', '"')
                if 'name="' in value and 'content="' in value:
                    self.data[value.split('name="')[1].split('"')[0]] = value.split('content="')[1].split('"')[0]
                elif 'http-equiv="' in value and 'content="' in value:
                    self.data[value.split('http-equiv="')[1].split('"')[0]] = value.split('content="')[1].split('"')[0]
                elif 'property="' in value and 'content="' in value:
                    self.data[value.split('property="')[1].split('"')[0]] = value.split('content="')[1].split('"')[0]
            elif '</title' in value:
                self.data['title'] = value.strip()[:-7]

        