from __future__ import annotations
from binarytrees._visualization.visualize_binary_tree import generate_binary_tree_image, display_binary_tree_image
from typing import Self
from sys import stderr


class BinaryTreeNode:
    """Class representing a node in a binary tree.
    """

    def __init__(self, value: int, left_child: BinaryTreeNode | None = None, right_child: BinaryTreeNode | None = None, parent: BinaryTreeNode | None = None):
        self.set_value(value)
        self._left = left_child
        self._right = right_child
        self._parent = parent

    def __repr__(self) -> str:
        return f"BinaryTreeNode[{str(self.get_value())}]"

    def __eq__(self, other: BinaryTreeNode) -> bool:
        if type(self) != type(other):
            return False
        return self.get_value() == other.get_value()

    def get_value(self) -> int:
        return self._value

    def set_value(self, value: int):
        if value is None:
            raise ValueError("Value cannot be None")
        if not isinstance(value, int):
            raise TypeError("Value must be a numeric type int")
        self._value = value

    def get_left_child(self) -> Self | None:
        return self._left

    def _set_left_child(self, node: Self | None):
        if type(self) == type(node) or node is None:
            self._left = node
        else:
            raise TypeError(
                f"Left child must be a {type(self).__name__} or None")

    def set_left_child(self, node: Self | None):
        self._set_left_child(node)
        if type(self) == type(node):
            node.set_parent(self)

    def get_right_child(self) -> Self | None:
        return self._right

    def _set_right_child(self, node: Self | None):
        if type(self) == type(node) or node is None:
            self._right = node
        else:
            raise TypeError(
                f"Right child must be a {type(self).__name__} or None")

    def set_right_child(self, node: Self | None):
        self._set_right_child(node)
        if type(self) == type(node):
            node.set_parent(self)

    def get_parent(self) -> Self | None:
        return self._parent

    def set_parent(self, node: Self | None):
        if type(self) == type(node) or node is None:
            self._parent = node
        else:
            raise TypeError(f"Parent must be a {type(self).__name__} or None")

    def is_equal_including_subtrees(self, other: Self) -> bool:
        if type(self) != type(other):
            return False
        if self != other:
            return False
        self_left = self.get_left_child()
        other_left = other.get_left_child()
        if self_left is None and other_left is None:
            left_equal = True
        elif self_left is None or other_left is None:
            left_equal = False
        else:
            left_equal = self_left.is_equal_including_subtrees(other_left)
        self_right = self.get_right_child()
        other_right = other.get_right_child()
        if self_right is None and other_right is None:
            right_equal = True
        elif self_right is None or other_right is None:
            right_equal = False
        else:
            right_equal = self_right.is_equal_including_subtrees(other_right)
        return left_equal and right_equal

    def preorder_traverse(self) -> list[Self]:
        traversal = []

        def _preorder_traverse(node: Self):
            if node is not None:
                traversal.append(node)
                _preorder_traverse(node.get_left_child())
                _preorder_traverse(node.get_right_child())
        _preorder_traverse(self)
        return traversal

    def inorder_traverse(self) -> list[Self]:
        traversal = []

        def _inorder_traverse(node: Self):
            if node is not None:
                _inorder_traverse(node.get_left_child())
                traversal.append(node)
                _inorder_traverse(node.get_right_child())
        _inorder_traverse(self)
        return traversal

    def postorder_traverse(self) -> list[Self]:
        traversal = []

        def _postorder_traverse(node: Self):
            if node is not None:
                _postorder_traverse(node.get_left_child())
                _postorder_traverse(node.get_right_child())
                traversal.append(node)
        _postorder_traverse(self)
        return traversal

    def to_dict(self) -> dict[str, any]:
        return {
            "value": self._value,
            "left": self._left.to_dict() if self._left else None,
            "right": self._right.to_dict() if self._right else None,
        }

    def _print_child(self, child: Self | None, level: int, prefix: str):
        if child:
            child.print_tree(level + 1, prefix)
        else:
            print(" " * ((level + 1) * 4) + f"{prefix} null")

    def print_tree(self, level: int = 0, prefix: str = "Root: "):
        print(" " * (level * 4) + prefix + str(self.get_value()))
        self._print_child(self._left, level, "L--> ")
        self._print_child(self._right, level, "R--> ")

    def generate_tree_image(self, title: str | None = None) -> str | None:
        """Returns a Base64 encoded string containing the PNG image of the tree. Optionally add a title to display on the image.
        """
        try:
            return generate_binary_tree_image(title, self, show_nil_nodes=False)
        except Exception as e:
            raise Exception(str(e))

    def display_tree_image(self, title: str | None = None, b64_encoded_tree_image: None | str = None):
        """Display the image of the tree in an image viewer. Optionally include a title to be displayed. 
        If no image is provided, one is generated automatically. 
        If one is provided, the title argument is ignored, since it already has a title.
        """
        try:
            if b64_encoded_tree_image is None:
                b64_encoded_tree_image = self.generate_tree_image(title)
        except Exception as e:
            print("""The image could not be shown. In case the error mentions the Graphviz executable, then please make sure that you have installed Graphviz and configured it correctly on your system. 
Please consult the following error message:""", file=stderr)
            print(e, file=stderr)
        display_binary_tree_image(b64_encoded_tree_image)

    def deep_copy(self) -> Self:
        """Creates and returns a hard copy of the node and all its subnodes.
        The copy can then be modified without changing the original.
        """
        return type(self).from_dict(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> BinaryTreeNode | None:
        if data is None:
            return None
        if not isinstance(data, dict) or "value" not in data.keys():
            raise ValueError(
                "Invalid JSON format: Each node must have a 'value' key")
        node = cls._create_node_from_dict(data)
        if "left" in data and data["left"] is not None:
            node.set_left_child(cls.from_dict(data["left"]))
            node.get_left_child().set_parent(node)
        if "right" in data and data["right"] is not None:
            node.set_right_child(cls.from_dict(data["right"]))
            node.get_right_child().set_parent(node)
        return node

    @classmethod
    def _create_node_from_dict(cls, data: dict[str, any]) -> BinaryTreeNode:
        if "color" in data:
            raise ValueError(
                "BinaryTreeNode does not accept a 'color' attribute")
        return cls(data["value"])
