import os, json

from format_readers.reader_class import Reader

class BMPReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.bmp', '.dib'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'rb') as file:
            content = ''.join(f'{byte:08b}' for byte in file.read())

        info_header_size = int(self._reverse_bytes(content[112:144]), 2)
        data = {
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
        if data['content']['info_header']['num_colors'] <= 8:
            pixel = 0
            data['content']['color_table'] = {}
            data['binary']['color_table'] = {}
            for _ in range(data['content']['info_header']['num_colors']):
                data['content']['color_table'][str(pixel)] =   {}
                data['binary']['color_table'][str(pixel)] =    {}
                
                data['content']['color_table'][str(pixel)]['red'] =    int(self._reverse_bytes(content[current_pos:current_pos+1]), 2)
                data['content']['color_table'][str(pixel)]['green'] =  int(self._reverse_bytes(content[current_pos+1:current_pos+2]), 2)
                data['content']['color_table'][str(pixel)]['blue'] =   int(self._reverse_bytes(content[current_pos+2:current_pos+3]), 2)

                data['binary']['color_table'][str(pixel)]['red'] =         content[current_pos:current_pos+1]
                data['binary']['color_table'][str(pixel)]['green'] =       content[current_pos+1:current_pos+2]
                data['binary']['color_table'][str(pixel)]['blue'] =        content[current_pos+2:current_pos+3]
                data['binary']['color_table'][str(pixel)]['reserved'] =    content[current_pos+3:current_pos+4]

                pixel += 1
                current_pos += 4
        
        pixel_data = content[current_pos:]

        data['binary']['pixel_data'] = {}
        data['binary']['pixel_data']['content'] = pixel_data
        data['content']['pixel_data'] = []
        height, width = data['content']['info_header']['height'], data['content']['info_header']['width']
        pos = 0
        for _ in range(height):
            row = []
            for _ in range(width):
                if data['content']['info_header']['bits_per_pixel'] <= 8:
                    pixel = data['content']['color_table'][str(int(self._reverse_bytes(pixel_data[pos:pos+data['content']['info_header']['bits_per_pixel']]), 2))]
                    row.append((pixel['red'], pixel['green'], pixel['blue']))
                elif data['content']['info_header']['bits_per_pixel'] == 16:
                    row.append(
                        (
                            8 * int(self._reverse_bytes(pixel_data[pos+10:pos+15]), 2),
                            8 * int(self._reverse_bytes(pixel_data[pos+5:pos+10]), 2),
                            8 * int(self._reverse_bytes(pixel_data[pos:pos+5]), 2),
                        )
                    )
                elif data['content']['info_header']['bits_per_pixel'] == 24:
                    row.append(
                        (
                            int(self._reverse_bytes(pixel_data[pos+16:pos+24]), 2),
                            int(self._reverse_bytes(pixel_data[pos+8:pos+16]), 2),
                            int(self._reverse_bytes(pixel_data[pos:pos+8]), 2),
                        )
                    )
        
                pos += data['content']['info_header']['bits_per_pixel']
            
            data['content']['pixel_data'].insert(0, row)
            #pos += 4 - (width * data['content']['info_header']['bits_per_pixel']) % 4
        
        self.data.update(data)

    
    def _reverse_bytes(self, bits: str) -> str:
        return ''.join([bits[i*8:i*8+8] for i in range(len(bits) // 8)][::-1])

    
    def _bits_to_text(self, bits: str) -> str:
        return ''.join([chr(int(bits[i*8:i*8+8], 2)) for i in range(len(bits) // 8)][::-1])