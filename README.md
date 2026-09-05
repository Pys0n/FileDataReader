# Usage

To create a new reader use those lines of code:
```python
from reader import FileDataReader

r = FileDataReader('your_file.extension')
```

To access the data you can use the `.get_data()`-function.

You can also save the data in a `.json`-file using this function: `.to_json()` or `.to_json(filename)`.


# List of implemented file types

- [.bin (binary file)](https://en.wikipedia.org/wiki/Binary_file)
- [.bmp, .dib (bitmap)](https://en.wikipedia.org/wiki/BMP_file_format)
- [.csv (comma-separated values)](https://en.wikipedia.org/wiki/Comma-separated_values)
- [.html, .htm (hypertext markup language)](https://en.wikipedia.org/wiki/HTML)
- [.ical, .ics, .ifb, .icalendar (internet calendaring)](https://en.wikipedia.org/wiki/ICalendar)
- [.ini](https://en.wikipedia.org/wiki/INI_file)
- [.json (javascript object notation)](https://en.wikipedia.org/wiki/JSON)
- [.jsonl, .ndjson, .ldjson (json lines / newline-delimited json)](https://en.wikipedia.org/wiki/JSON_streaming#NDJSON)
- [.md, .markdown](https://en.wikipedia.org/wiki/Markdown)
- [.pls](https://en.wikipedia.org/wiki/PLS_(file_format))
- .psv (pipe-separated values)
- .ssv (semicolon-separated values)
- [.svg, .svgz (scalable vector graphics)](https://en.wikipedia.org/wiki/SVG)
- [.tsv, .tab (tab-separated values)](https://en.wikipedia.org/wiki/Tab-separated_values)
- [.txt (text file)](https://en.wikipedia.org/wiki/Text_file)
- [.vcf (variant call format)](https://en.wikipedia.org/wiki/Variant_Call_Format)
- [.wav, .wave (waveform audio)](https://en.wikipedia.org/wiki/WAV)
- [.xml (extensible markup language)](https://en.wikipedia.org/wiki/XML)
- [.xpm (x pixmap)](https://en.wikipedia.org/wiki/X_PixMap)