import re
import os
import json
from pathlib import Path

# from pprint import pprint
# import threading


from copy import deepcopy






### functions specifyed to data 



def query(data_structure, criteria):
    """
    Filters structured data using the specified criteria.

    This function allows you to extract specific fields from structured data represented
    as nested dictionaries or lists. The provided criteria are used to filter the data and
    return only the corresponding fields.

    Args:
    - data_structure (dict | list): The structured data to be parsed.
    - criteria (dict | list | bool | callable): The criteria to be used for filtering.
      - If a dictionary, the function will return a new dictionary with corresponding fields.
      - If a list, it will return a list of filtered data.
      - If True, it will return the original data without filtering.
      - If a callable, it will apply the function to the respective value in the dictionary.


    Returns:
    - dict | list | None: The filtered data as per the provided criteria or None if the criteria
      is neither a dictionary nor a list.

    Examples:
        # Usage with dictionary and lambda function
        data = {
            "name": "John",
            "age": 30,
            "address": {"city": "New York", "state": "NY"},
        }
        criteria = {"name": True, "address": {"city": lambda x: x.upper()}}
        result = query(data, criteria)

        # Usage with list and custom function
        data = [{"name": "John"}, {"name": "Alice"}]
        criteria = [{"name": True}, {"name": lambda x: x.lower()}]
        result = query(data, criteria)
    """

    if isinstance(criteria, bool):
        if criteria:
            return data_structure
        else:
            raise ValueError("Criteria must be True to include data_structure.")

    if isinstance(data_structure, dict):
        output = {}
        if isinstance(criteria, dict):
            for key, sub_criteria in criteria.items():
                if key in data_structure:
                    if callable(sub_criteria):
                        output[key] = sub_criteria(data_structure[key])
                    else:
                        output[key] = query(data_structure[key], sub_criteria)
        elif isinstance(criteria, list) and len(criteria) == 1:
            sub_criteria = criteria[0]
            for key, value in data_structure.items():
                if key in sub_criteria:
                    filtered_value = (
                        sub_criteria[key](value) if callable(sub_criteria[key]) else
                        query(value, sub_criteria[key]) if isinstance(value, (dict, list)) else
                        value
                    )
                    output[key] = filtered_value
        return output

    elif isinstance(data_structure, list) and criteria:
        sub_criteria = criteria[0]
        if isinstance(sub_criteria, dict):
            return [query(item, sub_criteria) for item in data_structure]
        elif callable(sub_criteria):
            return [sub_criteria(item) for item in data_structure]
    return None


def query_path(data, key_path):
    """
    Accesses nested values within a dictionary using a path of keys which can contain regular expressions.

    This function is designed to delve deep into nested structures, pulling out values that match a
    specified path of keys. Each segment of the path may also be a regular expression, allowing
    for flexible and pattern-based searching.

    Args:
        data (dict): The dictionary from which values will be accessed.
        key_path (str): The path of keys in the format "A/B/C", where segments can be regular expressions.

    Returns:
        list: A list of values corresponding to the key path or an empty list if no match is found.

    Example:
        nested_data = {
            "A": {
                "B1": {"C": "value1"},
                "B2": {"C": "value2"}
            }
        }
        result = query_path(nested_data, "A/B1/C")  # Returns: ["value1"]
    """
    keys = key_path.split('/')
    current_data = [data]

    try:
        for key in keys:
            new_data = []
            for item in current_data:
                if isinstance(item, dict) and key in item:
                    new_data.append(item[key])
                elif isinstance(item, list):
                    for subitem in item:
                        if isinstance(subitem, dict) and key in subitem:
                            new_data.append(subitem[key])
            current_data = new_data
    except (KeyError, TypeError):
        return []

    return current_data


