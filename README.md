# Usage

To create a new reader use those lines of code:
```python
from reader import FileDataReader

r = FileDataReader('your_file.extension')
```

To access the data you can use the `.get_data()`-function.

You can also save the data in a `.json`-file using this function: `.to_json()` or `.to_json(filename)`.


# List of implemented file types

- [.bmp, .dib](https://en.wikipedia.org/wiki/BMP_file_format) (bitmap)
- [.csv](https://en.wikipedia.org/wiki/Comma-separated_values) (comma-separated values)
- [.html, .htm](https://en.wikipedia.org/wiki/HTML) (hypertext markup language)
- [.ical, .ics, .ifb, .icalendar](https://en.wikipedia.org/wiki/ICalendar) (internet calendaring)
- [.ini](https://en.wikipedia.org/wiki/INI_file)
- [.json](https://en.wikipedia.org/wiki/JSON) (javascript object notation)
- .psv (pipe-separated values)
- .ssv (semicolon-separated values)
- [.tsv, .tab](https://en.wikipedia.org/wiki/Tab-separated_values) (tab-separated values)
- [.txt](https://en.wikipedia.org/wiki/Text_file) (text file)
- [.vcf](https://en.wikipedia.org/wiki/Variant_Call_Format) (variant call format)
- [.xml](https://en.wikipedia.org/wiki/XML) (extensible markup language)