import os, json

from format_readers.reader_class import Reader

class VCFReader(Reader):
    def __init__(self, file: str, ignore_extension: bool = False) -> None:
        super().__init__(file, ignore_extension, ['.vcf'])

        self._load_data()


    def _load_data(self) -> None:
        with open(self.file, 'r') as file:
            text = file.read()
        
        data = {
            'content': {
                'content': text,
            },
        }

        table = None
        for line in text.split('\n'):
            if line.startswith('##') and '=' in line:
                key = line[2:].split('=')[0]
                val = '='.join(line.split('=')[1:])
                if val.startswith('<') and val.endswith('>'):
                    if key.strip() not in data['content']:
                        data['content'][key.strip()] = []

                    data = val[1:-1].split(',')
                    xdata = {}
                    for x in data:
                        xkey = x.split('=')[0]
                        xval = '='.join(x.split('=')[1:]).replace('"', '').replace('\'', '')
                        xdata[xkey] = xval
                    data['content'][key.strip()].append(xdata)
                else:
                    data['content'][key.strip()] = val.strip()

            elif line.startswith('#'):
                while '  ' in line:
                    line = line.replace('  ', ' ')
                table = [line[1:].split()]
            
            else:
                if table == None:
                    continue
            
                while '  ' in line:
                    line = line.replace('  ', ' ')
                table.append(line.split())
        
        data['content']['table'] = table

        self.data.update(data)
