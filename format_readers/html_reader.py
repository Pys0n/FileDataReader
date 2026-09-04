import os, json

from format_readers.reader_class import Reader

class HTMLReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.html', '.htm'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
            splited = text.split('>')
            doctype = splited[0] + '>'
        
        file_extension = '.' + self.file_name.split('.')[-1]
        if file_extension not in ['.html', '.htm']:
            file_extension = '.html'

        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': file_extension,
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

        