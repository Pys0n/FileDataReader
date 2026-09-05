import os, json

from format_readers.reader_class import Reader

class BINReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.bin'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'rb') as file:
            content = ''.join(f'{byte:08b}' for byte in file.read())
        
        data = {
            'binary_content': content,
            'content': self._bits_to_text(content),
        }

        self.data.update(data)


    def _bits_to_text(self, bits: str) -> str:
        return ''.join([chr(int(bits[i*8:i*8+8], 2)) for i in range(len(bits) // 8)][::-1])