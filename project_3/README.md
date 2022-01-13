# Project 3 - find.py
This project consists of a script that will search for files or directories that
match a specified search term.

## Usage
The script accepts a root directory where it will begin its search along with
the search term and a search type to determine if files or directories should be
excluded from the search.

### Arguments
'root' must be a valid path to a root directory.

'name' must be a valid regex string.

'search_type' can be empty to find all matching files and directories.
Additionally, it can be 'f' or 'file' to only search for files, or 'd' or 'dir'
to only search for matching directories.

## Commandline
These arguments can also be passed through the commandline.

--root is required and should be followed by a valid directory path.

--name should be followed by a valid regex string.

--type should be followed by 'f', 'file', 'd', or 'dir'.

## Testing
Testing created a directory tree with subfiles in order to test the search
function. Additionally, testing passes arguments directly to find().

### Prerequisites
The files test_find.py, find.py, and _init_.py should all be in the same folder
prior to testing.

### Test
The tests can be ran by executing test_find.py.
