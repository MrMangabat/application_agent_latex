
import re
import tiktoken



#some regex to remove characters that intervene with latex commands
def validate_words(do_not_use_words, *args):
    false_count = 0
    true_count = 0
    forbidden_words_used = []

    for arg in args:
        words = arg.split()
        for word in words:
            if word in do_not_use_words:
                forbidden_words_used.append(word)
    
    # Return a tuple with the counts and the list of forbidden words used
    return true_count, false_count, forbidden_words_used

def check_latex_safety(*args):
    # Dictionary to map LaTeX special characters to their safe equivalents
    replacements = {
        '\\': ' ',          # backslash to space
        '{': ' ',           # curly brace to space
        '}': ' ',           # curly brace to space
        '#': ' ',           # hash to space
        '%': ' ',           # percent to space
        '&': 'and',         # ampersand to 'and'
        '_': ' ',           # underscore to space
        '^': ' ',           # caret to space
        '~': ' ',           # tilde to space
        '$': 'dollars',     # dollar to space
        '/': ' ',           # slash to space
        '*': ' ',           # asterisk to space
        '-': ' '            # hyphen to space
    }
    
    # Regex pattern to match any LaTeX special character
    pattern = r'[\\{}#%&_^\~$\/\*\-]'
    
    true_count = 0
    false_count = 0

    # Function to replace matched characters
    def replace_match(match):
        return replacements[match.group(0)]
    
    # Process each input text
    results = []
    for text in args:
        if re.search(pattern, text):
            false_count += 1
            safe_text = re.sub(pattern, replace_match, text)
        else:
            true_count += 1
            safe_text = text
        results.append(safe_text)

    print(f"Number of safe texts: {true_count}")
    print(f"Number of modified texts: {false_count}")

    return results


def count_tokens(text):
    # Get the encoding for the "gpt-3.5-turbo" model
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    # Encode the text into tokens
    amount_of_tokens = encoding.encode(text)
    # Print the number of tokens
    print('tokens', len(amount_of_tokens))


def split_text_at_punctuation(text: str) -> str:
    # Define the regular expression pattern to match punctuation followed by whitespace or end of string
    pattern = re.compile(r'([.!?])\s*')
    # Split the text at each punctuation mark followed by optional whitespace
    phrases = pattern.split(text)
    # Collect the phrases in a list
    result = []
    for i in range(0, len(phrases) - 1, 2):
        result.append((phrases[i] + phrases[i + 1]).strip())
    # If there is any remaining text that does not end with punctuation, add it to the result
    if len(phrases) % 2 != 0:
        result.append(phrases[-1].strip())
    # Join the phrases with newline characters and return the resulting string
    return '\n'.join(result)



def print_data_types(*args):
    for arg in args:
        print("data/objecttype type: ", type(arg))
        print("\n")
        print("what is being validated:", arg)