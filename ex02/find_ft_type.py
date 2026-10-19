def all_thing_is_obj(obj: any) -> int:
    if isinstance(obj, list):
        print("List :", end=" ")
    elif isinstance(obj, tuple):
        print("Tuple :", end=" ")
    elif isinstance(obj, set):
        print("Set :", end=" ")
    elif isinstance(obj, dict):
        print("Dict :", end=" ")
    elif isinstance(obj, str):
        print(obj, " is in the kitchen :", end=" ")
    else:
        print("Type is not found")
        return 42
    print(type(obj))
    return 42