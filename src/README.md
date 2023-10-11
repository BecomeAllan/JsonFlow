# JsonFlow

## Introduction
JsonFlow is a robust Python library designed to seamlessly manipulate and traverse nested JSON data structures (and Python dictionaries). It provides intuitive functionalities for deep data extraction, modification, and inspection, making it an essential tool for developers working with complex JSON structures. Whether you're handling configuration files, API responses, or data storage, JsonFlow streamlines the process, giving you the power to interact with JSON like never before.



## Features

- **Pseudo Formatting**: Get a formatted, bird's-eye view of your JSON structure, making it easier to understand the nested relationships within.
- **Customizable Query Mechanism**: Use lambda functions, string paths, and more to selectively extract or modify parts of your JSON.
- **Soft & Hard Insertion**: Whether you're looking to non-destructively manipulate your data or dive deep with modifications, JsonFlow has got you covered.
- **Flatten and Structure**: Easily flatten deep JSON structures to a linear format or restructure them as per your requirements.

## Examples

Let's dive into some of the key features with example usages where:

```python
from JsonFlow import JsoniFy

data = JsoniFy(some_dict)
```


### 1. Pseudo Formatting

Using `pseudo_format()`, you can get a visual representation of your JSON structure:

```python
data.pseudo_format()

# Output:
- A
|   - B (list[dict])
|   |   - C
|   |   |   - Text (str)
|   |   - D (str)
|   - E
|   |   - Text (str)
- F
|   - G
|   |   - H (str)
|   - I (int)
```

### 2. Customizable Query Mechanism

Retrieve or modify selective parts of your JSON:

```python
output = data({
    "A": {
        "B":[{
            "C": {"Text": lambda x: x.upper()}
        }],
        "E":True
    },
    "F": {
        "I": True
    }
})
```

### 3. Soft Insertion

Use `soft_insert()` to apply a custom function across your JSON without destroying the original structure:

```python
def custom_value_func_embed(key, value):
    if isinstance(value, dict):
      # print(value.keys())
      if 'Text' in value.keys():
          return value.update({f"Embed({value['Text']})": len(value["Text"])})
    return None

data.soft_insert(custom_value_func_embed, inplace = False)

# result
{
  "A": {
    "B": [
      {
        "C": {
          "Text": "Test text",
          "Embed(Test text)": 9
        },
        "D": "Value2"
      },
      {
        "C": {
          "Text": "Test text",
          "Embed(Test text)": 9
        },
        "D": "Value2"
      }
    ],
    "E": {
      "Text": "Test text 2 E",
      "Embed(Test text 2 E)": 13
    }
  },
  "F": {
    "G": {
      "H": "Value4"
    },
    "I": 3
  }
}
```

### 4. Hard Insertion

For deeper, structural modifications, leverage `hard_insert()`:

```python
data_test = data.hard_insert(["A/B"], deep_merge)
```

### 5. Flattening and Structuring

Easily switch between deep and linear representations:

```python
def fu(x):
  return str(x)

output = flatten_dict(data, func = fu)
# result
[
  {
    "path": "Doc[1]/A/B[1]/C/Text",
    "content": "Test text"
  },
  {
    "path": "Doc[1]/A/B[1]/D",
    "content": "Value2"
  },
  {
    "path": "Doc[1]/A/B[2]/C/Text",
    "content": "Test text"
  },
  {
    "path": "Doc[1]/A/B[2]/D",
    "content": "Value2"
  },
  {
    "path": "Doc[1]/A/E/Text",
    "content": "Test text 2 E"
  },
  {
    "path": "Doc[1]/F/G/H",
    "content": "Value4"
  },
  {
    "path": "Doc[1]/F/I",
    "content": "3"
  }
]
```

```python
res = [{'path': 'A/B[1]', 'content': {"text": "hi", "age":10}},
       {'path': 'A/B[2]', 'content': {"text": "hi", "age":10}},
       {'path': 'A/B[3]', 'content': {"text": "hi2", "age":10}}]

structure_data(res, nested=True,
            adjust_list=True,
            keys_content = ["text"])

# result
{'A': {'B': [{'text': 'hi', 'age': 10},
   {'text': 'hi', 'age': 10},
   {'text': 'hi2', 'age': 10}]}}

structure_data(res, nested=True,
              adjust_list=False,
              keys_content = ["text"])

# result
{'A': {'B[1]': {'text': 'hi', 'age': 10},
  'B[2]': {'text': 'hi', 'age': 10},
  'B[3]': {'text': 'hi2', 'age': 10}}}
```

## Conclusion

JsonFlow is your go-to solution for anything JSON in Python. With its vast array of features and user-friendly interface, your JSON-related tasks will feel like a breeze. Dive in, explore, and let JsonFlow take your JSON game to the next level.