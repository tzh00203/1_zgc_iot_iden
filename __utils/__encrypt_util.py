

def encrypt_string(str):
    encrypt_dict = {
        "1": "S",
        "2": "W",
        "3": "y",
        "4": "O",
        "5": "t",
        "6": "v",
        "7": "4",
        "8": "c",
        "9": "I",
        "0": "M",
        ".": "e"
    }
    encrypt_str = ""
    for c in str:
        encrypt_str += encrypt_dict[c]
    
    
    encrypt_str += "7758258"
    return encrypt_str    
    
def decrypt_string(str):
    decrypt_dict = {
        "S": "1",
        "W": "2",
        "y": "3",
        "O": "4",
        "t": "5",
        "v": "6",
        "4": "7",
        "c": "8",
        "I": "9",
        "M": "0",
        "e": "."
    }
    decrypt_str = ""
    for c in str:
        decrypt_str += decrypt_dict[c]
    return decrypt_str    
    
