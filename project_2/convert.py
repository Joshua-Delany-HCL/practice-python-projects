import argparse
from datetime import datetime
import json
from math import floor
import os

_HEADER = "test_datetime,io_bs,io_rw,io_rwmixread,read_iops,read_bw_bytes,read_clat_ns_mean,write_iops,write_bw_bytes,write_clat_ns_mean,error,logfile"


def convert(paths: list[str],
            output_filename: str,
            time_format: str = None,
            human_readable: bool = False):
    """Extracts data from .JSON files and write all extracted data to new file.

    Extracts data from the .JSON files given in the paths list and writes the
    data, along with a header, to a new file in .csv format. The new file
    is the 'output_filename'.

    Args:
        paths: A list of string paths to existing .JSON files.
        output_filename: A string filename that will be used as the filename for
            the new .csv file with extracted data.
        time_format: A string pattern to specify how the extracted time data
            should be formatted.
        human_readable: A flag that determines how bw_bytes should be written.
            If true then the bw_bytes will be written in power of 1024.

    Returns:
        New .csv with results for all .json files specified in paths. Will have
        the name given in output_filename with .csv extension.

    Raises:
        ValueError: Not a valid path
    """
    # Check for valid .JSON file
    for path in paths:
        if not os.path.exists(path):
            raise ValueError(f"Not a valid path: {path}")

    # Load .JSON files and save filename
    loaded_files = []
    for path in paths:
        with open(path) as f:
            loaded_files.append((json.load(f), os.path.basename(path)))
            f.close()

    data = [_HEADER]
    for loaded_file in loaded_files:

        file_dict = loaded_file[0]
        file_name = loaded_file[1]

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
        logfile = file_name

        # Convert formatting
        if time_format is not None:
            timestamp = datetime.utcfromtimestamp(timestamp)
            timestamp = timestamp.strftime(time_format)
        if human_readable is True:
            read_bw_bytes = round(read_bw_bytes/1024, 2)
            write_bw_bytes = round(write_bw_bytes/1024, 2)

        data.append(f"{timestamp},{bs},{rw},{rwmixread},{read_iops},"
                    f"{read_bw_bytes},{read_clatnsmean},{write_iops},"
                    f"{write_bw_bytes},{write_clatnsmean},{err_num},{logfile}")

    # Write data to new file
    new_file_path = os.path.join(os.getcwd(), output_filename)
    with open(new_file_path, "w") as f:
        f.write("\n".join(data))
        print("Results: {new_file_path}".format(new_file_path=new_file_path))
    return new_file_path


def main(args: list[str] = None):
    # Create parser and add arguments
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument(
        "--json_file",
        action='extend',
        nargs="+",
        type=str,
        required=True,
        help="Name of input json file to parse data, this could be multiple."
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        required=True,
        help="Name of output filename."
    )
    parser.add_argument(
        "--time_str_format",
        type=str,
        help="Output timestamp in given string format."
    )
    parser.add_argument(
        "-h", "--human-readable",
        action="store_true",
        help="Convert size bw_bytes into human readable format."
    )

    # Parse command line args
    if args is not None:
        parsed = parser.parse_args(args)
    else:
        parsed = parser.parse_args()
    paths = parsed.json_file
    output_filename = parsed.output_filename
    time_str_format = parsed.time_str_format
    human_readable = parsed.human_readable

    return convert(paths=paths,
                   output_filename=output_filename,
                   time_format=time_str_format,
                   human_readable=human_readable)


if __name__ == "__main__":
    main()
