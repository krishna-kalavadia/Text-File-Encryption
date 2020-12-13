from tkinter import *
from tkinter import filedialog
import random
import copy
import sympy

# Used to generate a randomized encryption alphabet which is used for the substitution encryption
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
cipher_alphabet = copy.deepcopy(letters)
random.shuffle(cipher_alphabet)

# Create custom ASCII dicts to avoid characters such as '\t' and '\n'
ascii_dict_num_as_key = {i - 32: chr(i) for i in range(32, 127)}
ascii_dict_char_as_key = {chr(i): i - 32 for i in range(32, 127)}


def encrypt_text(line, vigenere_key):
    """
    Encrypts a string of characters 
    @param line: string of characters to encrypt
    @param vigenere_key: string of characters that will be used as a key for the Vigenere Cipher
    @return encrypted_message: string of encrypted characters
    """
    # Substitution Encryption
    sub_encrypt_dict = dict(zip(letters, cipher_alphabet))
    sub_encrypted = ""
    for char in line:
        try:
            encrypted_letter = sub_encrypt_dict[char]
            sub_encrypted += encrypted_letter
        except KeyError:
            sub_encrypted += char

    # Affine Encryption
    a = 4
    b = 9
    mod_val = 95  # Ensures encrypted num will be mapped to custom ASCII dict
    affine_encrypted = ''
    # For each char encrypt it using the custom ASCII dict
    for char in sub_encrypted:
        try:
            encrypted_num = (a * ascii_dict_char_as_key[char] + b) % mod_val
            encrypted_char = ascii_dict_num_as_key[encrypted_num]
            affine_encrypted += encrypted_char
        except KeyError:
            affine_encrypted += char

    # Vigenere Encryption
    key_index = 0
    vigenere_encrypted = ''
    for char in affine_encrypted:
        try:
            message_num = ascii_dict_char_as_key[char] % mod_val
            key_num = ascii_dict_char_as_key[vigenere_key[key_index]] % mod_val
            encrypted_num = (message_num + key_num) % mod_val
            encrypted_char = ascii_dict_num_as_key[encrypted_num]
            vigenere_encrypted += encrypted_char
            key_index += 1
            if key_index == len(vigenere_key):
                key_index = 0
        except:
            vigenere_encrypted += char

    encrypted_message = vigenere_encrypted

    return encrypted_message


def decrypt_text(line, cipher_alphabet, vigenere_key):
    """
    Decrypts a string of encrypted characters
    @param line: string of characters to decrypt
    @param cipher_alphabet: list that contains the key used for substitution Ex [a,b,c] -> cipher_alphabet of [b,c,a]
    @param vigenere_key: string of characters that will be used as a key for the Vigenere Cipher
    @return decrypted_message: string of decrypted characters
    """
    # Decrypt Vingere Encryption
    key = vigenere_key
    key_index = 0
    mod_val = 95  # ensures encrypted num will be mapped to custom ASCII dict
    vignere_decrypted = ""
    for char in line:
        try:
            message_num = ascii_dict_char_as_key[char] % mod_val
            key_num = ascii_dict_char_as_key[key[key_index]] % mod_val
            encrypted_num = (message_num - key_num) % mod_val
            encrypted_char = ascii_dict_num_as_key[encrypted_num]
            vignere_decrypted += encrypted_char
            key_index += 1
            if key_index == len(key):
                key_index = 0
        except:
            vignere_decrypted += char

    # Decrypt Affine Encryption
    a = 4
    b = 9
    mod_inverse = sympy.mod_inverse(a, mod_val)  # multiplicative inverse needed for decryption
    affine_unencrypted = ''
    # for each char in the encrypted text, decrypt it using the custom ASCII dict
    for char in vignere_decrypted:
        try:
            encrypted_num = (mod_inverse * (ascii_dict_char_as_key[char] - b)) % mod_val
            unencrypted_char = ascii_dict_num_as_key[encrypted_num]
            affine_unencrypted += unencrypted_char
        except KeyError:
            affine_unencrypted += char

    # Decrypt substitution
    sub_decrypt_dict = dict(zip(cipher_alphabet, letters))
    sub_decrypted_message = ""
    for char in affine_unencrypted:
        try:
            decrypted_letter = sub_decrypt_dict[char]
            sub_decrypted_message += decrypted_letter
        except KeyError:
            sub_decrypted_message += char

    decrypted_message = sub_decrypted_message
    return decrypted_message


