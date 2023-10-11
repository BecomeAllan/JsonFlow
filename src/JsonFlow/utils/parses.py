from bs4 import BeautifulSoup, NavigableString
import pandoc

# pandoc.configure(auto=True)
# pandoc.configure(read=True)


# def html_to_dict(tag, _current_path=None, _path_occurrences=None):
#     """
#     Recursively convert an HTML structure into a list of dictionaries.

#     This function traverses the HTML tags and generates a dictionary entry for each unique path and value.
    
#     Args:
#     - tag (Tag): The BeautifulSoup tag to be processed.
#     - _current_path (list, optional): List maintaining the current path to the tag.
#                                     Defaults to an empty list.
#     - _path_occurrences (dict, optional): A dictionary tracking the count of occurrences of a specific path.
#                                         Defaults to an empty dictionary.

#     Returns:
#     list: The HTML structure converted into a list of dictionaries.
#     """

#     # If the arguments are None, initialize them
#     if _current_path is None:
#         _current_path = []
#     if _path_occurrences is None:
#         _path_occurrences = {}

#     tag_name = tag.name
#     if tag_name == "[document]":
#         tag_name = "document"

#     # Check if we've encountered this tag before in the current path and update its name if we have.
#     path_str = "/".join(_current_path + [tag_name])
#     tag_count = _path_occurrences.get(path_str, 0)
    
#     if tag_count:
#         tag_count += 1
#         tag_name = f"{tag_name}[{tag_count}]"
#     else:
#         tag_count = 1
    
#     _path_occurrences[path_str] = tag_count

#     # Update the current path
#     _current_path.append(tag_name)

#     results = []

#     # Recursively process all child tags
#     for child in tag.children:
#         if isinstance(child, NavigableString) and child.strip():
#             results.append({'path': '/'.join(_current_path), 'content': child.strip()})
#         elif not isinstance(child, NavigableString):
#             results.extend(html_to_dict(child, _current_path.copy(), _path_occurrences))

#     return results


# Exemplo de uso

# html_doc = """
# <h1 id="titulo-1">Titulo 1</h1>
# <h1 id="titulo-2">Titulo 2</h1>
# <h2 id="subtitulo">Subtitulo</h2>
# <h3 id="subtitulo-1">Subtitulo</h3>
# <ol start="3" type="1">
# <li>Amortização ou liquidação de saldo devedor</li>
# </ol>
# <p>É possível amortizar (abater) parte do saldo devedor ou liquidar toda
# a dívida.</p>
# <p><span class="math inline"><em>x</em><sup>2</sup></span></p>
# <pre class="importante!"><code>Não é possível usar o FGTS para amortizar ou quitar o consórcio
# cujo crédito tenha sido utilizado para aquisição de imóvel.</code></pre>
# <ul>
# <li>Teste
# <ul>
# <li>Teste 1</li>
# <li>Teste 2</li>
# <li>Teste 3 Alguma coisa aqui</li>
# </ul>
# </li>
# </ul>
# """

# dict_html = html_to_dict(html)
# dict_html


