# JsonFlow (beta)

## Introduction
JsonFlow is a robust Python library designed by @BecomeAllan to seamlessly manipulate and traverse nested JSON data structures (and Python dictionaries). It provides intuitive functionalities for deep data extraction, modification, and inspection, making it an essential tool for developers working with complex JSON structures. Whether you're handling configuration files, API responses, data storage, AI pipelines... JsonFlow streamlines the process, giving you the power to interact with JSON like never before.

---

JsonFlow was built entirely in Python, ensuring a smooth experience without external dependencies. To install, simply use:

```
!pip install -q JsonFlow
```

---
# **JsonFlow: Powering Ecosystems of Applications and Pipelines**

The JsonFlow library is not just a tool—it's a game-changer. Crafted with precision and vision, it's designed to empower developers to create entire ecosystems of applications and pipelines, enhancing readability and facilitating seamless integration with various platforms. The drive behind this initiative is to harness the vast potential of both structured and unstructured data, ensuring that the inherent information is not just accessible, but also utilizable to its fullest.

JsonFlow is not just a library; it's a framework. It's aimed at being the cornerstone for automating tasks, whether they're rooted in data exploration or agile development. As we venture into the future, our roadmap for JsonFlow includes:

+ [ ] Developing a build in the Mojo language, bringing the velocity of C/C++ to Python.
+ [ ] Integrating with vectorized/Tensor operations from libraries such as NumPy and PyTorch. This will streamline the construction of training/inference pipelines more easily for machine learning and deep learning models, enhancing the full potential of the automation process.
+ [ ] Implementing automatic process management, ensuring the efficiency of your pipelines, and providing comprehensive logs to monitor behavior and performance.

By choosing JsonFlow, you're not just selecting a tool, but aligning with a vision for a more integrated, efficient, and data-driven future.


## Core Features

- **Pseudo Formatting**: Get a formatted, bird's-eye view of your JSON structure, making it easier to understand the nested relationships within.
- **Customizable Query Mechanism**: Use lambda functions, string paths, and more to selectively extract or modify parts of your JSON.
- **Soft & Hard Insertion**: Whether you're looking to non-destructively manipulate your data or dive deep with modifications, JsonFlow has got you covered.
- **Flatten and Structure**: Easily flatten deep JSON structures to a linear format or restructure them as per your requirements.

## Examples

Let's dive into some of the key features with example usages where:

```python
from JsonFlow import JsoniFy

some_dict = {
    "A": {
        "B": [
         {
            "C": {
                "Text": "Test text"
            },
            "D": "Value2"
        },
         {
            "C": {
                "Text": "Test text"
            },
            "D": "Value2"
        },   
        ],
        "E": {
            "Text": "Test text 2 E"
        }
    },
    "F": {
        "G": {
            "H": "Value4"
        },
        "I": 3
        }
}

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

### 2. Customizable /Query Mechanism

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
# result
{
  "A": {
    "B": [
      {
        "C": {
          "Text": "TEST TEXT"
        }
      },
      {
        "C": {
          "Text": "TEST TEXT"
        }
      }
    ],
    "E": {
      "Text": "Test text 2 E"
    }
  },
  "F": {
    "I": 3
  }
}


# or query via path

data.query_path("A/B/C")
# result
[{'Text': 'Test text'}, {'Text': 'Test text'}]

```

### 3. Soft Insertion

Use `soft_insert()` to apply a custom function across your JSON:

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

For specific structural modifications, leverage `hard_insert()`:

```python
from JsonFlow import deep_merge

data_test = data.hard_insert(["A/B"], deep_merge)

# Result
[
    {'A': {
        'B': {
            'C': {
                'Text': ['Test text', 'Test text']
                },
            'D': ['Value2', 'Value2']},
        'E': {'Text': 'Test text 2 E'}
        },
     'F': {
        'G': {'H': 'Value4'},
        'I': 3}}
]
```

### 5. Flattening and Structuring

Easily switch between deep and linear representations:

```python

from JsonFlow import flatten_dict

def fu(x):
  return str(x)

output = flatten_dict(data.data, func = fu)
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
from JsonFlow import structure_data

res = [{'path': 'A/B[1]', 'content': {"text": "hi", "age":10}},
       {'path': 'A/B[2]', 'content': {"text": "hi", "age":10}},
       {'path': 'A/B[3]', 'content': {"text": "hi2", "age":10}}]

structure_data(res, nested=True,
            adjust_list=True,
            keys_content = ["text"])

# result
{'A': {'B': [{'text': 'hi'},
   {'text': 'hi'},
   {'text': 'hi2'}]}}

structure_data(res, nested=True,
              adjust_list=False,
              keys_content = ["text"])

# result
{'A': {'B[1]': {'text': 'hi'},
  'B[2]': {'text': 'hi'},
  'B[3]': {'text': 'hi2'}}}
```

### 6. Regex


Find the relevant keys or values in your JSON:

