"""
Program creates Fernet filekey.
"""
import argparse


from cryptography.fernet import Fernet


def create_key(keyfile):
    """
    Function creates Fernet key file.
    Args:
        keyfile: Filename for the key file.
    """
    # key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open(keyfile, 'wb') as filekey:
        filekey.write(key)
    print(f"File {keyfile} has been created successfully.")


def main():
    """
    Main function that reads the arguments given by user and encrypts files.
    """
    # Create ArgumentParser object.
    parser = argparse.ArgumentParser(description='Script uses .key file to encrypt files.')
    # Arguments
    parser.add_argument('--keyfile',
                        '-k',
                        help='Path to filekey to create.')
    args = parser.parse_args()

    if args.keyfile is None:
        keyfile = input('Enter the path to the key file: ')
    else:
        keyfile = args.keyfile

    assert keyfile.endswith('.key'), (
        f"Name '{keyfile}' is not correct. Keyfile name has to end with .key extension.")

    create_key(keyfile)


if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print(f"ERROR: {e}")
