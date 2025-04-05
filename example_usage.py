"""This file just seves to show you what you can do with the Binary Tree Classes.
"""

import json
from binarytrees import BinaryTreeNode, RedBlackTreeNode, RedBlackTreeColor

# Example tree as JSON
tree_json = """
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
"""

# Convert JSON to Python dictionary
json_as_dict = json.loads(tree_json)
student_tree_dict = json_as_dict["student_tree"]

# Create a binary tree object from tree dictonary
root = BinaryTreeNode.from_dict(student_tree_dict)

# Print root
print("Print root:")
print(root)

# Print value of root
print("Print value of root:")
print(root.get_value())

# Get left child and right child of root
left_child = root.get_left_child()
right_child = root.get_right_child()
print("Left child of root:")
print(left_child)
print("Right child of root:")
print(right_child)

# Get left child of left child
print("Left child of left child of root:")
print(left_child.get_left_child())

# Get parent of root's left child (root itself)
print("Parent of left child of root (root itself):")
print(left_child.get_parent())

# Create a copy of the tree, which can then be modified without changing the original tree
copy_root = root.deep_copy()
copy_root.get_right_child().set_value(42)
copy_root.get_right_child().set_right_child(None)
print("Original tree:")
root.print_tree()
print("Copied and modified tree:")
copy_root.print_tree()

# Check if root and copy root are equal.
# The equality operator only compares value (and color in case of red-black trees.)
print("Root and copy root nodes are equal:")
print(root == copy_root)

# To also make sure, that not only the nodes, but also the left and right subtrees are equal,
# use the method is_equal_including_subtrees().
# Even though the root was unchanged, this comparison returns False,
# since the right subtree was modified (One node removed and another changed value).
print("Root and copy root nodes are equal and have the same subtrees:")
print(root.is_equal_including_subtrees(copy_root))

# Display tree as image in separate image viewer instead of in terminal
root.display_tree_image("Original Tree")
copy_root.display_tree_image("Copied & Modified Tree")

# In case you do not want to save the image to a file instead,
# you can do this after creating a new png file and adjusting the path:

"""
import base64
tree_image_b64string = root.generate_tree_image()
PATH = r"INSERT/ABSOLUTE/PATH/TO/IMAGE.png"
with open(PATH, "wb") as f:
    f.write(base64.b64decode(tree_image_b64string))
"""
