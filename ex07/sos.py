import sys
import logging

logger = logging.getLogger(__name__)

MORSE_CODE = {
    # alphabet
    'a': '.-',    'b': '-...',  'c': '-.-.',  'd': '-..',
    'e': '.',     'f': '..-.',  'g': '--.',   'h': '....',
    'i': '..',    'j': '.---',  'k': '-.-',   'l': '.-..',
    'm': '--',    'n': '-.',    'o': '---',   'p': '.--.',
    'q': '--.-',  'r': '.-.',   's': '...',   't': '-',
    'u': '..-',   'v': '...-',  'w': '.--',   'x': '-..-',
    'y': '-.--',  'z': '--..',

    # numeric
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',

    # space
    ' ': '/'
}

def main():
    '''
Program that takes a string as an argument and encodes it into Morse Code.
    '''
    try:
        if len(sys.argv[1:]) != 1:
            raise AssertionError("AssertionError: the arguments are bad")
        else:
            text = sys.argv[1]
            text = text.lower()
            invalid_char = [char for char in text if char not in MORSE_CODE]
            if len(invalid_char) > 0:
                raise AssertionError("AssertionError: the arguments are bad")
            for char in text[:-1]:
                print(MORSE_CODE[char], end=" ") 
            print(MORSE_CODE[text[-1]])
    except AssertionError as e:
        print(e)

if __name__ == "__main__":
    main()