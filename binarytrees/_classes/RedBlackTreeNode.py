from __future__ import annotations
from binarytrees._classes.BinaryTreeNode import BinaryTreeNode
from binarytrees._enums.RedBlackTreeColor import RedBlackTreeColor
from binarytrees._visualization.visualize_binary_tree import generate_binary_tree_image


class RedBlackTreeNode(BinaryTreeNode):
    """Class representing a node in a red-black tree.
    """

    def __init__(self, value: int, color: str = RedBlackTreeColor.RED, left_child: RedBlackTreeNode | None = None, right_child: RedBlackTreeNode | None = None, parent: RedBlackTreeNode | None = None):
        super().__init__(value, left_child, right_child, parent)
        self.set_color(color)

    def __repr__(self) -> str:
        color = str(self.get_color())
        return f"RedBlackTreeNode[{str(self.get_value())}, {color}]"

    def __eq__(self, other: RedBlackTreeNode) -> bool:
        if type(self) != type(other):
            return False
        return self.get_value() == other.get_value() and self.get_color() == other.get_color()

    def get_color(self) -> RedBlackTreeColor:
        return self._color

    def set_color(self, color: str | RedBlackTreeColor):
        if isinstance(color, str):
            try:
                color = RedBlackTreeColor(color)
            except ValueError:
                raise ValueError(
                    f"Invalid color '{color}'. Must be 'RED' or 'BLACK'.")
        if not isinstance(color, RedBlackTreeColor):
            raise TypeError(
                "Color must be an instance of RedBlackTreeColor Enum.")
        self._color = color

    def to_dict(self) -> dict[str, any]:
        return {
            "value": self._value,
            "color": self._color.value,
            "left": self._left.to_dict() if self._left else None,
            "right": self._right.to_dict() if self._right else None,
        }

    def print_tree(self, level: int = 0, prefix: str = "Root: "):
        print(" " * (level * 4) + prefix +
              f"{self.get_value()} ({str(self.get_color())})")
        self._print_child(self._left, level, "L--> ")
        self._print_child(self._right, level, "R--> ")

    def generate_tree_image(self, title: str | None = None) -> str | None:
        """Returns a Base64 encoded string containing the PNG image of the tree. Optionally add a title to display on the image.
        """
        try:
            return generate_binary_tree_image(title, self, show_nil_nodes=True)
        except Exception as e:
            raise Exception(str(e))

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> RedBlackTreeNode | None:
        return super().from_dict(data)

    @classmethod
    def _create_node_from_dict(cls, data: dict[str, any]) -> RedBlackTreeNode:
        if "color" not in data:
            raise ValueError(
                "Invalid JSON format: RedBlackTreeNode requires a 'color' key")
        return cls(data["value"], data["color"])

    @classmethod
    def from_binary_tree_node(cls, binary_tree_node: BinaryTreeNode, color: str | RedBlackTreeColor = RedBlackTreeColor.BLACK) -> RedBlackTreeNode:
        """You can use this method to convert a regular binary tree into a red-black tree. 
        The color you pass is the color in which ALL the nodes will be colored. By default they will all be colored black.
        """
        # parent = BinaryTreeNode.get_parent()
        left = binary_tree_node.get_left_child()
        right = binary_tree_node.get_right_child()
        new_node = cls(binary_tree_node.get_value(), color)
        if left is not None:
            new_left = RedBlackTreeNode.from_binary_tree_node(left, color)
            new_node.set_left_child(new_left)
            new_left.set_parent(new_node)
        if right is not None:
            new_right = RedBlackTreeNode.from_binary_tree_node(right, color)
            new_node.set_right_child(new_right)
            new_right.set_parent(new_node)
        return new_node
