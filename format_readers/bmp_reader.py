import os, json

class BMPReader:
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        if not isinstance(file, str):
            raise TypeError(f'Expected `file` to be a str, got {type(file).__name__}')
        if not os.path.isfile(file):
            raise ValueError(f'file "{file}" does not exist')
        if not ignore_extension and not file.endswith('.bmp'):
            raise ValueError(f'Expected `file` to be a .bmp, got {file.split('.')[-1]}')

        self.file = file
        self.file_name = file.replace('\\', '/').split('/')[-1]
        self._load_data()


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
        with open(self.file, 'rb') as file:
            content = ''.join(f'{byte:08b}' for byte in file.read())
        
        info_header_size = int(self._reverse_bytes(content[112:144]), 2)
        self.data = {
            'full_file_name': self.file_name,
            'file_name': '.'.join(self.file_name.split('.')[:-1]),
            'file_extension': '.bmp',
            'content': {
                'header': {
                    'signature':    self._bits_to_text(self._reverse_bytes(content[:16])),
                    'file_size':    int(self._reverse_bytes(content[16:48]), 2),
                    'data_offset':  int(self._reverse_bytes(content[80:112]), 2),
                },
                'info_header': {
                    'size':             info_header_size,
                    'width':            int(self._reverse_bytes(content[144:176]), 2),
                    'height':           int(self._reverse_bytes(content[176:208]), 2),
                    'planes':           int(self._reverse_bytes(content[208:224]), 2),
                    'palette':          {1: 'monochrome palette', 4: '4bit palletized', 8: '8bit palletized', 16: '16bit RGB', 24: '24bit RGB'}[int(self._reverse_bytes(content[224:240]), 2)],
                    'num_colors':       {1: 1, 4: 16, 8: 256, 16: 65536, 24: 16777216}[int(self._reverse_bytes(content[224:240]), 2)],
                    'bits_per_pixel':   int(self._reverse_bytes(content[224:240]), 2),
                    'compression':      ['no compression', 'BI_RLE8 8bit RLE encoding', 'BI_RLE4 4bit RLE encoding'][int(self._reverse_bytes(content[240:272]), 2)],
                    'image_size':       int(self._reverse_bytes(content[272:304]), 2),
                    'x_pixels_per_m':   int(self._reverse_bytes(content[304:336]), 2),
                    'y_pixels_per_m':   int(self._reverse_bytes(content[336:368]), 2),
                    'colors_used':      int(self._reverse_bytes(content[368:400]), 2),
                    'important_colors': int(self._reverse_bytes(content[400:432]), 2),
                },
            },
            'binary': {
                'content': content,
                'header': {
                    'content':      content[:112],
                    'signature':    content[:16],
                    'file_size':    content[16:48],
                    'reserved':     content[48:80],
                    'data_offset':  content[80:112],
                },
                'info_header': {
                    'content':          content[112:112 + info_header_size * 8],
                    'size':             content[112:144],
                    'width':            content[144:176],
                    'height':           content[176:208],
                    'planes':           content[208:224],
                    'bits_per_pixel':   content[224:240],
                    'compression':      content[240:272],
                    'image_size':       content[272:304],
                    'x_pixels_per_m':   content[304:336],
                    'y_pixels_per_m':   content[336:368],
                    'colors_used':      content[368:400],
                    'important_colors': content[400:432],
                },
            },
        }

        current_pos = 432
        if self.data['content']['info_header']['num_colors'] <= 8:
            pixel = 0
            self.data['content']['color_table'] = {}
            self.data['binary']['color_table'] = {}
            for _ in range(self.data['content']['info_header']['num_colors']):
                self.data['content']['color_table'][str(pixel)] =   {}
                self.data['binary']['color_table'][str(pixel)] =    {}
                
                self.data['content']['color_table'][str(pixel)]['red'] =    int(self._reverse_bytes(content[current_pos:current_pos+1]), 2)
                self.data['content']['color_table'][str(pixel)]['green'] =  int(self._reverse_bytes(content[current_pos+1:current_pos+2]), 2)
                self.data['content']['color_table'][str(pixel)]['blue'] =   int(self._reverse_bytes(content[current_pos+2:current_pos+3]), 2)

                self.data['binary']['color_table'][str(pixel)]['red'] =         content[current_pos:current_pos+1]
                self.data['binary']['color_table'][str(pixel)]['green'] =       content[current_pos+1:current_pos+2]
                self.data['binary']['color_table'][str(pixel)]['blue'] =        content[current_pos+2:current_pos+3]
                self.data['binary']['color_table'][str(pixel)]['reserved'] =    content[current_pos+3:current_pos+4]

                pixel += 1
                current_pos += 4
        
        pixel_data = content[current_pos:]

        self.data['binary']['pixel_data'] = {}
        self.data['binary']['pixel_data']['content'] = pixel_data
        self.data['content']['pixel_data'] = []
        height, width = self.data['content']['info_header']['height'], self.data['content']['info_header']['width']
        pos = 0
        for _ in range(height):
            row = []
            for _ in range(width):
                if self.data['content']['info_header']['bits_per_pixel'] <= 8:
                    pixel = self.data['content']['color_table'][str(int(self._reverse_bytes(pixel_data[pos:pos+self.data['content']['info_header']['bits_per_pixel']]), 2))]
                    row.append((pixel['red'], pixel['green'], pixel['blue']))
                elif self.data['content']['info_header']['bits_per_pixel'] == 16:
                    row.append(
                        (
                            8 * int(self._reverse_bytes(pixel_data[pos+10:pos+15]), 2),
                            8 * int(self._reverse_bytes(pixel_data[pos+5:pos+10]), 2),
                            8 * int(self._reverse_bytes(pixel_data[pos:pos+5]), 2),
                        )
                    )
                elif self.data['content']['info_header']['bits_per_pixel'] == 24:
                    row.append(
                        (
                            int(self._reverse_bytes(pixel_data[pos+16:pos+24]), 2),
                            int(self._reverse_bytes(pixel_data[pos+8:pos+16]), 2),
                            int(self._reverse_bytes(pixel_data[pos:pos+8]), 2),
                        )
                    )
        
                pos += self.data['content']['info_header']['bits_per_pixel']
            
            self.data['content']['pixel_data'].insert(0, row)
            #pos += 4 - (width * self.data['content']['info_header']['bits_per_pixel']) % 4

    
    def _reverse_bytes(self, bits: str) -> str:
        return ''.join([bits[i*8:i*8+8] for i in range(len(bits) // 8)][::-1])

    
    def _bits_to_text(self, bits: str) -> str:
        return ''.join([chr(int(bits[i*8:i*8+8], 2)) for i in range(len(bits) // 8)][::-1])