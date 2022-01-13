# Project 2 - convert.py With Commandline Arguments
This project consist of a simple python script that extracts data from .json
files and converts it to .csv formatting. The results are stored in a new file
in the same directory as convert.py. 

## Usage
The function convert() accepts multiple command line arguments that can also be
directly passed to the main() function for parsing.

The .json files are expected to have the same formatting as the samples in the
data directory. Additionally, multiple files can be passed to the function in a
single run and their results will all be added to the same output file.

The output file will be created in the same directory as convert.py.

The time formatting is expected to be a valid time formatting string.

The human-readable option is a flag that determines if the output will be in KB.

### Commandline args
--json_file should be followed by the paths for each .json file to convert.

--output_filename should be followed by the desired name for the output file.

--time_str_format should be followed by a valid time format: '%d/%m/%y %H:%M:%S'

-h or --human-readable is a flag that will convert the bytes output.

## Testing
Testing consists of test cases that compare the output of convert() against the
samples in the data directory.

### Prerequisites
The files test_convert.py, convert.py, and __init__.py must all be in the same
directory along with the data directory. This is because tes_convert.py calls
the convert function and uses a sample from the data directory to test.

### Test
Simply execute test_convert.py to run the tests. Testing simulates commandline
arguments by passing them directly to main() which then parses them as if they
were commandline arguments.
