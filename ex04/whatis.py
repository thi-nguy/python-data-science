import sys

arg_list = sys.argv[1:]
if len(arg_list) > 1:
    print("AssertionError: more than one argument is provided")
elif len(arg_list) < 1:
    sys.exit()
else:
    try:
        numb = int(sys.argv[1])
        if numb % 2 == 0:
            print("I'm Even.")
        else:
            print("I'm Odd.")
    except ValueError:
        print("AssertionError: argument is not an integer")