import os, json

from format_readers.reader_class import Reader

class ICSReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extensions, ['.ical', '.ics', '.ifb', '.icalendar'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        data = {
            'content': {
                'content': text,
                'VCALENDAR': {},
            },
        }

        paths = [data['content']['VCALENDAR']]
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
        
        self.data.update(data)
        