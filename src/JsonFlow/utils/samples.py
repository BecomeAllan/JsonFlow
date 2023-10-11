sample_md = """

Title: 'Teste markdown'


---

# Markdown Features

## Headers

You can create headers of different levels:

```
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6
```

## Emphasis

- *Italic* or _Italic_
- **Bold** or __Bold__
- **_Bold and Italic_** or __*Bold and Italic*__
- ~~Strikethrough~~

## Lists

### Unordered

- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2

### Ordered

1. First item
2. Second item
3. Third item

## Links

[Google](https://www.google.com)

## Images

![Alt text](https://www.example.com/image.jpg)

## Code

Inline `code` snippet.

Code block:

\```
def hello_world():
    print("Hello, World!")
\```

(Note: Remove the `\` before the backticks in the above example.)

## Tables

| Header 1 | Header 2 |
|----------|----------|
| Row1Col1 | Row1Col2 |
| Row2Col1 | Row2Col2 |

## Blockquotes

> This is a blockquote.

## Horizontal Rule

---

Or:

***

Or:

___

## Inline HTML

<details>
  <summary>Click to expand!</summary>
  
  This is a details block, useful for hiding large amounts of content.
</details>

## Task Lists

- [x] Completed task
- [ ] Incomplete task
"""


sample_html = """

<html>
 <body>
  <h1 id="markdown-features">
   Markdown Features
  </h1>
  <h2 id="headers">
   Headers
  </h2>
  <p>
   You can create headers of different levels:
  </p>
  <pre><code># Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6</code></pre>
  <h2 id="emphasis">
   Emphasis
  </h2>
  <ul>
   <li>
    <em>
     Italic
    </em>
    or
    <em>
     Italic
    </em>
   </li>
   <li>
    <strong>
     Bold
    </strong>
    or
    <strong>
     Bold
    </strong>
   </li>
   <li>
    <strong>
     <em>
      Bold and Italic
     </em>
    </strong>
    or
    <strong>
     <em>
      Bold and
Italic
     </em>
    </strong>
   </li>
   <li>
    <del>
     Strikethrough
    </del>
   </li>
  </ul>
  <h2 id="lists">
   Lists
  </h2>
  <h3 id="unordered">
   Unordered
  </h3>
  <ul>
   <li>
    Item 1
   </li>
   <li>
    Item 2
    <ul>
     <li>
      Subitem 2.1
     </li>
     <li>
      Subitem 2.2
     </li>
    </ul>
   </li>
  </ul>
  <h3 id="ordered">
   Ordered
  </h3>
  <ol type="1">
   <li>
    First item
   </li>
   <li>
    Second item
   </li>
   <li>
    Third item
   </li>
  </ol>
  <h2 id="links">
   Links
  </h2>
  <p>
   <a href="https://www.google.com">
    Google
   </a>
  </p>
  <h2 id="images">
   Images
  </h2>
  <figure>
   <img alt="Alt text" src="https://www.example.com/image.jpg"/>
   <figcaption aria-hidden="true">
    Alt text
   </figcaption>
  </figure>
  <h2 id="code">
   Code
  </h2>
  <p>
   Inline
   <code>
    code
   </code>
   snippet.
  </p>
  <p>
   Code block:
  </p>
  <p>
   ``` def hello_world(): print(“Hello, World!”) ```
  </p>
  <p>
   (Note: Remove the
   <code>
    \
   </code>
   before the backticks in the above
example.)
  </p>
  <h2 id="tables">
   Tables
  </h2>
  <table>
   <thead>
    <tr class="header">
     <th>
      Header 1
     </th>
     <th>
      Header 2
     </th>
    </tr>
   </thead>
   <tbody>
    <tr class="odd">
     <td>
      Row1Col1
     </td>
     <td>
      Row1Col2
     </td>
    </tr>
    <tr class="even">
     <td>
      Row2Col1
     </td>
     <td>
      Row2Col2
     </td>
    </tr>
   </tbody>
  </table>
  <h2 id="blockquotes">
   Blockquotes
  </h2>
  <blockquote>
   <p>
    This is a blockquote.
   </p>
  </blockquote>
  <h2 id="horizontal-rule">
   Horizontal Rule
  </h2>
  <hr/>
  <p>
   Or:
  </p>
  <hr/>
  <p>
   Or:
  </p>
  <hr/>
  <h2 id="inline-html">
   Inline HTML
  </h2>
  <details>
   <summary>
    Click to expand!
   </summary>
   This is a details block, useful for hiding large amounts of content.
  </details>
  <h2 id="task-lists">
   Task Lists
  </h2>
  <ul class="task-list">
   <li>
    <input checked="" disabled="" type="checkbox"/>
    Completed task
   </li>
   <li>
    <input disabled="" type="checkbox"/>
    Incomplete task
   </li>
  </ul>
 </body>
</html>
""" 