def pandoc_to_dict(doc):
    """
    Convert a pandoc document structure into a list of dictionaries.

    This function traverses the pandoc document and generates a dictionary entry
    for each unique path and value.
    
    Args:
    - doc (list): The pandoc document to be processed.

    Returns:
    list: The pandoc document structure converted into a list of dictionaries.
    """

    results = []
    path_occurrences = {}

    def int_to_letter(n, case="low"):
        if n <= 0:
            raise ValueError("Number must be a positive integer")

        if case == "low":
            return chr((n-1) % 26 + ord('A')).lower()
        elif case == "upper":
            return chr((n-1) % 26 + ord('A')).upper()

    def int_to_roman(num, case = "low"):
        if not (0 < num < 4000):
            raise ValueError("Number must be between 1 and 3999")
        
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        roman_num = ''
        i = 0
        while  num > 0:
            for _ in range(num // val[i]):
                roman_num += syms[i]
                num -= val[i]
            i += 1
        
        if case == "low":
            return roman_num.lower()
        else:
            return roman_num

    def update_path_occurrences(current_path):
        """Update and return the path with its occurrence count."""
        if current_path in path_occurrences:
            path_occurrences[current_path] += 1
            current_path += f"[{path_occurrences[current_path]}]"
        else:
            path_occurrences[current_path] = 1
        return current_path

    def process_block(block, current_path, adicional_info):
        """Recursively process a pandoc block."""
        nonlocal results

        # Define behavior for each block type
        # This structure allows for easy expansion and modification
        # for different pandoc block types.
        # Define behavior for each block type
        block_type_handlers = {
            pandoc.types.Header: handle_header,
            pandoc.types.Para: handle_para,
            pandoc.types.Plain: handle_plain,
            pandoc.types.OrderedList: handle_ordered_list,
            pandoc.types.BulletList: handle_bullet_list,
            pandoc.types.LineBlock: handle_line_block,
            pandoc.types.RawBlock: handle_raw_block,
            pandoc.types.CodeBlock: handle_code_block,
            pandoc.types.BlockQuote: handle_block_quote,
            pandoc.types.DefinitionList: handle_definition_list,
            pandoc.types.HorizontalRule: handle_horizontal_rule,
            pandoc.types.Table: handle_table,
            pandoc.types.Image: handle_image,
            pandoc.types.Div: handle_div,
            # list: 
        }


        # Get the handler for the block type and call it
        # print(type(block))
        handler = block_type_handlers.get(type(block))
        if handler:
            handler(block, current_path, adicional_info)
        else:
            # Handle default or unknown block types here, if necessary
            pass

    def handle_header(block, current_path, adicional_info):
        """Handle the Header block type."""
        current_path = f"{current_path}/H{block[0]}"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block[2]),
            "meta": str(block[1])
        })

    def handle_para(block, current_path, adicional_info):
        """Handle the Para block type."""
        current_path = f"{current_path}/P"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block)
        })

    def handle_plain(block, current_path, adicional_info):
        current_path = f"{current_path}/Plain"
        current_path = update_path_occurrences(current_path)

        results.append({
            "path": current_path,
            "text": pandoc.write(block)
        })

    def handle_ordered_list(block, current_path, adicional_info):

        
        styles = {
            pandoc.types.DefaultStyle: lambda num: num,
            pandoc.types.Decimal: lambda num: num,
            pandoc.types.Example: lambda num: num,
            pandoc.types.LowerAlpha: lambda x: int_to_letter(x, "low"), 
            pandoc.types.UpperAlpha: lambda x: int_to_letter(x, "upper"), 
            pandoc.types.LowerRoman: lambda x: int_to_roman(x, "low"), 
            pandoc.types.UpperRoman: lambda x: int_to_roman(x, "upper")
        }

        delims = {
            pandoc.types.DefaultDelim: ("", "."),
            pandoc.types.Period: ("", "."),
            pandoc.types.OneParen: ("", ")"),
            pandoc.types.TwoParens: ("(", ")")
        }


        current_path = f"{current_path}/OrderedList"
        start_num, style, delim = block[0]
        for idx, item in enumerate(block[1]):
            # print(style)
            # print(item)
            info =  (
                styles.get(type(style), lambda num: num)(start_num+idx),
                delims.get(type(delim), ("", ""))
                      )
            info_index = pandoc.types.Str(f"{info[1][0]}{info[0]}{info[1][1]} ")
            # print(info)
            item_path = f"{current_path}/Item[{idx+1}]"
            for subblock in item:
                if isinstance(subblock, pandoc.types.Plain):
                    temp = subblock[0].copy()
                    temp.insert(0, info_index)                    
                    subblock = pandoc.types.Plain(temp)

                process_block(subblock, item_path, info_index)

    def handle_bullet_list(block, current_path, adicional_info):
        current_path = f"{current_path}/BulletList"
        for idx, item in enumerate(block):
            item_path = f"{current_path}/Item[{idx+1}]"
            for subblock in item:
                for subsubblock in subblock:
                    process_block(subsubblock, item_path, adicional_info)

    def handle_line_block(block, current_path, adicional_info):
        current_path = f"{current_path}/LineBlock"
        current_path = update_path_occurrences(current_path)
        # print(block)
        # for line in block:
        results.append({
                "path": current_path,
                "text": pandoc.write(block)
            })

    def handle_raw_block(block, current_path, adicional_info):
        current_path = f"{current_path}/RawBlock"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block),
            "Format": str(block[0])
        })

    def handle_code_block(block, current_path, adicional_info):
        current_path = f"{current_path}/CodeBlock"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block),
            "meta": str(block[0])
        })

    def handle_block_quote(block, current_path, adicional_info):
        current_path = f"{current_path}/BlockQuote"
        for subblock in block:
            process_block(subblock, current_path, adicional_info)

    def handle_definition_list(block, current_path, adicional_info):
        current_path = f"{current_path}/DefinitionList"
        current_path = update_path_occurrences(current_path)
        # print(pandoc.write(block))
        results.append({
            "path": current_path,
            "text": pandoc.write(block),
            # "meta": str(block[0])
        })

        # Some customization for definition list 
        # for idx, item in enumerate(block):
        #     item_path = f"{current_path}/Item[{idx+1}]"
        #     # print(item[0])
        #     for subblock in item[1]:
        #       for idx, definition in enumerate(definitions):
        #           def_path = f"{term_path}/Definition[{idx+1}]"
        #           for subblock in definition:
        #               process_block(subblock, def_path, adicional_info)

    def handle_horizontal_rule(block, current_path, adicional_info):
        current_path = f"{current_path}/HorizontalRule"
        results.append({
            "path": current_path,
            "type": "HorizontalRule",
            "text": "---------\n"
        })

    def handle_table(block, current_path, adicional_info):
        current_path = f"{current_path}/Table"
        current_path = update_path_occurrences(current_path)
        # Here you can add additional processing for specific table elements,
        # such as captions, headers, body, etc.
        results.append({
            "path": current_path,
            "Caption": pandoc.write(block)
        })

    def handle_image(block, current_path, adicional_info):
        current_path = f"{current_path}/Image"
        current_path = update_path_occurrences(current_path)
        for subblock in block[2]:
            process_block(subblock, current_path, adicional_info)

    def handle_div(block, current_path, adicional_info):
        current_path = f"{current_path}/Div"
        current_path = update_path_occurrences(current_path)
        for subblock in block[1]:
            process_block(subblock, current_path, adicional_info)

    # Start processing from the root "Document" path
    current_path = "Document"
    adicional_info = None
    handle_doc = doc.copy()

    for block in handle_doc:
        process_block(block, current_path, adicional_info)

    return results








