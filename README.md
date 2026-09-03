# Usage

To create a new reader use those lines of code:
```python
from reader import FileDataReader

r = FileDataReader('your_file.extension')
```

To access the data you can use the `.get_data()`-function.

You can also save the data in a `.json`-file using this function: `.to_json()` or `.to_json(filename)`.


# List of implemented file types

- [.bmp (.dib)](https://en.wikipedia.org/wiki/BMP_file_format) (coming soon)
- [.csv](https://en.wikipedia.org/wiki/Comma-separated_values)
- [.html (.htm)](https://en.wikipedia.org/wiki/HTML)
- [.json](https://en.wikipedia.org/wiki/JSON)
- [.tsv (.tab)](https://en.wikipedia.org/wiki/Tab-separated_values)
- [.txt](https://en.wikipedia.org/wiki/Text_file)
- [.xml](https://en.wikipedia.org/wiki/XML)