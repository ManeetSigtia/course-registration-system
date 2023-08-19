# function to encrypt a string basd on Ceasar Cipher
def encrypt(string, shift):
    encrypted_string = ''   # final encrypted string that will be produced
    queue = []
    for character in string:
        ascii_code = ord(character)  # determining each character's ASCII value
        # creating an encrypted character for each character in the string
        encrypted_ascii_character = chr(ascii_code + shift)
        queue.append(encrypted_ascii_character)  # adding encrpyted character to queue

    while len(queue) > 0:   # checking for underflow
        # accessing elements in the same order they were added
        encrypted_character = queue.pop(0)
        encrypted_string += encrypted_character  # generating encrypted string
    
    return encrypted_string


# function to decrypt a string basd on Ceasar Cipher
def decrypt(string, shift):
    decrypted_string = ''  # final decrypted string that will be produced
    queue = []
    for character in string:
        ascii_code = ord(character)  # determining each character's ASCII value
        # creating a decrypted character for each character in the string
        decrypted_ascii_character = chr(ascii_code - shift)
        queue.append(decrypted_ascii_character)  # adding decrpyted character to queue

    while len(queue) > 0:   # checking for underflow
        # accessing elements in the same order they were added
        decrypted_character = queue.pop(0)
        decrypted_string += decrypted_character  # generating encrypted string
    
    return decrypted_string
