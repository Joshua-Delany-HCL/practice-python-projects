import json
from math import floor
import os

_HEADER = "test_datetime,io_bs,io_rw,io_rwmixread,read_iops,read_bw_bytes,read_clat_ns_mean,write_iops,write_bw_bytes,write_clat_ns_mean,error,logfile"


def convert(path: str = None):
    """Extracts data from a .JSON file and writes data to a new .csv file.

    Extracts data from the .JSON file given in the path and writes the data,
    along with a header, to a new .csv file in .csv format. The new .csv file
    will have the same name as the file given in path, but with a .csv extension
    instead of a .JSON extension.

    Args:
        path: A string path to an existing .JSON file.

    Returns:
        New .csv file with same name as original file, and the extracted data
        written in .csv format.

    Raises:
        ValueError: Not a valid path
    """

    # Check for valid .JSON file
    if not os.path.exists(path):
        raise ValueError(f"Not a valid path: {path}")

    # Load .JSON file
    file_dict = None
    with open(path) as f:
        file_dict = json.load(f)

    # Get desired data from .JSON file
    timestamp = file_dict["timestamp"]
    bs = file_dict["jobs"][0]["job options"]["bs"]
    rw = file_dict["global options"]["rw"]
    rwmixread = file_dict["global options"].get("rwmixread", "")
    read_dict = file_dict["jobs"][0]["read"]
    write_dict = file_dict["jobs"][0]["write"]
    read_iops = floor(read_dict["iops"])
    read_bw_bytes = floor(read_dict["bw_bytes"])
    read_clatnsmean = floor(read_dict["clat_ns"]["mean"])
    write_iops = floor(write_dict["iops"])
    write_bw_bytes = floor(write_dict["bw_bytes"])
    write_clatnsmean = floor(write_dict["clat_ns"]["mean"])
    err_num = file_dict["jobs"][0]["error"]
    logfile = os.path.basename(path)

    # Format retrieved data
    data = f"{timestamp},{bs},{rw},{rwmixread},{read_iops},{read_bw_bytes}," \
           f"{read_clatnsmean},{write_iops},{write_bw_bytes}," \
           f"{write_clatnsmean},{err_num},{logfile}"

    # Output data to .csv file along with header
    name, _ = logfile.split(".")
    name = name + ".csv"
    new_file_path = os.path.join(os.getcwd(), name)
    with open(new_file_path, "w") as f:
        write_data = "\n".join([_HEADER, data])
        f.write(write_data)
        print("Conversion successful: {new_file_path}".format(
            new_file_path=new_file_path))
    return new_file_path