```python

from JsonFlow import find_keys_by_regex, find_values_by_depth


some_dict = {
    "A": {
        "B": [
         {
            "1C": {
                "Text": "Test text"
            },
            "D": "Value2"
        },
         {
            "2C": {
                "Text": "Test text"
            },
            "D": "Value2"
        },   
        ],
        "E": {
            "Text": "Test text 2 E"
        }
    },
    "F": {
        "G": {
            "H": "Value4"
        },
        "I": 3
        }
}


find_keys_by_regex(some_dict, r"\d.", return_type="dict")

# {'A': {'B': {0: {'1C': {'Text': 'Test text'}},
#    1: {'2C': {'Text': 'Test text'}}}}}

find_keys_by_regex(some_dict, r"\d.", return_type="list")

# ['A/B/0/1C', 'A/B/1/2C']

find_values_by_depth(some_dict, r'Value.')

# [(['A', 'B', 0, 'D'], 'Value2'),
#  (['A', 'B', 1, 'D'], 'Value2'),
#  (['F', 'G', 'H'], 'Value4')]
```

### Utility functions (Merge)

Some additional useful features


```python

content_to_merge = [
    {"test": ["value1", "value2"],
     "adicional_info": {"label": "label_value1"}},
    {"test": "value3",
     "adicional_info": {"label": "label_value2"}},
    {"test": {"content": "valu3"},
     "adicional_info": {"label": "label_value3"}},
] 

###

merge_content(content_to_merge)

### output
{'test': [
    ['value1', 'value2'],
    'value3',
     {'content': 'valu3'}
    ],
 'adicional_info': [
    {'label': 'label_value1'},
    {'label': 'label_value2'},
    {'label': 'label_value3'}
]}

###

deep_merge(content_to_merge)

### output
{'test': [
    ['value1', 'value2'],
    'value3',
    {'content': 'valu3'}
    ],
 'adicional_info': {
    'label': [
        'label_value1',
        'label_value2',
        'label_value3'
        ]}}

```

---

### Parsers

To utilize the parsers built for JsonFlow, follow these steps:

```
!wget https://github.com/jgm/pandoc/releases/download/2.19.2/pandoc-2.19.2-1-amd64.deb -O pandoc-2.19.2-1-amd64.deb
!dpkg -i pandoc-2.19.2-1-amd64.deb

!pip install --upgrade -q pandoc==2.3 beautifulsoup4
!pip install -q JsonFlow[parse]
```

an now you have the pandoc library to integrate to any possibility of document to document, see [pandoc](https://pandoc.org/) or the library of python in [Python pandoc](https://github.com/boisgera/pandoc).


```python
import pandoc
from JsonFlow.utils import pandoc_to_dict, dict_to_html
from JsonFlow.utils import sample_html, sample_md




doc_p = pandoc.read(sample_md, format= "markdown")

pandoc_to_dict(doc_p[1])

# output
[{'path': 'Document/H1',
  'text': 'Markdown Features\n',
  'meta': "('markdown-features', [], [])"},
 {'path': 'Document/H2', 'text': 'Headers\n', 'meta': "('headers', [], [])"},
 {'path': 'Document/P',
  'text': 'You can create headers of different levels:\n'},
...
 {'path': 'Document/BulletList/Item[1]/Plain[7]',
  'text': '☒ Completed task\n'},
 {'path': 'Document/BulletList/Item[1]/Plain[8]',
  'text': '☐ Incomplete task\n'}]

####

data = [
    {'path': 'html/head/title', 'content': 'My title'},
        {'path': 'document/ul/li[1]', 'content': 'Item 1'},
        {'path': 'document/ul/li[1]/ul/li', 'content': 'Subitem 1.1'},
        {'path': 'document/ul/li[2]', 'content': 'Item 2'}]

html_trns = dict_to_html(data[0:13])

### output
# <html>
#  <head>
#   <title>
#    My title
#   </title>
#  </head>
# </html>
# <document>
#  <ul>
#   <li>
#    Item 1
#    <ul>
#     <li>
#      Subitem 1.1
#     </li>
#    </ul>
#   </li>
#   <li>
#    Item 2
#   </li>
#  </ul>
# </document>


pandoc_parse_html = pandoc.read(html_trns, format = "html")

print(pandoc.write(pandoc_parse_html, format="markdown"))

## Output

# -   Item 1
#     -   Subitem 1.1
# -   Item 2
```


---

## Contributions

Feel free to help build this ecosystem, with applications from parses to pipelines, search engines, and ML engines. This library was designed to improve AI models but can handle much more technology. Soon, we will have a repository to archive the more useful pieces of code of day life.


## Conclusion

JsonFlow is your go-to solution for anything JSON in Python. With its vast array of features and user-friendly interface, your JSON-related tasks will feel like a breeze. Dive in, explore, and let JsonFlow take your JSON game to the next level.


---

**Disclaimer**: While every effort has been made to ensure the accuracy and reliability of the JsonFlow library, the author and contributors cannot guarantee that it is free from defects. Users are advised to ensure that the library meets their requirements before integrating it into their projects. The author disclaims all warranties, either express or implied, including but not limited to any implied warranties of merchantability or fitness for a particular purpose. In no event shall the author be liable for any damages, including but not limited to special, direct, indirect, or consequential damages, losses, or expenses arising in connection with this library or its use.

Furthermore, I am a member of the academic community, and I would be immensely flattered if you could cite this work when utilizing JsonFlow in your projects or publications.

[![DOI](https://zenodo.org/badge/703299059.svg)](https://zenodo.org/badge/latestdoi/703299059)

---
