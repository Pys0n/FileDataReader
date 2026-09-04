import os, json

from format_readers.reader_class import Reader

class ICSReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extensions, ['.ical', '.ics', '.ifb', '.icalendar'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        file_extension = '.' + self.file_name.split('.')[-1]
        if file_extension not in ['.ical', '.ics', '.ifb', '.icalendar']:
            file_extension = '.ics'

        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': file_extension,
            'content': {
                'content': text,
                'VCALENDAR': {

                },
            },
        }

        paths = [self.data['content']['VCALENDAR']]
        for line in text.split('\n')[1:-1]:
            line = line.strip()
            key = line.split(':')[0]
            val = ':'.join(line.split(':')[1:])

            if key == 'BEGIN':
                paths[-1][val] = [{}]
                paths.append(paths[-1][val][0])
            elif key == 'END':
                paths.pop(-1)
            else:
                paths[-1][key] = val