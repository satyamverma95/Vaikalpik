def create_dict_recursively(keys, values):
    if not keys:
        # base case: no more keys to process, return the final value
        return values
    else:
        # recursive case: create a nested dictionary and process the remaining keys and values
        key = keys[0]
        remaining_keys = keys[1:]
        nested_dict = {key: create_dict_recursively(remaining_keys, values)}
        return nested_dict

# example usage
keys = ["a", "b", "c"]
values = 123
result = create_dict_recursively(keys, values)
print(result)