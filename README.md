# access2csv

A tool to parse and convert Apache's (Combined Log Format) access.log to csv

## Usage

```console
usage: access2csv.py -i <PATH> [<PATH> ...] -o <PATH> [-e <PATH>] [-h]

Convert Apache's (Combined Log Format) access.log to csv

required:
  -i, --input <PATH> [<PATH> ...]  path to access.log file(s)
  -o, --output <PATH>              path to output file

optional:
  -e, --error <PATH>               path to save lines with parsing errors
  -h, --help                       show this help message and exit
```

## Requirements

Python 3.9 or later
