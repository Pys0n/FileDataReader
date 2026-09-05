import os, json

from format_readers.reader_class import Reader

class WAVReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.wav', '.wave'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'rb') as file:
            content = ''.join(f'{byte:08b}' for byte in file.read())
        
        data = {
            'content': {
                'header': {
                    'file_type_block_id':   self._bits_to_text(self._reverse_bytes(content[:32])),
                    'file_size':            int(self._reverse_bytes(content[32:64]), 2),
                    'file_format_id':       self._bits_to_text(self._reverse_bytes(content[64:96])),
                },
                'info_header': {
                    'format_block_id':      self._bits_to_text(self._reverse_bytes(content[96:128])),
                    'block_size':           int(self._reverse_bytes(content[128:160]), 2),
                    'audio_format':         {1: 'PCM', 3: 'IEEE 754'}.get(int(self._reverse_bytes(content[160:176]), 2), 'unknown'),
                    'number_of_channels':   int(self._reverse_bytes(content[176:192]), 2),
                    'frequency':            int(self._reverse_bytes(content[192:224]), 2),
                    'bytes_per_second':     int(self._reverse_bytes(content[224:256]), 2),
                    'bytes_per_block':      int(self._reverse_bytes(content[256:272]), 2),
                    'bits_per_sample':      int(self._reverse_bytes(content[272:288]), 2),
                },
            },
            'binary': {
                'content': content,
                'header': {
                    'content':              content[:96],
                    'file_type_block_id':   content[:32],
                    'file_size':            content[32:64],
                    'file_format_id':       content[64:96],
                },
                'info_header': {
                    'content':              content[96:288],
                    'format_block_id':      content[96:128],
                    'block_size':           content[128:160],
                    'audio_format':         content[160:176],
                    'number_of_channels':   content[176:192],
                    'frequency':            content[192:224],
                    'bytes_per_second':     content[224:256],
                    'bytes_per_block':      content[256:272],
                    'bits_per_sample':      content[272:288],
                },
            },
        }

        pos = 288
        if int(self._reverse_bytes(content[160:176]), 2) != 1:
            data['binary']['info_header']['extra_parameter_size'] = content[288:304]
            data['content']['info_header']['extra_parameter_size'] = (self._reverse_bytes(content[288:304]), 2)
            data['binary']['info_header']['extra_parameters'] = content[304:38304 + int(self._reverse_bytes(content[288:304]), 2)]
            pos = 304 + int(self._reverse_bytes(content[288:304]), 2)
        
        data['binary']['data'] = {
            'data_block_id':    content[pos:pos+32],
            'data_size':        content[pos+32:pos+64],
            'sampled_data':     [],
        }
        data['content']['data'] = {
            'data_block_id':    self._bits_to_text(self._reverse_bytes(content[pos:pos+32])),
            'data_size':        int(self._reverse_bytes(content[pos+32:pos+64]), 2),
            'sampled_data':     [],
        }
        data_content = content[pos+64:]
        bps = data['content']['info_header']['bits_per_sample']
        sample_size = (bps * data['content']['info_header']['number_of_channels'])
        for i in range(data['content']['data']['data_size'] // sample_size):
            bcdata = []
            cdata = []
            for c in range(data['content']['info_header']['number_of_channels']):
                bcdata.append(data_content[i*sample_size+c*bps:i*sample_size+(c+1)*bps])
                cdata.append(int(self._reverse_bytes(data_content[i*sample_size+c*bps:i*sample_size+(c+1)*bps]), 2))
            data['binary']['data']['sampled_data'].append(bcdata)
            data['content']['data']['sampled_data'].append(cdata)

        self.data.update(data)


    def _reverse_bytes(self, bits: str) -> str:
        return ''.join([bits[i*8:i*8+8] for i in range(len(bits) // 8)][::-1])

    
    def _bits_to_text(self, bits: str) -> str:
        return ''.join([chr(int(bits[i*8:i*8+8], 2)) for i in range(len(bits) // 8)][::-1])