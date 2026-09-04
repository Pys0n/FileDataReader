import os, json

class Reader:
    def __init__(self, file: str, ignore_extension: bool = False, extensions: list = []) -> None:
        if not isinstance(file, str):
            raise TypeError(f'Expected `file` to be a str, got {type(file).__name__}')
        if not os.path.isfile(file):
            raise ValueError(f'file "{file}" does not exist')
        if not ignore_extension:
            found = False
            for extension in extensions:
                found = file.endswith(extension)
                if found:
                    break
                
            if not found:
                raise ValueError(f'Expected `file` to be a {' / '.join(extensions)}, got {file.split('.')[-1]}')

        self.file = file
        self.file_name = file.replace('\\', '/').split('/')[-1]


    def get_content(self) -> str:
        if 'content' in self.data:
            if isinstance(self.data['content'], str):
                return self.data['content']
            elif isinstance(self.data['content'], dict):
                if 'content' in self.data['content'] and isinstance(self.data['content']['content'], str):
                    return self.data['content']['content']
        elif 'binary' in self.data:
            if isinstance(self.data['binary']['content'], str):
                return self.data['binary']['content']

        return ''
    

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