"""
Given a file that contains a fernet key, uses it to encrypt given folder or files.
"""
import argparse
import os.path
import cryptography

from cryptography.fernet import Fernet


def _str_to_bool(s):
    """
    Function to convert string to boolean.
    """
    assert s, "No encryption mode was given."
    return s.lower() == "true"


def decrypt_file(filename, fernet, encrypt=False):
    """
    Function to decrypt a file given a keyfile.
    Args: 
        filename: Path to file to encrypt.
        keyfile: Path to filekey.key to be used to encrypt the file.
    """
    try:
        # Opening the encrypted file.
        with open(filename, 'rb') as enc_file:
            encrypted = enc_file.read()

        # Decrypting the file.
        decrypted = fernet.decrypt(encrypted)

        if not encrypt:
            # Opening the file in write mode and writing the decrypted data.
            with open(filename, 'wb') as dec_file:
                dec_file.write(decrypted)
            print(f'File {filename} has ben successfully decrypted.')
        else:
            raise Exception("File is already encrypted.")
    except cryptography.fernet.InvalidToken:
    # Decryption failed due to an invalid token (likely not encrypted).
        if not encrypt:
            print(f'ERROR: {filename} does not seem to be encrypted.' +
            ' Or is encripted with a different filekey.')
        else:
            raise
    except Exception as er:
        # Handle other specific exceptions as needed.
        if not encrypt:
            print(f"ERROR: An error occurred while decrypting {filename}: {er}")
        else:
            raise


def encrypt_file(filename, fernet):
    """
    Function encrypts file using provided keyfile.
    Args: 
        filename: Path to file to encrypt.
        keyfile: Path to filekey.key to be used to encrypt the file.
    """
    try:
        decrypt_file(filename, fernet, True)
    except cryptography.fernet.InvalidToken: # Use-case original file not encrypted.
        try:
            # Opening the original file to encrypt.
            with open(filename, 'rb') as file:
                original = file.read()

            # Encrypting the file.
            encrypted = fernet.encrypt(original)

            # Opening the file in write mode and writing the encrypted data.
            with open(filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

            print(f'File {filename} has ben successfully encrypted.')
        except Exception as er:
            # Handle other specific exceptions as needed
            print(f"ERROR: An error occurred while encrypting {filename}: {er}")
    except Exception as er:
        # Handle other specific exceptions as needed
        print(f"ERROR: An error occurred while encrypting {filename}: {er}")


def process_file(filename, fernet, encrypt):
    """
    Function processes a file either encrypting or decrypting it based of encrypt.
    """
    assert os.path.exists(filename), f"Filename with path '{filename}' does not exist."

    if not filename.endswith('.key'):
        if encrypt:
            encrypt_file(filename, fernet)
        else:
            decrypt_file(filename, fernet)


def parse_arguments():
    """
    Parse command-line arguments and return the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Script uses .key file to encrypt files.')
    parser.add_argument('--encrypt',
                        '-e',
                        default=False,
                        help='If true program encrypts, if False program decrypts (default: False)')
    parser.add_argument('--keyfile', '-k', help='Path to filekey.key')
    parser.add_argument('--dir',
                        '-d',
                        help='Path to directory to encrypt (optional if file is given).')
    parser.add_argument('--file',
                        '-f',
                        help='Path to file to encrypt (optional if dir is given).')

    args = parser.parse_args()

    if args.keyfile is None:
        keyfile = input('Enter the path to the key file: ')
        encrypt = _str_to_bool(input('Enter True if encryption is desired or False to decrypt: '))
    else:
        keyfile = args.keyfile
        encrypt = _str_to_bool(args.encrypt)

    assert os.path.exists(keyfile), f"Keyfile with path '{keyfile}' does not exist."
    assert keyfile.endswith('.key'), (
        f"Name '{keyfile}' is not correct. Keyfile name has to end with .key extension.")

    if args.dir is None and args.file is None:
        dirname = input('Enter the path to directory to encrypt/decrypt or leave empty if NA: ')
    else:
        dirname = args.dir

    if args.file is None and args.file is None:
        filename = input('Enter the path to the file to encrypt/decrypt or leave empty if NA: ')
    else:
        filename = args.file

    assert filename or dirname, "No file or directory was given."

    return keyfile, encrypt, dirname, filename


def main():
    """
    Main function that reads the arguments given by user and encrypts files.
    """

    keyfile, encrypt, dirname, filename = parse_arguments()

    # Opening the key.
    with open(keyfile, 'rb') as filekey:
        key = filekey.read()

    # Using the generated key.
    fernet = Fernet(key)

    if filename:
        process_file(filename, fernet, encrypt)

    if dirname:

        assert os.path.isdir(dirname), f"Directory with path '{dirname}' does not exist."
        assert os.path.abspath(dirname) != os.path.abspath(os.getcwd()), (
            "Current directory cannot be encrypted.")

        for file_name in os.listdir(dirname):
            process_file(os.path.join(dirname, file_name), fernet, encrypt)


if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print(f"ERROR: {e}")
