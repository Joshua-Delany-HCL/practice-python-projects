import os
import unittest

import convert

# Results for write-8k.json from summary-results.csv
_DATA = ["test_datetime,io_bs,io_rw,io_rwmixread,read_iops,read_bw_bytes,read_clat_ns_mean,write_iops,write_bw_bytes,write_clat_ns_mean,error,logfile\n1636757030,8k,write,,0,0,0,46430,380370287,13776938,0,write-8k.json"]


class TestConvert(unittest.TestCase):
    """Simple test for success and failure of convert function
    """
    def test_success(self):
        """Test for successful run when passed a valid file path
        """
        cwd = os.getcwd()
        path = os.path.join(cwd, "data", "write-8k.json")
        results_path = convert.convert(
            paths=[path],
            output_filename=os.path.join(cwd, "results.csv")
        )
        with open(results_path, "r") as f:
            data = f.read()
        os.remove(results_path)
        self.assertEqual(_DATA[0], data)

    def test_failure(self):
        """Test for correct error handling when passed an invalid file path
        """
        path = os.path.join(os.getcwd(), "data", "not-a-valid-path")
        self.assertRaises(
            ValueError,
            lambda: convert.convert(paths=[path], output_filename="failure.csv")
        )

    def test_commandline_single_convert(self):
        """Test for successful run when passed a valid path from commandline
        """
        file_path = os.path.join(os.getcwd(), "data", "write-8k.json")
        arguments = "--json_file {file_path} " \
                    "--output_filename results.csv".format(file_path=file_path)
        results_path = convert.main(
            args=arguments.split()
        )
        with open(results_path, "r") as f:
            data = f.read()
        os.remove(results_path)
        self.assertEqual(_DATA[0], data)

    def test_commandline_multiple_convert(self):
        """Test for successful run with all sample data and parsed arguments
        """
        cwd = os.getcwd()
        files = ["write-8k.json",
                 "write-1M.json",
                 "read-8k.json",
                 "read-1M.json",
                 "rw70-8k.json",
                 "rw70-1M.json",
                 "rw50-8k.json",
                 "rw50-1M.json"]

        # Form arguments list
        paths = []
        for file in files:
            paths.append(os.path.join(cwd, "data", file))
        paths = " ".join(paths)
        arguments = "--json_file {file_paths} " \
                    "--output_filename results.csv".format(file_paths=paths)

        # Call convert with arguments
        results_path = convert.main(
            args=arguments.split()
        )

        # Get test results from convert
        with open(results_path, "r") as f:
            results_data = f.read()
        os.remove(results_path)

        # Get correct data from sumary-results.csv
        with open(os.path.join(cwd, "data", "sumary-results.csv"), "r") as f:
            correct_data = f.read()

        self.assertEqual(correct_data, results_data)

    def test_commandline_multiple_convert_human_readable(self):
        """Test for successful run with all sample data and parsed arguments
        """
        cwd = os.getcwd()
        files = ["write-8k.json",
                 "write-1M.json",
                 "read-8k.json",
                 "read-1M.json",
                 "rw70-8k.json",
                 "rw70-1M.json",
                 "rw50-8k.json",
                 "rw50-1M.json"]

        # Form arguments list
        paths = []
        for file in files:
            paths.append(os.path.join(cwd, "data", file))
        paths = " ".join(paths)
        arguments = "--json_file {file_paths} " \
                    "--output_filename results.csv " \
                    "--human-readable".format(file_paths=paths)

        # Call convert with arguments
        results_path = convert.main(
            args=arguments.split()
        )

        # Get test results from convert 5 & 8
        with open(results_path, "r") as f:
            results_data = f.read()
        os.remove(results_path)

        # Get correct data from sumary-results.csv
        with open(os.path.join(cwd, "data", "sumary-results.csv"), "r") as f:
            correct_data = f.read()

        # Split rows into individual list elements and drop headers
        results_data = results_data.split("\n")[1:]
        correct_data = correct_data.split("\n")[1:]

        # Extract read & write bw_bytes into a tuple per row
        test_bw = []
        correct_bw = []
        for entry in results_data:
            as_array = entry.split(",")
            test_bw.append((as_array[5], as_array[8]))
        for entry in correct_data:
            as_array = entry.split(",")
            correct_bw.append((as_array[5], as_array[8]))

        # Compare results against expected values
        for i in range(len(test_bw)):
            self.assertEqual(float(test_bw[i][0]),
                             round(int(correct_bw[i][0])/1024, 2))
            self.assertEqual(float(test_bw[i][1]),
                             round(int(correct_bw[i][1])/1024, 2))

    def test_commandline_multiple_convert_time_formatted(self):
        """Test for successful run with all sample data, parsed args, and utc
        """
        cwd = os.getcwd()
        files = ["write-8k.json",
                 "write-1M.json",
                 "read-8k.json",
                 "read-1M.json",
                 "rw70-8k.json",
                 "rw70-1M.json",
                 "rw50-8k.json",
                 "rw50-1M.json"]

        # Form arguments list
        paths = []
        for file in files:
            paths.append(os.path.join(cwd, "data", file))
        paths = "  ".join(paths)
        arguments = "--json_file  {file_paths}  " \
                    "--output_filename  results_utc.csv  " \
                    "--time_str_format  %Y-%m-%d %H:%M:%S".format(
                    file_paths=paths)

        # Call convert with arguments
        results_path = convert.main(
            args=arguments.split("  ")
        )

        # Get test results from convert
        with open(results_path, "r") as f:
            results_data = f.read()
        os.remove(results_path)

        # Get correct data from sumary-results.csv
        good_data_path = os.path.join(cwd, "data", "sumary-results-utctime.csv")
        with open(good_data_path, "r") as f:
            correct_data = f.read()

        self.assertEqual(correct_data, results_data)


if __name__ == '__main__':
    unittest.main()