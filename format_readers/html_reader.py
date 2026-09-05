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
        
        data = {
            'content': text,
            'DOCTYPE': doctype,
        }
    
        for value in splited:
            if 'lang' in value:
                value = value.replace(' ', '').replace('\'', '"')

                if 'lang="' not in value:
                    continue

                data['lang'] = value.split('lang="')[1].split('"')[0]
            if '<meta' in value:
                value = value.strip()[6:].strip().replace(' ', '').replace('\'', '"')
                if 'name="' in value and 'content="' in value:
                    data[value.split('name="')[1].split('"')[0]] = value.split('content="')[1].split('"')[0]
                elif 'http-equiv="' in value and 'content="' in value:
                    data[value.split('http-equiv="')[1].split('"')[0]] = value.split('content="')[1].split('"')[0]
                elif 'property="' in value and 'content="' in value:
                    data[value.split('property="')[1].split('"')[0]] = value.split('content="')[1].split('"')[0]
            elif '</title' in value:
                data['title'] = value.strip()[:-7]

        self.data.update(data)
        