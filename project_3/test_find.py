import os
import unittest

import find

_TOP_DIRECTORY = "top_level_dir"
_DIRECTORIES = ["temp_dir_1",
                "temp_practice_dir_2",
                "temp_dir_3"]
_FILES = [("", "practice_1.py"),
          ("temp_practice_dir_2", "practice_2.py"),
          ("temp_practice_dir_2", "logo.png"),
          ("temp_dir_3", "practice_3.py")]


def _build_environment():
    """Creates directories and files in the current working directory
    """
    cwd = os.getcwd()

    # Create directories
    top_directory_path = os.path.join(cwd, _TOP_DIRECTORY)
    if not os.path.exists(top_directory_path):
        os.mkdir(top_directory_path)
    for dir in _DIRECTORIES:
        path = os.path.join(cwd, _TOP_DIRECTORY, dir)
        if not os.path.exists(path):
            os.mkdir(path)

    # Populate directories
    for entry in _FILES:
        open(os.path.join(os.getcwd(), _TOP_DIRECTORY, entry[0], entry[1]), "w")


def _clear_environment():
    """Deletes directories and files created by build_environment
    """
    cwd = os.getcwd()

    # Empty directories
    for entry in _FILES:
        path = os.path.join(cwd, _TOP_DIRECTORY, entry[0], entry[1])
        if os.path.exists(path):
            os.remove(path)

    # Remove directories
    for directory in _DIRECTORIES:
        path = os.path.join(cwd, _TOP_DIRECTORY, directory)
        if os.path.exists(path):
            os.rmdir(path)
    top_directory_path = os.path.join(cwd, _TOP_DIRECTORY)
    if os.path.exists(top_directory_path):
        os.rmdir(top_directory_path)


class TestFind(unittest.TestCase):
    """Unit tests for find.py
    """
    def test_basic(self):
        """Test basic search functionality without type restriction
        """
        path = os.path.join(os.getcwd(), _TOP_DIRECTORY)
        results = find.find(root=path, name=".*practice.*")
        self.assertTrue(len(results) == 4)
        self.assertTrue(os.path.join(path, "temp_practice_dir_2") in results)
        self.assertTrue(os.path.join(path, "practice_1.py") in results)
        self.assertTrue(
            os.path.join(path, "temp_practice_dir_2", "practice_2.py") in
            results)
        self.assertTrue(
            os.path.join(path, "temp_dir_3", "practice_3.py") in results)

    def test_file_type(self):
        """Test search type 'f'
        """
        path = os.path.join(os.getcwd(), _TOP_DIRECTORY)
        results = find.find(root=path, name=".*practice.*", search_type="f")
        self.assertTrue(len(results) == 3)
        self.assertTrue(os.path.join(path, "practice_1.py") in results)
        self.assertTrue(
            os.path.join(path, "temp_practice_dir_2", "practice_2.py") in
            results)
        self.assertTrue(
            os.path.join(path, "temp_dir_3", "practice_3.py") in results)

    def test_dir_type(self):
        """Test search type 'd'
        """
        path = os.path.join(os.getcwd(), _TOP_DIRECTORY)
        results = find.find(root=path, name=".*practice.*", search_type="d")
        self.assertTrue(len(results) == 1)
        self.assertTrue(os.path.join(path, "temp_practice_dir_2") in results)

    def test_bad_type(self):
        """Test search type other than 'f', 'file', 'd', or 'dir'
        """
        path = os.path.join(os.getcwd(), _TOP_DIRECTORY)
        results = find.find(root=path, name=".*practice.*", search_type="g")
        self.assertTrue(len(results) == 4)
        self.assertTrue(
            os.path.join(path, "temp_practice_dir_2") in
            results)
        self.assertTrue(
            os.path.join(path, "practice_1.py") in
            results)
        self.assertTrue(
            os.path.join(path, "temp_practice_dir_2", "practice_2.py") in
            results)
        self.assertTrue(
            os.path.join(path, "temp_dir_3", "practice_3.py") in
            results)

    def test_invalid_root(self):
        """Test if the program will properly terminate when given invalid path
        """
        path = os.getcwd() + "invalid/"
        self.assertRaises(
            ValueError,
            lambda: find.find(root=path, name="")
        )

    def test_invalid_name(self):
        """Test how the program terminates when given an invalid string pattern
        """
        path = os.path.join(os.getcwd(), _TOP_DIRECTORY)
        self.assertRaises(
            ValueError,
            lambda: find.find(root=path, name="*temp_dir_1")
        )


if __name__ == "__main__":
    _build_environment()
    try:
        unittest.main()
    finally:
        pass
        _clear_environment()
