import os, json

from format_readers.reader_class import Reader

class PNGReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.png'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'rb') as file:
            content = ''.join(f'{byte:08b}' for byte in file.read())
        
        #content = '100010010101000001001110010001110000110100001010000110100000101000000000000000000000000000001101010010010100100001000100010100100000000000000000000000000000000100000000000000000000000000000001000010000000001000000000000000000000000010010000011101110101001111011110000000000000000000000000000011000100100101000100010000010101010000001000110101110110001111111000110011111100000000000000000000000000001100000001000000010000000000011000110111011000110110110000000000000000000000000000000000000100100101000101010011100100010010101110010000100110000010000010'

        data = {
            'binary': {
                'content': content,
                'signature': content[:64],
                'chunks': {},
            },
            'content': {
                'chunks': {},
            }
        }

        pos = 64
        while pos < len(content):
            bsize = content[pos:pos+32]
            bchunk = content[pos+32:pos+64]
            bcontent = content[pos+64:pos+64+int(bsize, 2)*8]
            bcrc = content[pos+64+int(bsize, 2)*8:pos+96+int(bsize, 2)*8]

            chunk = self._bits_to_text(self._reverse_bytes(bchunk))
            rcontent = None
            if chunk == 'IHDR':
                rcontent = {
                    'width':            int(bcontent[:32], 2),
                    'height':           int(bcontent[32:64], 2),
                    'bits_per_sample':  int(bcontent[64:72], 2),
                    'color_type':       {0: 'grayscale', 2: 'truecolor', 3: 'indexed', 4: 'grayscaled and alpha', 6: 'truecolor and alpha'}[int(bcontent[72:80], 2)],
                    'compression':      int(bcontent[80:88], 2),
                    'filter':           int(bcontent[88:96], 2),
                    'interlace':        ['no interlace', 'Adam7 interlace'][int(bcontent[96:104], 2)],
                }

                color_type = int(bcontent[72:80], 2)

                bcontent = {
                    'content':          bcontent,
                    'width':            bcontent[:32],
                    'height':           bcontent[32:64],
                    'bits_per_sample':  bcontent[64:72],
                    'color_type':       bcontent[72:80],
                    'compression':      bcontent[80:88],
                    'filter':           bcontent[88:96],
                    'interlace':        bcontent[96:104],
                }
            elif chunk == 'PLTE':
                rcontent = {}
                bc = {'content': bcontent}
                for i in range(int(bsize, 2) // 3):
                    rcontent[str(i)] = {
                        'red':      int(bcontent[i*24:i*24+8], 2),
                        'green':    int(bcontent[i*24+8:i*24+16], 2),
                        'blue':     int(bcontent[i*24+16:i*24+14], 2),
                    }

                    bc[str(i)] = {
                        'red':      bcontent[i*24:i*24+8],
                        'green':    bcontent[i*24+8:i*24+16],
                        'blue':     bcontent[i*24+16:i*24+24],
                    }
                
                bcontent = bc
            elif chunk == 'tRNS':
                rcontent = {}
                bc = {'content': bcontent}
                if color_type == 0:
                    rcontent[str(int(bcontent[:16], 2))] = '0'
                    bc[bcontent[:16]] = '0'
                elif color_type == 2:
                    rcontent[(int(bcontent[:16], 2), int(bcontent[16:32], 2), int(bcontent[32:48], 2))] = '0'
                    bc[bcontent[:48]] = '0'
                elif color_type == 3:
                    for i in range(int(bsize, 2)):
                        rcontent[str(i)] = int(bcontent[i*8:i*8+8], 2)
                        bc[str(i)] = bcontent[i*8:i*8+8]
                bcontent = bc
            elif chunk == 'gAMA':
                bc = {'content': bcontent}
                rcontent = {'content': int(bcontent, 2) / 100000}
            elif chunk == 'cHRM':
                bc = {
                    'content':          bcontent,
                    'white_point_x':    bcontent[:32],
                    'white_point_y':    bcontent[32:64],
                    'red_x':            bcontent[64:96],
                    'red_y':            bcontent[96:128],
                    'green_x':          bcontent[128:160],
                    'green_y':          bcontent[160:192],
                    'blue_x':           bcontent[224:256],
                    'blue_y':           bcontent[256:],
                }
                rcontent = {
                    'white_point_x':    int(bcontent[:32], 2) / 100000,
                    'white_point_y':    int(bcontent[32:64], 2) / 100000,
                    'red_x':            int(bcontent[64:96], 2) / 100000,
                    'red_y':            int(bcontent[96:128], 2) / 100000,
                    'green_x':          int(bcontent[128:160], 2) / 100000,
                    'green_y':          int(bcontent[160:192], 2) / 100000,
                    'blue_x':           int(bcontent[224:256], 2) / 100000,
                    'blue_y':           int(bcontent[256:], 2) / 100000,
                }
            elif chunk == 'sRGB':
                bc = {'rendering_intent': bcontent}
                bc = {'rendering_intent': ['perceptual', 'relative colorimetric', 'saturation', 'absolute colorimetric'][int(bcontent, 2)]}
            elif chunk == 'iCCP':
                profile_name = ''
                for i in range(int(bsize, 2)):
                    if bcontent[i*8:i*8+8] != '00000000':
                        profile_name += bcontent[i*8:i*8+8]
                    else: break
                rcontent = {
                    'profile_name': self._bits_to_text(self._reverse_bytes(profile_name)),
                    'compression': int(bcontent[i*8+8:i*8+16], 2),
                    'compression_profile': self._bits_to_text(self._reverse_bytes(bcontent[i*8+16:])),
                }
                bcontent = {
                    'content': bcontent,
                    'profile_name': profile_name,
                    'compression': bcontent[i*8+8:i*8+16],
                    'compression_profile': bcontent[i*8+16:],
                }
            elif chunk == 'pHYs':
                rcontent = {
                    'x_pixels_per_unit':    int(bcontent[:32], 2),
                    'y_pixels_per_unit':    int(bcontent[32:64], 2),
                    'unit_specifier':       ['unknown', 'meter'][int(bcontent[64:72], 2)],
                }
                bcontent = {
                    'content':              bcontent,
                    'x_pixels_per_unit':    bcontent[:32],
                    'y_pixels_per_unit':    bcontent[32:64],
                    'unit_specifier':       bcontent[64:72],
                }
            elif chunk == 'sBIT':
                rcontent = int(bcontent, 2)
            elif chunk == 'tEXt':
                key, value = self._bits_to_text(self._reverse_bytes(bcontent)).split('\u0000')
                rcontent = {key: value}
                bcontent = {
                    'content':  bcontent,
                    'key':      bcontent[:len(key) * 8],
                    'text':     bcontent[len(key) * 8 + 8:],
                }
            elif chunk == 'zTXt':
                key, value = self._bits_to_text(self._reverse_bytes(bcontent)).split('\u0000')
                rcontent = {key: value[1:]}
                bcontent = {
                    'content':      bcontent,
                    'key':          bcontent[:len(key) * 8],
                    'compression':  bcontent[len(key) * 8 + 8:len(key) * 8 + 16],
                    'text':         bcontent[len(key) * 8 + 16:],
                }
            elif chunk == 'iTXt':
                key = ''
                for i in range(int(bsize, 2)):
                    if bcontent[i*8:i*8+8] != '00000000':
                        key += bcontent[i*8:i*8+8]
                    else: break
                compression_flag = bcontent[i*8+8:i*8+16]
                compression      = bcontent[i*8+16:i*8+32]
                language_tag = ''
                for j in range(i*8+32, int(bsize, 2)):
                    if bcontent[j*8:j*8+8] != '00000000':
                        language_tag += bcontent[j*8:j*8+8]
                    else: break
                translated_key = ''
                for i in range(j*8+8, int(bsize, 2)):
                    if bcontent[i*8:i*8+8] != '00000000':
                        translated_key += bcontent[i*8:i*8+8]
                    else: break
                text = bcontent[i*8+8:]

                rcontent = {
                    'key':              self._bits_to_text(self._reverse_bytes(key)),
                    'compression_flag': ['uncompressed text', 'compressed text'][int(compression_flag, 2)],
                    'compression':      int(compression, 2),
                    'language_tag':     'unspecified' if len(language_tag) == 0 else self._bits_to_text(self._reverse_bytes(language_tag)),
                    'translated_key':   self._bits_to_text(self._reverse_bytes(translated_key)),
                    'text':             self._bits_to_text(self._reverse_bytes(text)),
                }
                bcontent = {
                    'content':          bcontent,
                    'key':              key,
                    'compression_flag': compression_flag,
                    'compression':      compression,
                    'language_tag':     language_tag,
                    'translated_key':   translated_key,
                    'text':             text,
                }
            elif chunk == 'bKGD':
                if color_type == 3:
                    rcontent = {'palette_index': str(int(bcontent, 2))}
                    bcontent = {'palette_index': bcontent}
                elif color_type in [0, 4]:
                    rcontent = {'gray': str(int(bcontent, 2))}
                    bcontent = {'gray': bcontent}
                elif color_type in [2, 6]:
                    rcontent = {
                        'red':      int(bcontent[:16], 2),
                        'green':    int(bcontent[16:32], 2),
                        'blue':     int(bcontent[32:], 2),
                    }
                    bcontent = {
                        'content':  bcontent,
                        'red':      bcontent[:16],
                        'green':    bcontent[16:32],
                        'blue':     bcontent[32:],
                    }
            elif chunk == 'sPLT':
                palette_name = ''
                for i in range(int(bsize, 2)):
                    if bcontent[i*8:i*8+8] != '00000000':
                        palette_name += bcontent[i*8:i*8+8]
                    else: break
                bsample_depth = bcontent[i*8+8:i*8+16] 
                sample_depth = int(bsample_depth, 2)
                sd = (sample_depth - 2) // 4
                pos = i*8+16
                bsamples = []
                samples = []
                for i in range((int(bsize, 2) - pos // 8) // sample_depth):
                    samples.append({
                        'red':          int(bcontent[pos:pos+8*sd], 2),
                        'green':        int(bcontent[pos+8*sd:pos+16*sd], 2),
                        'blue':         int(bcontent[pos+16*sd:pos+24*sd], 2),
                        'frequency':    int(bcontent[pos+24*sd:pos+24*sd+16], 2),
                    })
                    bsamples.append({
                        'red':          bcontent[pos:pos+8*sd],
                        'green':        bcontent[pos+8*sd:pos+16*sd],
                        'blue':         bcontent[pos+16*sd:pos+24*sd],
                        'frequency':    bcontent[pos+24*sd:pos+24*sd+16],
                    })
                
                rcontent = {
                    'palette_name': self._bits_to_text(self._reverse_bytes(palette_name)),
                    'sample_depth': sample_depth,
                    'samples': samples,
                }
                bcontent = {
                    'palette_name': palette_name,
                    'sample_depth': bsample_depth,
                    'samples': bsamples,
                }
            elif chunk == 'hIST':
                color_frequencies = {}
                bcolor_frequencies = {}
                for i in range(int(bsize, 2) // 2):
                    color_frequencies[str(i)] = int(bcontent[i*16:i*16+16], 2)
                    bcolor_frequencies[str(i)] = bcontent[i*16:i*16+16]
                rcontent = {'color_frequencies': color_frequencies}
                bcontent = {'content': bcontent, 'color_frequencies': bcolor_frequencies}
            elif chunk == 'tIME':
                rcontent = {
                    'year':     int(bcontent[:16], 2),
                    'month':    int(bcontent[16:24], 2),
                    'day':      int(bcontent[24:32], 2),
                    'hour':     int(bcontent[32:40], 2),
                    'minute':   int(bcontent[40:48], 2),
                    'second':   int(bcontent[48:], 2),
                }
                bcontent = {
                    'content':  bcontent,
                    'year':     bcontent[:16],
                    'month':    bcontent[16:24],
                    'day':      bcontent[24:32],
                    'hour':     bcontent[32:40],
                    'minute':   bcontent[40:48],
                    'second':   bcontent[48:],
                }



            if chunk not in ['tEXt', 'zTXt', 'iTXt', 'IDAT']:
                data['binary']['chunks'][bchunk] = {
                    'size': bsize,
                    'type': bchunk,
                    'content': bcontent,
                    'crc': bcrc,
                }

                data['content']['chunks'][chunk] = {
                    'size': int(bsize, 2),
                    'type': chunk,
                    'content': rcontent,
                }
            elif chunk == 'IDAT':
                if 'data_chunks' not in data['content']['chunks']:
                    data['content']['chunks']['data_chunks'] = []
                if 'data_chunks' not in data['binary']['chunks']:
                    data['binary']['chunks']['data_chunks'] = []
                
                data['content']['chunks']['data_chunks'].append({
                    'size': int(bsize, 2),
                    'type': chunk,
                    'content': rcontent,
                })
                data['binary']['chunks']['data_chunks'].append({
                    'size': bsize,
                    'type': bchunk,
                    'content': bcontent,
                    'crc': bcrc,
                })
            else:
                if 'text_chunks' not in data['content']['chunks']:
                    data['content']['chunks']['text_chunks'] = []
                if 'text_chunks' not in data['binary']['chunks']:
                    data['binary']['chunks']['text_chunks'] = []
                
                data['content']['chunks']['text_chunks'].append({
                    'size': int(bsize, 2),
                    'type': chunk,
                    'content': rcontent,
                })
                data['binary']['chunks']['text_chunks'].append({
                    'size': bsize,
                    'type': bchunk,
                    'content': bcontent,
                    'crc': bcrc,
                })
                

            pos += int(bsize, 2) * 8 + 96


        self.data.update(data)


    def _reverse_bytes(self, bits: str) -> str:
        return ''.join([bits[i*8:i*8+8] for i in range(len(bits) // 8)][::-1])

    def _bits_to_text(self, bits: str) -> str:
        return ''.join([chr(int(bits[i*8:i*8+8], 2)) for i in range(len(bits) // 8)][::-1])