def json_pseudo_format(data, bullet="-", custom_format_func=None, indentation_func=None):
    """
    Format the keys of a (possibly nested) dictionary with custom keys based on the provided options.

    Args:
    - data (dict): The original dictionary to be modified.
    - bullet (str): The bullet string used for indentation.
    - custom_format_func (callable): A function to customize the key formatting.
        * It receives two arguments:
            - key (str): The original dictionary key.
            - value: The value associated with the key in the dictionary.
        * It should return a formatted key (str).
    - indentation_func (callable): A function to determine the indentation.
        * It receives one argument:
            - depth (int): The nesting depth for the current dictionary level.
        * It should return a string representing the desired indentation.

    Returns:
    - list: A list of formatted keys.
    """
    formatted_keys = []

    if indentation_func is None:
        indentation_func = lambda depth: "|   " * depth

    if custom_format_func is None:
        def default_custom_format_func(key, value):
            if isinstance(value, dict):
                return key
            elif isinstance(value, list):
                if any(isinstance(item, dict) for item in value):
                    return f"{key} (list[dict])"
                else:
                    return f"{key} (list)"
            else:
                return f"{key} ({type(value).__name__})"
        
        custom_format_func = default_custom_format_func

    def format_key(key, value, depth):
        indentation_str = indentation_func(depth)
        formatted_key = custom_format_func(key, value)
        if formatted_key is not None:
            return f"{indentation_str}{bullet} {formatted_key}"
        return None

    def recursive_format(data_element, depth):
        if isinstance(data_element, dict):
            for key, value in data_element.items():
                formatted_key = format_key(key, value, depth)
                if formatted_key is not None:
                    formatted_keys.append(formatted_key)
                if isinstance(value, list) and any(isinstance(item, dict) for item in value):
                    recursive_format(value[0], depth + 1)
                else:
                    recursive_format(value, depth + 1)

    recursive_format(data, 0)
    return formatted_keys


def soft_modify(data, value_function, inplace = False):
    """
    Replaces nested values in a dictionary based on the provided value function.

    Args:
        data (dict or list): The original dictionary to be modified.
        value_function (callable): A function that takes two arguments:
            - key (str): The current key in the dictionary.
            - value: The value associated with the key in the dictionary.
          The function should return:
            - The replacement value for the current key, or
            - None, to keep the current value unchanged.

    Returns:
        dict: A new dictionary with the values replaced as specified by the value_function.
    """

    if not isinstance(data, (dict, list) ):
      raise ValueError("data must be a dict or list(dict)")

    if inplace:
        modified_data = data
    else:
        modified_data = deepcopy(data)


    def recursive_insertion(dct):
        if not isinstance(dct, dict):
            raise ValueError("data must be a dict")
        keys_to_modify = list(dct.keys())
        for key in keys_to_modify:
            value = dct[key]

            if isinstance(value, dict):
                recursive_insertion(value)
            
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        recursive_insertion(item)

            new_value = value_function(key, value)            
            if new_value is not None:
                dct[key] = new_value


    if isinstance(modified_data, dict):
        recursive_insertion(modified_data)
    elif isinstance(modified_data, list):
        for item in modified_data:
            recursive_insertion(item)

    return modified_data


def hard_modify(data, path, func, inplace=False):
    """
    Modify a value in a nested dictionary based on a given path and function.
    
    Given a nested dictionary and a path to a specific value within it, this function 
    applies a specified function to that value. The original dictionary can either be 
    modified in place or a modified copy can be returned, based on the 'inplace' argument.
    
    Parameters:
    - data (dict): The original nested dictionary.
    - path (str): The path to the value that needs to be modified, in the format "A/B/C".
    - func (callable): The function to be applied to the specified value.
    - inplace (bool, optional): If True, modifies the original dictionary in place. 
      Otherwise, returns a modified copy. Default is False.
      
    Returns:
    - dict: The modified dictionary (either the original modified in place or a copy).
    
    Example:
        original_data = {
            "A": {
                "B": {"C": 5}
            }
        }
        result = hard_modify(original_data, "A/B/C", lambda x: x*2)  
        # Returns: {"A": {"B": {"C": 10}}}
    """
    keys = path.split("/")

    if inplace:
        current = data
    else:
        current = deepcopy(data)

    # Traverse through the dictionary using the keys from the path
    sub_data = current
    for key in keys[:-1]:
        if key in sub_data:
            sub_data = sub_data[key]
        else:
            # Return the original (or copied) data if path doesn't exist
            return current

    # Use the last key from the path to modify the value with func
    if keys[-1] in sub_data:
        sub_data[keys[-1]] = func(sub_data[keys[-1]])

    return current