class MainWindow:
    def __init__(self, root):
        """
        Initializes the main window
        @param root: Toplevel widget object
        """
        self.root = root
        main_lbl = Label(root, text="Text File Encryption", font=("Helvetica", 20), pady=5, padx=10)
        main_lbl.pack()

        select_lbl = Label(root, text="Select an operation from the drop-down menu", font=("Helvetica", 15), pady=10,
                           padx=1)
        select_lbl.pack()

        # Create drop down menu
        drop_down_options = ['Encrypt Text File', "Decrypt Text File"]
        self.variable = StringVar(root)
        self.variable.set(drop_down_options[0])  # sets default value
        options = OptionMenu(self.root, self.variable, *drop_down_options)
        options.pack()

        next_btn = Button(root, text="Next", command=lambda: self.direct_to_window(), pady=1, padx=10)
        next_btn.pack()

        quit_btn = Button(root, text="Quit", font=("Helvetica", 16), command=root.destroy, pady=1, padx=10)
        quit_btn.pack(side=BOTTOM, anchor=SE)

    def direct_to_window(self):
        """
        Directs to a new window based on drop-down menu result
        """
        if self.variable.get() == 'Encrypt Text File':
            self.encryption_window()
        else:
            self.decryption_window()

    def encryption_window(self):
        """
        Asks for the text file to encrypt and the Vigenere key
        """

        # Ask for text file to encrypt and create an error window if user does not select a file
        input_file = filedialog.askopenfilename(title="Select input text file", filetypes=(('text files', 'txt'),))
        if input_file == "":
            error_wd = Toplevel(self.root)
            error_wd.geometry("240x80")
            enter_key_lbl = Label(error_wd, text="ERROR no input file selected", font=("Helvetica", 16), pady=10,
                                  padx=1)
            enter_key_lbl.pack()
            quit_btn = Button(error_wd, text="Close", font=("Helvetica", 14), command=error_wd.destroy, pady=1,
                              padx=10)
            quit_btn.pack()
            return

        encryption_wd = Toplevel(self.root)
        encryption_wd.geometry("300x150")

        enter_key_lbl = Label(encryption_wd, text="Enter key:", font=("Helvetica", 16), pady=10, padx=1)
        enter_key_lbl.pack()

        entry_bar = Entry(encryption_wd)
        entry_bar.pack()

        enter_key_lbl_2 = Label(encryption_wd, text="Example: 'RaPtoRs>>'", font=("Helvetica", 14), pady=10, padx=1)
        enter_key_lbl_2.pack()

        # If user presses encrypt move on to the actual encryption of the file
        # Use lambda function to have multiple callbacks and a callback with parameters
        encrypt_btn = Button(encryption_wd, text="Encrypt", font=("Helvetica", 14), pady=1, padx=10, command=lambda:
                             [self.encrypt_file(entry_bar, input_file), encryption_wd.destroy()])
        encrypt_btn.pack()

    def encrypt_file(self, entry_bar, input_file):
        """
        Encrypts the text file by processing each line separately and writes the result to 'encrypted.txt'
        @param entry_bar: entry widget object
        @param input_file: string containing name of file to encrypt
        """

        # Obtain the Vigenere key from entry bar or create one for user if they did not enter anything
        key = (str(entry_bar.get())).strip()
        if key == "":
            key = "DeFaultKeY"

        # Encrypt each line in input file and write to 'encrypted.txt'
        file_to_encrypt = open(input_file, 'r')
        file_lines = file_to_encrypt.readlines()
        with open('encrypted.txt', 'w') as file:
            print("Writing encrypted lines to encrypted.txt\n")
            for line in file_lines:
                line = line.strip()
                encrypted_line = encrypt_text(line, key)
                file.write(encrypted_line + "\n")
                print(encrypted_line)

        # Output the cipher alphabet and Vigenere key used so it can be used for decryption
        with open('encryption_keys.txt', 'w') as f1:
            cipher_alphabet_str = ','.join(cipher_alphabet)
            f1.write(cipher_alphabet_str + "\n")
            f1.write(key + "\n")

        # Display a confirmation window for user
        completed_wd = Toplevel(self.root)
        completed_wd.geometry("250x120")
        enter_key_lbl = Label(completed_wd, text="Completed Encryption", font=("Helvetica", 16), pady=10, padx=1)
        enter_key_lbl.pack()
        if key == "DeFaultKeY":
            enter_key_lbl = Label(completed_wd, text="No key entered, used Default Key", font=("Helvetica", 14),
                                  pady=10, padx=1)
            enter_key_lbl.pack()

        quit_btn = Button(completed_wd, text="Close", font=("Helvetica", 14), command=completed_wd.destroy, pady=1,
                          padx=10)
        quit_btn.pack()

    def decryption_window(self):
        """
        Asks for the text file to decrypt, and for the text file that contains the encryption keys
        """
        # Ask for text file to decrypt and create an error window if user does not select a file
        input_file = filedialog.askopenfilename(title="Select text file to decrypt", filetypes=(('text files', 'txt'),))
        if input_file == "":
            error_wd = Toplevel(self.root)
            error_wd.geometry("350x100")
            enter_key_lbl = Label(error_wd, text="ERROR no input file to decrypt selected", font=("Helvetica", 15),
                                  pady=10,
                                  padx=1)
            enter_key_lbl.pack()
            quit_btn = Button(error_wd, text="Close", font=("Helvetica", 14), command=error_wd.destroy, pady=1,
                              padx=10)
            quit_btn.pack()
            return

        # Ask for text file containing encryption keys and create an error window if user does not select a file
        key_file = filedialog.askopenfilename(title="Select text file containing encryption keys",
                                              filetypes=(('text files', 'txt'),))
        if key_file == "":
            error_wd = Toplevel(self.root)
            error_wd.geometry("380x100")
            enter_key_lbl = Label(error_wd, text="ERROR no file containing encryption keys selected",
                                  font=("Helvetica", 15), pady=10, padx=1)
            enter_key_lbl.pack()
            quit_btn = Button(error_wd, text="Close", font=("Helvetica", 14), command=error_wd.destroy, pady=1,
                              padx=10)
            quit_btn.pack()
            return

        # Display user's selections
        temp_list = input_file.split("/")
        input_file_name = temp_list[len(temp_list) - 1]
        decryption_wd = Toplevel(self.root)
        decryption_wd.geometry("400x100")
        input_file_lbl = Label(decryption_wd, text="File to decrypt: '" + input_file_name + "'", font=("Helvetica", 14),
                               pady=5, padx=30)
        input_file_lbl.pack()

        temp_list = key_file.split("/")
        key_file_name = temp_list[len(temp_list) - 1]
        input_file_lbl = Label(decryption_wd, text="File containing keys: '" + key_file_name + "'",
                               font=("Helvetica", 14),
                               pady=8, padx=30)
        input_file_lbl.pack()
        # If user presses decrypt button move on to the actual decryption of the file
        # Use lambda function to have multiple callbacks and a callback with parameters
        decrypt_btn = Button(decryption_wd, text="Decrypt", font=("Helvetica", 14), pady=1, padx=10,
                             command=lambda: [self.decrypt_file(input_file, key_file), decryption_wd.destroy()])
        decrypt_btn.pack()

        # Creates space at bottom of window for aesthetic purposes, not the best way to do so
        empty_lbl = Label(decryption_wd, text="", font=("Helvetica", 14), pady=8, padx=30)
        empty_lbl.pack()

    def decrypt_file(self, input_file, key_file):
        """
        Decrypts the encrypted text file by processing each line separately and writes the result to 'decrypted.txt'
        @param input_file: string containing name of file to decrypt
        @param key_file: string containing name of file that holds encryption keys
        """
        # Extract the encryption keys from 'encryption_keys.txt'
        encrypted_file = open(key_file, 'r')
        file_lines = encrypted_file.readlines()
        cipher_alphabet_key = []
        vigenere_key = ''
        i = 1
        for line in file_lines:
            if i == 1:
                line = line.strip().rstrip('\n')
                cipher_alphabet_key = line.split(',')
            elif i == 2:
                line = line.rstrip('\n')
                vigenere_key = line
            i += 1

        # Decrypt each line in encrypted file and write to 'decrypted.txt'
        encrypted_file = open(input_file, 'r')
        file_lines = encrypted_file.readlines()
        with open('decrypted.txt', 'w') as file:
            print("Writing decrypted lines to 'decrypted.txt' using encryption keys from encryption_keys.txt'\n")
            for line in file_lines:
                line = line.strip()
                decrypted_line = decrypt_text(line, cipher_alphabet_key, vigenere_key)
                file.write(decrypted_line + "\n")
                print(decrypted_line)

        # Display a confirmation window for user
        completed_wd = Toplevel(self.root)
        completed_wd.geometry("250x120")
        enter_key_lbl = Label(completed_wd, text="Completed Decryption", font=("Helvetica", 16), pady=5, padx=1)
        enter_key_lbl.pack()
        enter_key_lbl = Label(completed_wd, text="Decrypted text in 'decrypted.txt'", font=("Helvetica", 16), pady=5,
                              padx=1)
        enter_key_lbl.pack()
        quit_btn = Button(completed_wd, text="Close", font=("Helvetica", 14), command=completed_wd.destroy, pady=1,
                          padx=10)
        quit_btn.pack()


if __name__ == '__main__':
    root = Tk()
    root.title('Text File Encryption')
    root.geometry("400x150")
    app = MainWindow(root)
    root.mainloop()
