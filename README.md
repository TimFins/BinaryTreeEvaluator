# Evaluator Microservice for Binary Search Trees and Red-Black Trees

The goal of this project is to build a Python microservice, which provides detailed feedback to students solving binary search tree and red-black tree exercises.
Each task such as inserting values in a binary search tree or deleting values in a red-black tree implements an HTTP route.
A JSON request contains all the information about the task as well as the student's submission. The task is to create the solution, grade the submission, provide detailed feedback and send it back as a JSON response.

## Setup
Please set your working directory to the same directory as this file.

### Prerequisites
#### Software
The programming language [Python](https://www.python.org/downloads/) and the package manager [pip](https://pip.pypa.io/en/stable/installation/) (or alternatively [Anaconda](https://www.anaconda.com/download)) is required.

The Python version should not really matter as long as it is a relatively new one. This project was created with Python version 3.11.5. You should use a Python version >= 3.11.5.

In order to be able to display images, you additionally have to install [Graphviz](https://graphviz.org/) (on top having to install its Python library below).
You can find information on how to install it for your operating system at the [Graphviz download page](https://graphviz.org/download/).

#### Install packages
This project requires the following Python packages:
- Flask (for running the HTTP server)
- Graphviz (for generating PNG images of graphs)
- Pillow (for opening generated PNG images in an image viewer)

The dependencies and exact versions are present in `requirements.txt`
They can be installed directly using pip:
> pip install -r requirements.txt

## Usage
The file `example_usage.py` can be run just like a regular Python script.
The HTTP server has to be started in a different way.

### Start server
You can use Flask to start the HTTP server. We recommend running in debug mode, because this way the server automatically restarts when the code changes, so that you do not have to restart the server manually.
To start the HTTP server run the following command in the command line:
> flask run --debug

If the `flask` command cannot be located correctly, then you can also try:
> python -m flask run --debug

Upon success, an HTTP server starts on localhost. You can terminate it using CTRL+C in the terminal.

Since flask usually takes localhost port 5000, you will probably find your HTTP server there. Alternatively, look for the address in the terminal output. Usually it will look like this:
> * Running on http://127.0.0.1:5000

### Send request to server
If the server runs you can send a request to the given server by e.g., using command line tools like CURL or other API tools like Postman.
You will have to perform a post request on the endpoint and pass the contents as a JSON body.

#### Example body:
You can just use this JSON body as an example:
```json
{"existing_tree":{"value":10,"left":{"value":5,"left":{"value":6,"left":null,"right":null},"right":null},"right":{"value":15,"left":null,"right":null}},"values":[8],"student_tree":{"value":10,"left":{"value":5,"left":{"value":6,"left":null,"right":null},"right":{"value":8,"left":null,"right":null}},"right":{"value":15,"left":null,"right":null}}}
```

#### Example request using cURL
Assuming Flask uses the default port 5000, you can use this cURL command to test the HTTP server.
```sh
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"existing_tree":{"value":10,"left":{"value":5,"left":{"value":6,"left":null,"right":null},"right":null},"right":{"value":15,"left":null,"right":null}},"values":[8],"student_tree":{"value":10,"left":{"value":5,"left":{"value":6,"left":null,"right":null},"right":{"value":8,"left":null,"right":null}},"right":{"value":15,"left":null,"right":null}}}' http://127.0.0.1:5000/example-route
```

#### Example request using PowerShell on Windows
Assuming Flask uses the default port 5000, you can use this command in Windows PowerShell to test the HTTP server.
```sh
Invoke-WebRequest -Uri "http://127.0.0.1:5000/example-route" -ContentType "application/json" -Method POST -Body '{"existing_tree":{"value":10,"left":{"value":5,"left":{"value":6,"left":null,"right":null},"right":null},"right":{"value":15,"left":null,"right":null}},"values":[8],"student_tree":{"value":10,"left":{"value":5,"left":{"value":6,"left":null,"right":null},"right":{"value":8,"left":null,"right":null}},"right":{"value":15,"left":null,"right":null}}}'
```

## HTTP Routing

The `app.py` file serves as the main entry point for handling requests in the Flask application. It defines the available endpoints, processes incoming data, and returns a response. You should implement your endpoints as HTTP POST endpoints.

Examples for requests and responses can be seen further below in the document.

### Request

Each route requires the following JSON input:
- The **student_tree** (the submitted solution, **mandatory**).
- The **existing_tree** (initial state) and/or the **values** (elements to be added or removed, etc.) or **both**, depending on task.

Inside the route's function, the task is programmatically solved using the **BinaryTreeNode** or **RedBlackTreeNode** classes. The student's submission is then evaluated against the expected solution, and feedback with an appropriate score is returned.

The request has the following JSON format:
```json
{
    "existing_tree": ...,
    "values": ...,
    "student_tree": ...
}
```

As an example, the endpoint `/example-route` in `app.py` was defined to showcase basic functionality. This route does the following:
- Accepts input
- Converts the **trees** from JSON to objects using `BinaryTreeNode.from_dict()`.
- Does a trivial grading as example.
- Returns the score and feedback.

### Evaluation functions
Evaluation functions should ideally be stored in the `evaluation` directory. Create a new file containing your evaluations. Import it in `evaluation/__init__.py` and then import it in your route. 


### Response

The response should have an HTTP status code of 200 (OK). The response should include:
- **score** (from 0 to 100)
- **feedback** as text
- **solution** the correct solution graph as JSON

The response has the following JSON format:
```json
{
    "score": ...,
    "feedback": ...,
    "solution": ...
}
```

## Example JSON requests/responses
### Example request for inserting values into a binary search tree
This could be an example input where the task is to insert the values in the existing tree.
In this example the student has correctly created a new node with the value 8 and placed it at the correct location.
*In this example, the student submission is correct.*
```json
{
     "existing_tree":{
          "value":10,
          "left":{
                "value":5,
                "left":{
                     "value":4,
                     "left":null,
                     "right":null
                },
                "right":null
          },
          "right":{
                "value":15,
                "left":null,
                "right":null
          }
     },
     "values": [8],
     "student_tree":{
          "value":10,
          "left":{
                "value":5,
                "left":{
                     "value":4,
                     "left":null,
                     "right":null
                },
                "right":{
                     "value":8,
                     "left":null,
                     "right":null
                }
          },
          "right":{
                "value":15,
                "left":null,
                "right":null
          }
     }
}
```

### Example request for constructing a binary search tree from values
This could be an example input where the task is to create a binary search tree from scratch with the given input `values`.
*In this example, the student submission is correct.*

```json
{
    "existing_tree": null,
    "values": [2, 3, 1, 4],
    "student_tree": {
        "value": 2,
        "left": {
            "value": 1,
            "left": null,
            "right": null
        },
        "right": {
            "value": 3,
            "left": null,
            "right": {
                "value": 4,
                "left": null,
                "right": null
            }
        }
    }
}
```

### Example request for fixing a red-black tree
This could be an example input where the task is fixing the provided red-black tree by restoring red-black properties and performing rebalancing.
Since the job is to only fix the tree instead of adding or removing nodes, the `values` field is null. 
*In this example, the student submission is incorrect.*
```json
{
    "existing_tree": {
        "value": 10,
        "color": "BLACK",
        "left": {
            "value": 5,
            "color": "RED",
            "left": null,
            "right": null
        },
        "right": {
            "value": 15,
            "color": "BLACK",
            "left": null,
            "right": null
        }
    },
    "values": null,
    "student_tree": {
        "value": 10,
        "color": "RED",
        "left": {
            "value": 5,
            "color": "RED",
            "left": null,
            "right": null
        },
        "right": {
            "value": 15,
            "color": "RED",
            "left": null,
            "right": null
        }
    }
}
```

### Example request for inserting values into a red-black tree
This could be an example input where the task is to insert values into an already existing red-black tree.
Note, that the student did not color the root black, violating a red-black tree property.
*In this example, the student submission is incorrect.*
```json
{
    "existing_tree": {
        "value": 1,
        "color": "BLACK",
        "left": null,
        "right": {
            "value": 2,
            "color": "RED",
            "left": null,
            "right": null
        }
    },
    "values": [3, 4],
    "student_tree": {
        "value": 2,
        "color": "RED",
        "left": {
            "value": 1,
            "color": "BLACK",
            "left": null,
            "right": null
        },
        "right": {
            "value": 3,
            "color": "BLACK",
            "left": null,
            "right": {
                "value": 4,
                "color": "RED",
                "left": null,
                "right": null
            }
        }
    }
}
```

### Example response for inserting values into a red-black tree
Assuming that the last example was used as input.
The root has the wrong color, but the rebalancing and insertion was done correctly apart from that.
Assuming, that this results in a deduction of 10 points and the given feedback, the response would look like this (with status code 200):

```json
{
    "score": 90,
    "feedback": "Your solution does not fulfill the rule, that the root node in a red-black tree must be black, since the root with the value 2 is colored red in your submission. You likely just forgot to re-color it after correctly balancing. Everything else is correct.",
    "solution": {
        "value": 2,
        "color": "BLACK",
        "left": {
            "value": 1,
            "color": "BLACK",
            "left": null,
            "right": null
        },
        "right": {
            "value": 3,
            "color": "BLACK",
            "left": null,
            "right": {
                "value": 4,
                "color": "RED",
                "left": null,
                "right": null
            }
        }
    }
}
```

## Classes for working with binary trees

The classes/enums are located in the `binarytrees` package in the `binarytrees/` directory.
These classes/enums should be used, since they have useful functionality for binary tree evaluation.

### Contents
| Class/Enum            | Note                                                                                                                                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **BinaryTreeNode**    | Class representing a node in a binary tree (more information below).                                                                                                         |
| **RedBlackTreeNode**  | Class representing a node in a red-black tree (more information below).                                                                                                      |
| **RedBlackTreeColor** | Enum containing the two possible colors in a red-black tree (red and black). Working with an enum should be safer and more convenient compared to handling strings directly. |

### Usage
The classes/enums are packaged into a Python package. The package can just be imported into the file where it is needed.
They can be imported with an import statement like this:
```py
from binarytrees import BinaryTreeNode, RedBlackTreeNode, RedBlackTreeColor
```

The most relevant functions are showcased in the file `example_usage`, to get familiar with the functionality.

### Most relevant attributes and methods of BinaryTreeNode class

| Method/Attribute                       | Datatype(s)                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **value** _(setter, getter)_           | `int`                                              | Value of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **left_child** _(setter, getter)_      | `BinaryTreeNode` or `None`                         | Left child of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **right_child** _(setter, getter)_     | `BinaryTreeNode` or `None`                         | Right child of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **parent** _(setter, getter)_          | `BinaryTreeNode` or `None`                         | Parent of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **==**                                 | `BinaryTreeNode`                                   | Compares whether two nodes have the same value. Subtrees are not checked.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **is_equal_including_subtrees(other)** | accepts `BinaryTreeNode`                           | Compares whether two nodes have the same value. Additionally makes sure, that the entire left and right subtrees are also equal.                                                                                                                                                                                                                                                                                                                                                                          |
| **preorder_traverse()**                | returns `list[BinaryTreeNode]`                     | Returns the node and its descendants as a list in the order after preorder traversal.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **inorder_traverse()**                 | returns `list[BinaryTreeNode]`                     | Returns the node and its descendants as a list in the order after inorder traversal.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **postorder_traverse()**               | returns `list[BinaryTreeNode]`                     | Returns the node and its descendants as a list in the order after postorder traversal.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **to_dict()**                          | returns `dict[str, any]`                           | Converts node and subtrees to a dictionary, just like the one in the input.                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **print_tree()**                       |                                                    | Prints formatted structure of node and subtrees to STDOUT.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **generate_tree_image(title)**         | optionally accepts `str` or `None`, returns `str`  | Generate a base 64 encoded string containing the tree as PNG, which can e.g., be written to a file. Optionally one can provide a string title, which will be included at the top of the image. If it cannot be generated, an exception is raised containing the original error message. The idea behind this method is, that it can be used for debugging.                                                                                                                                                |
| **display_tree_image(title, img)**     | optionally accepts (`str` or `None`) and `str`     | Generates an image of the tree and displays it in an image viewer. One can optionally provide a title to be shown at the top of the image. One can also provide a base64-encoded string containing the image as input. If none is provided, then one is automatically generated. If an image string is provided, the title is ignored, since the generated image will already have a title. If it cannot be generated or displayed, the user is informed. The idea is, that it can be used for debugging. |
| **deep_copy()**                        | returns `BinaryTreeNode`                           | Creates a deep copy of the node and subtrees. The copy can be modified without affecting the original.                                                                                                                                                                                                                                                                                                                                                                                                    |
| BinaryTreeNode.**from_dict(dict)**     | accepts `dict[str, any]`, returns `BinaryTreeNode` | Class method, which takes a dictionary as input and converts it to a `BinaryTreeNode` with all its subtrees.                                                                                                                                                                                                                                                                                                                                                                                              |


### Most relevant attributes and methods of RedBlackTreeNode class

| Method/Attribute                                        | Datatype(s)                                                                             | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **value** _(setter, getter)_                            | `int`                                                                                   | Value of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **color** _(setter, getter)_                            | `RedBlackTreeColor` or `str`                                                            | Color of the node. Either 'RED' or 'BLACK'. Enum RedBlackTreeColor is used to manage colors.                                                                                                                                                                                                                                                                                                                                                                                                              |
| **left_child** _(setter, getter)_                       | `RedBlackTreeNode` or `None`                                                            | Left child of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **right_child** _(setter, getter)_                      | `RedBlackTreeNode` or `None`                                                            | Right child of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **parent** _(setter, getter)_                           | `RedBlackTreeNode` or `None`                                                            | Parent of the node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **==**                                                  | `RedBlackTreeNode`                                                                      | Compares whether two nodes have the same value and color. Subtrees are not checked.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **is_equal_including_subtrees(other)**                  | accepts `RedBlackTreeNode`                                                              | Compares whether two nodes have the same value and color. Additionally makes sure, that the entire left and right subtrees are also equal.                                                                                                                                                                                                                                                                                                                                                                |
| **preorder_traverse()**                                 | returns `list[RedBlackTreeNode]`                                                        | Returns the node and its descendants as a list in the order after preorder traversal.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **inorder_traverse()**                                  | returns `list[RedBlackTreeNode]`                                                        | Returns the node and its descendants as a list in the order after inorder traversal.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **postorder_traverse()**                                | returns `list[RedBlackTreeNode]`                                                        | Returns the node and its descendants as a list in the order after postorder traversal.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **to_dict()**                                           | returns `dict[str, any]`                                                                | Converts node and subtrees to a dictionary, just like the one in the input.                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **print_tree()**                                        |                                                                                         | Prints formatted structure of node and subtrees to STDOUT.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **generate_tree_image(title)**                          | optionally accepts `str` or `None`, returns `str`                                       | Generate a base 64 encoded string containing the tree as PNG, which can e.g., be written to a file. Optionally one can provide a string title, which will be included at the top of the image. If it cannot be generated, an exception is raised containing the original error message. The idea behind this method is, that it can be used for debugging.                                                                                                                                                |
| **display_tree_image(title, img)**                      | optionally accepts (`str` or `None`) and `str`                                          | Generates an image of the tree and displays it in an image viewer. One can optionally provide a title to be shown at the top of the image. One can also provide a base64-encoded string containing the image as input. If none is provided, then one is automatically generated. If an image string is provided, the title is ignored, since the generated image will already have a title. If it cannot be generated or displayed, the user is informed. The idea is, that it can be used for debugging. |
| **deep_copy()**                                         | returns `RedBlackTreeNode`                                                              | Creates a deep copy of the node and subtrees. The copy can be modified without affecting the original.                                                                                                                                                                                                                                                                                                                                                                                                    |
| RedBlackTreeNode.**from_dict(dict)**                    | accepts `dict[str, any]`, returns `RedBlackTreeNode`                                    | Class method, which takes a dictionary as input and converts it to a `RedBlackTreeNode` with all its subtrees.                                                                                                                                                                                                                                                                                                                                                                                            |
| RedBlackTreeNode.**from_binary_tree_node(node, color)** | accepts `BinaryTreeNode` and (`RedBlackTreeColor` or `str`), returns `RedBlackTreeNode` | Class method, which takes a binary tree node as input and converts it to a `RedBlackTreeNode` with all its subtrees. The color argument determines in which color all the nodes will be colored. The goal is to have a convenient way to convert binary trees to red-black trees for debugging. This method should not be used in evaluation.                                                                                                                                                             |

## Most relevant information for the RedBlackTreeColor enum
| Method/Attribute | Datatype      | Notes                                                |
| ---------------- | ------------- | ---------------------------------------------------- |
| **RED**          | `str`         | Value: `"RED"`.                                      |
| **BLACK**        | `str`         | Value: `"BLACK"`.                                    |
| **str()**        | returns `str` | You can use str(value) to cast the enum to a string. |
