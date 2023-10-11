from .main import query, query_path, json_pseudo_format, soft_modify, hard_modify

from copy import deepcopy


class JsoniFy:
  def __init__(self, data):
    self.data = data

  def __call__(self, criteria):
    """
    Filters the instance's structured data using the specified criteria.

    This method allows extraction of specific fields from structured data represented
    as nested dictionaries or lists contained within the class instance. The provided 
    criteria are used to filter the data and return only the corresponding fields.

    Args:
    - criteria (dict | list | bool | callable): The criteria to be used for filtering.
      - If a dictionary, the method will return a new dictionary with corresponding fields.
      - If a list, it will return a list of filtered data.
      - If True, it will return the original data without filtering.
      - If a callable, it will apply the function to the respective value in the dictionary.

    Returns:
    - dict | list | None: The filtered data as per the provided criteria or None if the criteria
      is neither a dictionary nor a list.

    Examples:
        # Assuming `instance` is an instance of the class with appropriate data
        
        # Usage with dictionary and lambda function
        criteria = {"name": True, "address": {"city": lambda x: x.upper()}}
        result = instance(criteria)

        # Usage with list and custom function
        criteria = [{"name": True}, {"name": lambda x: x.lower()}]
        result = instance(criteria)
    """
    data = deepcopy(self.data)
    return query(data, criteria)

  def query_path(self, key_path):
    """
    Accesses nested values within the instance's data using a path of keys which can contain regular expressions.

    This method is designed to delve deep into nested structures, pulling out values that match a
    specified path of keys. Each segment of the path may also be a regular expression, allowing
    for flexible and pattern-based searching within the class instance's data.

    Args:
        key_path (str | list of str): The path of keys in the format "A/B/C", where segments can be regular 
        expressions. If provided a list of key paths, the method will return a list of results for each path.

    Returns:
        list | list of lists: 
            - If key_path is a string: A list of values corresponding to the key path or an empty list 
              if no match is found.
            - If key_path is a list of strings: A list of lists, where each inner list corresponds to the 
              results for each key path.

    Example:
        # Assuming `instance` is an instance of the class with appropriate data
        result = instance.query_path("A/B1/C")  # Single path query
        multiple_results = instance.query_path(["A/B1/C", "A/B2/C"])  # Multiple path queries
    """
    if isinstance(key_path,list):
      result = []
      for kp in key_path:
        result.append(
           query_path(self.data, kp) 
        )      
      return result

    elif isinstance(key_path, str):
      return query_path(self.data, key_path)
  
  def pseudo_format(self, bullet = "-", indent = 2, custom_format_func = None, indentation_func = None):
    """
    Formats the keys of the instance's data with custom representation based on the provided options.

    This method leverages the `json_pseudo_format` function to format dictionary keys in a custom manner.
    Keys from the instance's data, which might be nested, can be represented using custom indentation and formatting.

    Args:
        bullet (str, optional): The bullet string used for indentation. Defaults to "-".
        indent (int, optional): The number of spaces to be used for indentation. Defaults to 2.
        custom_format_func (callable, optional): A function to customize the key formatting.
            * It receives two arguments:
                - key (str): The original dictionary key.
                - value: The value associated with the key in the dictionary.
            * It should return a formatted key (str).
            * Defaults to None, meaning no custom formatting will be applied.
        indentation_func (callable, optional): A function to determine the indentation.
            * It receives one argument:
                - depth (int): The nesting depth for the current dictionary level.
            * It should return a string representing the desired indentation.
            * If not provided, default indentation based on `indent` argument will be applied.

    Prints:
        - The formatted keys based on the provided configuration. 

    Note:
        The actual formatting logic is carried out by the `json_pseudo_format` function, this method simply
        provides an interface for the class's data.
    """
    if indentation_func:
        indentation_func = lambda depth: f"|{' '*indent}" * depth
    if custom_format_func:
        custom_format_func = None

    print("\n".join(json_pseudo_format(
        self.data,
        bullet = bullet,
        indentation_func = indentation_func,
        custom_format_func = custom_format_func)))
  
  def soft_insert(self, fun, inplace = False):
    """
    Applies the specified function to the instance's data in a non-destructive manner.

    This method utilizes the `soft_modify` function to apply changes to the data without overwriting the original
    data, unless explicitly asked to do so. This approach is useful for data transformations where preserving the 
    original data structure is essential.

    Args:
        fun (callable): A function to apply to the data.
            * It receives the instance's data as an argument.
            * It should return the modified data.
        inplace (bool, optional): Whether to modify the instance's data in place or return a modified copy.
            Defaults to False, which means a modified copy of the data will be returned without changing the instance's data.

    Returns:
        dict | None: 
            - If `inplace` is False: Returns a modified copy of the instance's data based on the provided function.
            - If `inplace` is True: Modifies the instance's data and returns None.

    Note:
        The actual modification logic is managed by the `soft_modify` function; this method serves as an interface 
        for the class's data.
    """
    if inplace:
        soft_modify(self.data, fun, inplace)
    else:
        return soft_modify(self.data, fun, inplace)


  def hard_insert(self, paths, funs, inplace=False):
    """
    Modifies values in the instance's data based on given paths and functions.

    This method uses the `hard_modify` function to apply specified functions to values within the 
    class's data at the provided paths. The changes can be applied to the original data in place or 
    returned as modified copies, depending on the 'inplace' argument.

    Args:
        paths (list of str): A list of paths to the values that need to be modified, each in the format "A/B/C".
        funs (callable or list of callables): The function(s) to be applied to the specified value(s).
            - If a single callable is provided, it will be applied to all paths.
            - If a list of callables is provided, each function in the list will be applied to the corresponding path.
        inplace (bool, optional): If True, modifies the original data in place.
            Otherwise, returns a list of modified copies. Default is False.

    Returns:
        list of dict | None: 
            - If `inplace` is False: Returns a list of modified copies of the instance's data based on the provided paths and functions.
            - If `inplace` is True: Modifies the instance's data in place and returns None.

    Example:
        # Assuming `instance` is an instance of the class with appropriate data
        paths = ["A/B/C", "D/E"]
        funs = [lambda x: x*2, lambda x: x+1]
        modified_data_list = instance.hard_insert(paths, funs)
    """
    if isinstance(funs, (list,tuple)):
        funs_id = True
    else:
        funs_id = False
    if inplace:
        for id, path in enumerate(paths):
            if funs_id:
                hard_modify(self.data, path, funs[id], inplace)
            else:
                hard_modify(self.data, path, funs, inplace)
    else: 
        results = []
        for id, path in enumerate(paths):
            if funs_id:
                res = hard_modify(self.data, path, funs[id], inplace)
            else:
                res = hard_modify(self.data, path, funs, inplace)

            results.append(res)
        return results

