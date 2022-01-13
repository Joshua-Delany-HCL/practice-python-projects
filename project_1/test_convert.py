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
        path = os.path.join(os.getcwd(), "data", "write-8k.json")
        results_path = convert.convert(path)
        with open(results_path, "r") as f:
            data = f.read()
        os.remove(results_path)
        self.assertEqual(_DATA[0], data)

    def test_failure(self):
        """Test for correct error handling when passed an invalid file paht
        """
        path = os.path.join(os.getcwd(), "data", "not-a-valid-path")
        self.assertRaises(ValueError, lambda: convert.convert(path=path))


if __name__ == '__main__':
    unittest.main()