### general ( level 1 ) functions


def deep_merge(d):
    """
    Recursively merge nested dictionaries or lists of dictionaries.
    
    Given a dictionary `d`, if any value in `d` is a list of dictionaries, 
    those dictionaries are merged using the `merge_content` function. If a 
    value in `d` is a dictionary, the function is applied recursively on 
    this dictionary. 
    
    Parameters:
    - d (dict or list): Input dictionary or list to process.

    Returns:
    - dict or list: Merged dictionary or list.
    """
    
    # If the input is a dictionary, apply deep_merge recursively to its values
    if isinstance(d, dict):
        return {key: deep_merge(value) for key, value in d.items()}
    # If the input is a list and all items are dictionaries, apply merge_content
    elif isinstance(d, list) and all(isinstance(item, dict) for item in d):
        merged_content = merge_content(d)
        # Check if the merged content is a dictionary and reapply deep_merge
        if isinstance(merged_content, dict):
            return deep_merge(merged_content)
        return merged_content
    # If the input is a list (not necessarily containing only dictionaries), apply deep_merge to each item
    elif isinstance(d, list):
        return [deep_merge(item) for item in d]
    # Base case: if the input isn't any of the above types, return it as it is
    else:
        return d


def merge_content(data_list):
    """
    Merges a list of dictionaries by aggregating their values.

    Given a list of dictionaries, this function combines them by aggregating 
    values associated with the same keys. The values are combined into lists. 
    If, after the merge, a key is associated with a list containing only a 
    single value, the list is unpacked, and the value is stored directly.

    Parameters:
    - data_list (list of dict): A list of dictionaries to be merged.

    Returns:
    - dict: A merged dictionary with values combined into lists where keys are duplicated.
    """

    merged = {}
    
    for data in data_list:
        for key, value in data.items():
            if key not in merged:
                merged[key] = [value]
            else:
                if isinstance(merged[key], list):
                    merged[key].append(value)
                else:
                    merged[key] = [merged[key], value]
    
    # Convert single-item lists back to their values
    for key, value in merged.items():
        if isinstance(value, list) and len(value) == 1:
            merged[key] = value[0]
    
    return merged




### general ( level 2 )functions


def filter(content, keys_to_use):
    return {key: content[key] for key in keys_to_use if key in content}


