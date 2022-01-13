import argparse
import os
import re

from typing import Optional


def find(root: str = None,
         name: str = "",
         search_type: Optional[str] = None) -> list[str]:
    """Finds files and/or directories under root that match string pattern.

    Searches and returns files and/or directories that match the given string
    pattern. Starts search from root and searches all subdirectories. Results
    will be returned as a list of paths in string format.

    Args:
        root: A path to an existing directory.
        name: A string pattern to search for. Should be a valid regex.
        search_type: Optional, if search_type is 'd' or 'dir' then only matching
            directories will be returned. If search_type is 'f' or 'file' then
            only matching files (non-directory) will be returned.

    Returns:
        A list of files and/or directories under 'root' that match the given
        name string pattern.

    Raises:
        ValueError: Not a valid root path
        ValueError: Not a valid string pattern
    """
    if not os.path.exists(root):
        raise ValueError(f"Not a valid root path: {root}")
    try:
        re.compile(name)
    except re.error:
        raise ValueError(f"Not a valid string pattern: {name}")

    # Walk through files to find regex matches and append to 'results'
    # If type is not "d", "dir", "f", or "file" then will return all matches.
    results = []
    for curr_root, dirs, files in os.walk(root):
        if search_type not in ("d", "dir"):
            for fname in files:
                if re.match(name, fname):
                    results.append(os.path.join(curr_root, fname))
        if search_type not in ("f", "file"):
            for dname in dirs:
                if re.match(name, dname):
                    results.append(os.path.join(curr_root, dname))

    return results


def main():
    """Parses command line input and calls find with parsed arguments.
    """
    # Create parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, required=True)
    parser.add_argument("--name", type=str)
    parser.add_argument("--type", type=str)

    # Parse command line args
    parsed = parser.parse_args()

    # Find and print matching files
    results = find(root=parsed.root, name=parsed.name, search_type=parsed.type)
    for entry in results:
        print(entry)


if __name__ == "__main__":
    main()
