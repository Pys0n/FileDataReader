import os, json

class PSVReader:
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        if not isinstance(file, str):
            raise TypeError(f'Expected `file` to be a str, got {type(file).__name__}')
        if not os.path.isfile(file):
            raise ValueError(f'file "{file}" does not exist')
        if not ignore_extension and not file.endswith('.psv'):
            raise ValueError(f'Expected `file` to be a .psv, got {file.split('.')[-1]}')

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
            text = ''
            table = []
            for line in file.readlines():
                text += line + '\n'
                table.append(line.split('|'))

        
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': '.psv',
            'content': text[:-1],
            'table': table,
        }