def structure_data(data, nested=False, keys_content=None, adjust_list=False):
    """
    Structures a list of dictionaries into a nested dictionary based on given paths.

    Parameters:
    -----------
    data : list
        A list of dictionaries where each dictionary must contain a 'path' key denoting the
        path for content insertion and a 'content' key with the data to be inserted.
        
    nested : bool, optional (default = False)
        If True, inserts the content directly into the final dictionary structure without wrapping
        in another dictionary with a 'content_value' key. If False, wraps content in a 'content_value' key.

    keys_content : list or None, optional (default = None)
        If provided, filters out keys from the content dictionaries that are not in this list.

    adjust_list : bool, optional (default = False)
        If True, adjusts the structure to accommodate list insertion based on the path.
        For example, 'A/B[1]' will insert the content in the first position of a list under 'B' key inside 'A'.

    Returns:
    --------
    dict
        A structured dictionary based on the paths provided in the input data.

    Examples:
    ---------
    >>> data = [{'path': 'A/B[1]', 'content': "example 1"},
                {'path': 'A/B[2]', 'content': 'example2'}]
    >>> structure_data(data, nested=True, adjust_list=True)
    {'A': {'B': ["example 1", 'example2']}}

    Note:
    -----
    The path string in the input data is split using the '/' delimiter, and the function expects 
    paths to be correctly formatted. Using '[' and ']' indicates a position in a list for adjust_list=True.
    """


    root = {}

    # Helper function to insert content to the final structure.
    def insert_content(tree, path_parts, content):
        if not path_parts:
            if isinstance(tree, list):
                tree.append(content)
            else:
                if nested:
                    return content
                target = tree.setdefault("value", {})
                
                # If content is a direct value
                if not isinstance(content, dict):
                    if 'content_value' not in target:
                        target['content_value'] = []
                    target['content_value'].append(content)
                    return

                # If content is a dictionary
                if keys_content:
                    content = filter(content, keys_content)
                for key, val in content.items():
                    if key not in target:
                        target[key] = val
                    else:
                        if isinstance(val, list):
                            if not isinstance(target[key], list):
                                target[key] = [target[key]]
                            target[key].extend(val)
                        else:
                            if not isinstance(target[key], list):
                                target[key] = [target[key]]
                            target[key].append(val)
            return

        current = path_parts.pop(0)

        # Check for list adjustment syntax in the current path part
        if adjust_list and "[" in current and "]" in current:
            current, index = current.split("[")
            index = int(index[:-1]) - 1  # Convert to 0-based index

            if current not in tree:
                tree[current] = []

            while len(tree[current]) <= index:
                tree[current].append({})

            subtree = insert_content(tree[current][index], path_parts, content)
            if subtree is not None:  # Check for nested case to replace placeholder dictionary
                tree[current][index] = subtree

        else:
            if current not in tree:
                tree[current] = {}
            subtree = insert_content(tree[current], path_parts, content)
            if subtree is not None:  # Check for nested case
                tree[current] = subtree

    # Process each entry in the data list.
    for entry in data:
        path_parts = entry["path"].split("/")
        insert_content(root, path_parts, entry["content"])

    return root


def flatten_dict(d, parent_key='', content_key=None, func=None):
    """
    Flattens a nested dictionary or list structure into a list of dictionaries with paths and content.
    
    Parameters:
    - d (dict or list): The input dictionary or list to be flattened.
    - parent_key (str, optional): Used for recursive calls to keep track of the current path. Defaults to ''.
    - content_key (str, optional): The specific key to extract content from the dictionary. If not provided, all values are considered as content.
    - func (function, optional): A function to apply on the content. If provided, it's applied to the content of each item.
    
    Returns:
    - list of dicts: Each dictionary has two keys:
        - 'path': the path to reach the item in the original dictionary or list.
        - 'content': the content of the item. If `func` is provided, this is the result of applying `func` to the content.

    Example:
    data = {
        'A': {
            'B': {
                'value': 'example'
            }
        },
        'C': [1, 2, {'value': 'inside_list'}]
    }
    result = flatten_dict(data, content_key='value')
    print(result)
    # [{'path': 'A/B/value', 'content': 'example'}, {'path': 'C[3]/value', 'content': 'inside_list'}]

    Notes:
    - The function handles both dictionaries and lists.
    - For lists, the path will include indices (starting from 1).
    - If `content_key` is provided, only values associated with that key will be included in the output.
    """

    items = []
    
    if not isinstance(d, (dict, list)):
        return []
    
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}/{k}" if parent_key else k
            if isinstance(v, dict):
                if content_key and content_key in v:
                    if func:
                        items.append({'path': new_key, 'content': func(v[content_key]) })
                    else:
                        items.append({'path': new_key, 'content': v[content_key] })
                else:
                    items.extend(flatten_dict(v, new_key, content_key, func))
            elif isinstance(v, list):
                for idx, item in enumerate(v, 1):
                    list_key = f"{new_key}[{idx}]"
                    if content_key and isinstance(item, dict) and content_key in item:
                        if func:
                            items.append({'path': list_key, 'content': func(item[content_key])})
                        else:
                            items.append({'path': list_key, 'content': item[content_key]})
                    else:
                        items.extend(flatten_dict(item, list_key, content_key, func))
            else:
                if not content_key:
                    if func:
                        items.append({'path': new_key, 'content': func(v) })
                    else:
                        items.append({'path': new_key, 'content': v})

    elif isinstance(d, list):
        for idx, item in enumerate(d, 1):
            list_key = f"{parent_key}[{idx}]"
            if isinstance(item, (dict, list)):
                items.extend(flatten_dict(item, list_key, content_key, func))

    return items


