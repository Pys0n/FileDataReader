import os, json

from format_readers.reader_class import Reader

class ITNReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.itn'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        data = {
            'content': text,
            'wapoints': [],
        }

        for line in text.split('\n'):
            longitude, latitude, description, wtype, _ = line.split('|')

            data['wapoints'].append({
                'longitude': int(longitude) / 100000,
                'longitude': int(latitude) / 100000,
                'description': latitude,
                'int_type': int(wtype),
                'type': ['regular', 'waypoint disabled', 'stopover/destination', 'stopover disabled', 'departure point'][int(wtype)],
            })


        self.data.update(data)
