import sys
import string


def count_text(text: string) -> dict:
    '''
    Function to count the sums of a text's upper-case,
    lower-case, punctuations, digits and spaces.
    '''
    result = {"total": 0, "uc": 0, "lc": 0, "punct": 0, "digit": 0, "space": 0}
    for char in text:
        if char.isupper():
            result["uc"] += 1
        elif char.islower():
            result["lc"] += 1
        elif char.isdigit():
            result["digit"] += 1
        elif char.isspace():
            result["space"] += 1
        elif char in string.punctuation:
            result["punct"] += 1
    result["total"] = len(text)
    return result


def print_result(ret: dict) -> None:
    '''
    Function to print the result.
    '''
    print("The text contains", ret["total"], "characters:")
    print(ret["uc"], "upper letters")
    print(ret["lc"], "lower letters")
    print(ret["punct"], "punctuation marks")
    print(ret["space"], "spaces")
    print(ret["digit"], "digits")


def main():
    '''Autonomous program which takes a single string
    and displays the sums of its upper-case,
    lower-case, punctuations, digits and spaces.
    '''
    if len(sys.argv[1:]) > 1:
        print("AssertionError: more than one argument is provided")
        return
    elif len(sys.argv[1:]) == 1:
        text = sys.argv[1]
    elif (len(sys.argv[1:]) == 0):
        print("What is the text to count?")
        text = sys.stdin.read()
    ret = count_text(text)
    print_result(ret)


if __name__ == "__main__":
    main()
