"""
Script removes metadata from files.
"""
import subprocess
import argparse
import os


def remove_metadata(file_path, exiftool_path):
    """
    Function to remove metadata from file.
    Args:
        file_path: Path to file.
    """
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    if not file_path.endswith('.txt'):
        try:
            # Use exiftool to remove metadata
            subprocess.run([exiftool_path, '-all=', file_path], check=True)
            print(f"Metadata removed from {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error removing metadata from {file_path}: {e}")


def main():
    """
    Main function that reads arguments and removes metadata from files.
    """
    parser = argparse.ArgumentParser(description='Remove metadata from a file.')
    parser.add_argument('--exiftool',
                        '-e',
                        help='Path to exiftool.exe tool.')
    parser.add_argument('--dir',
                    '-d',
                    help='Path to directory to remove metadata from (optional if file is given).')
    parser.add_argument('--file',
                        '-f',
                        help='Path to file to remove metadata from (optional if dir is given).')
    args = parser.parse_args()

    if args.exiftool is None:
        exiftool_path = input('Enter the path to exiftool.exe: ')
    else:
        exiftool_path = args.exiftool

    assert os.path.exists(exiftool_path), f"File {exiftool_path} does not exist."

    if args.dir is None and args.file is None:
        dirname = input('Enter the path to directory to remove metadata from, leave empty if NA: ')
    else:
        dirname = args.dir

    if args.file is None and args.file is None:
        filename = input('Enter the path to the file to remove metadata from, leave empty if NA: ')
    else:
        filename = args.file

    assert filename or dirname, "No file or directory was given."

    if filename:
        remove_metadata(filename, os.path.abspath(exiftool_path))

    if dirname:

        assert os.path.isdir(dirname), f"Directory with path '{dirname}' does not exist."
        assert os.path.abspath(dirname) != os.path.abspath(os.getcwd()), (
            "Current directory cannot be encrypted.")

        for file_name in os.listdir(dirname):
            remove_metadata(os.path.abspath(os.path.join(dirname, file_name)),
                            os.path.abspath(exiftool_path))


if __name__ == '__main__':
    main()