# # Use como antes, assumindo que 'doc' seja um documento pandoc.
# dict_pandoc = pandoc_to_dict(doc[1])
# dict_pandoc



from bs4 import BeautifulSoup, Tag

def dict_to_html(data, content_key="content", path_key="path", split_tag="/"):
    """
    Convert a list of dictionaries (e.g., from html_to_dict) back into an HTML string.

    Args:
    - data (list of dict): List of dictionaries containing specified path and content keys.
    - content_key (str): The key in the dictionary where the content/text is stored.
    - path_key (str): The key in the dictionary that contains the path of the HTML tag.
    - split_tag (str): The character used to split the path.

    Returns:
    str: Reconstructed HTML string.
    """

    root = BeautifulSoup('', 'html.parser')

    for item in data:
        # Split the path into individual tags and their potential indices
        parts = item[path_key].split(split_tag)
        current = root
        for part in parts:
            # Separate the tag name from its index (if any)
            tag_name, *index = part.split('[')
            if index:
                index = int(index[0].rstrip(']'))
            else:
                index = None

            # Attempt to find the tag by its name and potential index
            found = None
            for idx, child in enumerate(current.children):
                if isinstance(child, Tag) and child.name == tag_name:
                    if index is None or idx == index - 1:
                        found = child
                        break

            # If the tag wasn't found, create it
            if not found:
                new_tag = root.new_tag(tag_name)
                current.append(new_tag)
                current = new_tag
            else:
                current = found

        # Assign the content (text) to the deepest tag in the hierarchy
        current.string = item[content_key]

    return str(root)


# Exemplo de uso
# data = [
#     {'path': 'html/head/title', 'value': 'My title'},
#         {'path': 'document/ul/li[1]', 'value': 'Item 1'},
#         {'path': 'document/ul/li[1]/ul/li', 'value': 'Subitem 1.1'},
#         {'path': 'document/ul/li[2]', 'value': 'Item 2'}]

# html_trns = dict_to_html(dict_html[0:13])

# # print(BeautifulSoup(html_trns, 'html.parser').prettify())

# pandoc_parse_html = pandoc.read(html_trns, format = "html")

# print(pandoc.write(pandoc_parse_html, format="markdown"))
