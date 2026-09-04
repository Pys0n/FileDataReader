import os, json

from format_readers.reader_class import Reader

class XPMReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.xpm'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': '.txt',
            'content': {
                'content': text,
            },
        }

        lines = text.split('\n')
        if lines[0].strip().startswith('#define'):
            # XPM1 -> XPM2
            values = []
            for line in lines[1:5]:
                values.append(line.strip().split()[-1])
            values = ' '.join(values)

            colors = []
            for line in lines[6:6+int(values.split()[2])]:
                line = line.split('"')
                colors.append(line[1] + ' c ' + line[3])

            pixels = []
            for line in lines[8+int(values.split()[2]):]:
                if line.endswith(','):
                    pixels.append(line[1:-2])
                else:
                    pixels.append(line[1:-1])
            
            lines = [values] + colors + pixels
        elif 'XPM2' in lines[0]:
            # XPM2
            lines = lines[1:]
        elif lines[0].strip().startswith('/* XPM */'):
            # XPM3 -> XPM2
            lines = lines[2:-1]
            for i in range(len(lines)):
                line = lines[i].strip()
                if line.endswith(','):
                    line = line[1:-2]
                else:
                    line = line[1:-1]
                lines[i] = line
        else:
            raise ValueError('Unable to identify XPM file version')


        width, height, colors, char_per_pixel = lines[0].split()
        width, height, colors, char_per_pixel = int(width), int(height), int(colors), int(char_per_pixel)
        self.data['content']['width'] = width
        self.data['content']['height'] = height
        self.data['content']['colors'] = colors
        self.data['content']['characters_per_pixel'] = char_per_pixel
        self.data['content']['colors'] = {}

        read_colors = True
        for line in lines[1:2+colors]:
            for color_type in [' c ', ' m ', ' g ', ' s ']:
                if color_type in line:
                    key, val = line.strip().split(color_type)
                    self.data['content']['colors'][key] = (int(val[1:3], 16), int(val[3:5], 16), int(val[5:7], 16))
                    break
        
        self.data['content']['pixel_data'] = []
        for line in lines[2+colors:]:
            row = []
            for i in range(len(line) // char_per_pixel):
                row.append(self.data['content']['colors'][line[i*char_per_pixel:i*char_per_pixel+char_per_pixel]])
            self.data['content']['pixel_data'].append(row)