def save_dict_as_json_to_folder(dictionary, folder_path, file_name):
    """
    Save a dictionary as a JSON formatted file within a specified folder.

    Args:
        dictionary (dict): The dictionary to be saved as JSON.
        folder_path (str): The path to the folder where the file will be saved.
        file_name (str): The name of the file to be created.

    Raises:
        FileNotFoundError: If the specified folder doesn't exist.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    full_path = os.path.join(folder_path, file_name)

    with open(full_path, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)


def read_json_file(file_path: str) -> dict:
    """
    Read a JSON file and return its content as a Python dictionary.

    Args:
        file_path (str): The path to the JSON file to be read.

    Returns:
        dict: A dictionary representing the content of the JSON file.

    Raises:
        FileNotFoundError: If the file is not found.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    try:
        with path.open('r', encoding='utf-8') as file:
            json_content = json.load(file)
            return json_content
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON: {str(e)}", e.doc, e.pos)



def find_keys_by_regex(data, regex, return_type="dict"):
    """
    Searches for dictionary keys that match a given regular expression.

    Args:
        data (dict): The dictionary to be searched.
        regex (str): The regular expression to be matched.
        return_type (str, optional): Specifies the type of return value - "dict" for a nested dictionary
                                    or "list" for a list of matched key paths. Defaults to "dict".

    Returns:
        dict or list: Depending on the `return_type`, either a nested dictionary containing matched keys
                      or a list of matched key paths.
    """
    if return_type not in ["dict", "list"]:
        raise ValueError("return_type must be either 'dict' or 'list'.")

    if return_type == "dict":
        result = {}
    else:
        result = []

    def search_keys(item, path=[]):
        if isinstance(item, dict):
            for key, value in item.items():
                new_path = path + [key]
                if isinstance(value, (dict, list)):
                    search_keys(value, new_path)
                if re.search(regex, str(key)):
                    if return_type == "dict":
                        current = result
                        for p in new_path[:-1]:
                            current = current.setdefault(p, {})
                        current[new_path[-1]] = value
                    else:
                        result.append('/'.join(map(str, new_path)))

        elif isinstance(item, list):
            for i, element in enumerate(item):
                new_path = path + [i]
                search_keys(element, new_path)

    search_keys(data)
    return result


def find_values_by_depth(data, regex):
    """
    Searches for values within a nested dictionary or list structure that match
    a given regular expression and returns their paths.

    Args:
        data (dict or list): The data structure to be searched.
        regex (str): The regular expression to be matched.

    Returns:
        list of tuple: A list of tuples where the first element of each tuple
                      is the path (as a list of keys) to the matching value,
                      and the second element is the matching value itself.

    Example:
        data = {
            'a': {
                'b': 'value1',
                'c': ['value2', 'match1']
            },
            'd': 'match2'
        }

        find_values_by_depth(data, r'match\d')
        -> [(['a', 'c', 1], 'match1'), (['d'], 'match2')]
    """
    results = []

    def search_depth(item, path=[]):
        if isinstance(item, dict):
            for key, value in item.items():
                new_path = path + [key]
                if isinstance(value, (dict, list)):
                    search_depth(value, new_path)
                elif re.match(regex, str(value)):
                    results.append((new_path, value))
        elif isinstance(item, list):
            for i, element in enumerate(item):
                new_path = path + [i]
                search_depth(element, new_path)

    search_depth(data)
    return results


