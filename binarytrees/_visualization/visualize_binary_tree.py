from __future__ import annotations
from typing import TYPE_CHECKING
import graphviz
import base64
from PIL import Image
from io import BytesIO

if TYPE_CHECKING:
    from binarytrees._classes.BinaryTreeNode import BinaryTreeNode
    from binarytrees._classes.RedBlackTreeNode import RedBlackTreeNode


def _get_tree_height(node: BinaryTreeNode | RedBlackTreeNode, show_nil_nodes: bool):
    left = node.get_left_child()
    right = node.get_right_child()
    left_height = (1 if show_nil_nodes else 0) if left is None else _get_tree_height(
        left, show_nil_nodes)
    right_height = (1 if show_nil_nodes else 0) if right is None else _get_tree_height(
        right, show_nil_nodes)
    return max(left_height, right_height) + 1


def _draw_subtree(dot: graphviz.Digraph, show_nil_nodes: bool, node: BinaryTreeNode | RedBlackTreeNode, maxdepth, parent_id="", parent_direction="_", depth=0):
    if node == "NIL":
        if depth < maxdepth:
            node_id = parent_id + parent_direction + "NIL"
            if show_nil_nodes:
                dot.node(node_id, "NIL", ordering="out", fixedsize="True", fillcolor="none",
                         style="filled", fontcolor="black", color="none", fontname="Arial Bold")
                dot.edge(parent_id, node_id, weight="0")
            else:
                dot.node(node_id, "", ordering="out",
                         fixedsize="True", style="invis")
                dot.edge(parent_id, node_id, weight="0", style="invis")
            _draw_subtree(dot, show_nil_nodes, "FILLER",
                          maxdepth, node_id, "<", depth+1)
            _draw_subtree(dot, show_nil_nodes, "FILLER",
                          maxdepth, node_id, "_", depth+1)
            _draw_subtree(dot, show_nil_nodes, "FILLER",
                          maxdepth, node_id, ">", depth+1)
        return
    elif node == "FILLER":
        if depth < maxdepth:
            node_id = parent_id + parent_direction + "FILLER"
            dot.node(node_id, "", ordering="out",
                     fixedsize="True", style="invis")
            dot.edge(parent_id, node_id, weight="1000", style="invis")
        return
    value = node.get_value()
    left = node.get_left_child()
    right = node.get_right_child()
    node_id = parent_id + parent_direction + str(value)
    try:
        color: str | None = str(node.get_color())
    except:
        color: str | None = None
    if (color):
        dot.node(node_id, str(value), ordering="out", fixedsize="True",
                 fillcolor=color, style="filled", fontcolor="white", fontname="Arial Bold")
    else:
        dot.node(node_id, str(value), ordering="out",
                 fixedsize="True", fontname="Arial Bold")
    if parent_id:
        dot.edge(parent_id, node_id, weight="0")
    _draw_subtree(dot, show_nil_nodes, "NIL" if not left else left,
                  maxdepth, node_id, "<", depth+1)
    _draw_subtree(dot, show_nil_nodes, "FILLER",
                  maxdepth, node_id, "_", depth+1)
    _draw_subtree(dot, show_nil_nodes, "NIL" if not right else right,
                  maxdepth, node_id, ">", depth+1)


def generate_binary_tree_image(title, tree: BinaryTreeNode | RedBlackTreeNode, show_nil_nodes: bool) -> str | None:
    """Creates an image of the tree and returns it as a base64 encoded string of a pdf.
    """
    try:
        dot: graphviz.Digraph = graphviz.Digraph()
        dot.attr("graph", center="True", dpi="300", label=title, labelloc="t")
        treeroot = tree
        _draw_subtree(dot, show_nil_nodes, treeroot,
                      _get_tree_height(treeroot, show_nil_nodes))
        dot.format = "png"
        # Get image as binary
        tree_binary = dot.pipe()
        # Encode binary image as Base64
        return base64.b64encode(tree_binary).decode("utf-8")
    except Exception as e:
        raise e


def display_binary_tree_image(b64_image: str | None):
    if not b64_image:
        return
    img = Image.open(BytesIO(base64.b64decode(b64_image)))
    img.show()
