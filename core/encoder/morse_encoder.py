MORSE_TABLE = {
    'A': '.-',     'B': '-...',   'C': '-.-.', 
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    '1': '.----',  '2': '..---',  '3': '...--',
    '4': '....-',  '5': '.....',  '6': '-....',
    '7': '--...',  '8': '---..',  '9': '----.',
    '0': '-----',  ' ': '/'
}

class MorseEncoder:
    def encode(self, text: str) -> str:
        return ' '.join(MORSE_TABLE.get(c.upper(), '?') for c in text)

# Example
if __name__ == "__main__":
    encoder = MorseEncoder()
    print("Morse:", encoder.encode("code red 5"))
