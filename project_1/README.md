# Project 1 - convert.py
This project consist of a simple python script that extracts data from a .json
file and converts it to .csv formatting. The results are stored in a new file in
the same directory as convert.py. The new file's name is the same as the input
file, but with a .csv extension instead of .json.

## Usage
The function convert() expects to be passed a path to an existing .json file
containing data in the same format as the sample files in the data directory.

## Testing
Testing is simples and only consists of two test cases. However, the files must
be in the correct directories prior to testing.

### Prerequisites
The files test_convert.py, convert.py, and __init__.py must all be in the same
directory along with the data directory. This is because tes_convert.py calls
the convert function and uses a sample from the data directory to test.

### Test
Simply execute test_convert.py to run the tests.
