def NULL_not_found(obj: any) -> int:
    if obj is None:
        print("Nothing:", obj, end=" ")
    elif isinstance(obj, float):
        print("Cheese:", obj, end=" ")
    elif isinstance(obj, bool):
        print("Fake:", obj, end=" ")
    elif isinstance(obj, int):
        print("Zero:", obj, end=" ")
    elif obj == "":
        print("Empty:", end=" ")
    else:
        print("Type not Found")
        return 1
    print(type(obj))
    return 1

