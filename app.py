from flask import Flask, jsonify, request
from binarytrees import BinaryTreeNode, RedBlackTreeNode, RedBlackTreeColor
from evaluation import example_evaluation


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return """<h1>Connection Established</h1><p>The HTTP Server is running. Please note, that in order to actually use this service, you have to send POST requests to the implemented routes.</p><p>This page serves no functional purpose.</p>"""


@app.route("/example-route", methods=["POST"])
def example_route():
    """Example route showcasing how a route should be handled.
    It takes the inputs, passes them to an evaluation function elsewhere and then answers with an example score and feedback.
    """
    print("A request has arrived!")
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Get the data
    existing_tree_json_data = data.get("existing_tree")
    student_tree_json_data = data.get("student_tree")
    values = data.get("values")

    # Parse the trees into the structure based on the task (rb-tree or bin-search-tree).
    # (Assuming your task requires an existing tree as input. If not, you can skip it and only parse the student tree.)
    try:
        existing_tree = BinaryTreeNode.from_dict(existing_tree_json_data)
        # existing_tree = RedBlackTreeNode.from_dict(existing_tree_json_data) # In case it would have been a red-black tree
    except:
        jsonify({"error": "Existing tree could not be parsed from JSON"}), 400

    try:
        student_tree = BinaryTreeNode.from_dict(student_tree_json_data)
        # student_tree = RedBlackTreeNode.from_dict(student_tree_json_data) # In case it would have been a red-black tree
    except:
        jsonify({"error": "Student tree could not be parsed from JSON"}), 400

    # Print the received trees to the log if they exist
    if existing_tree:
        print("Here is a text representation of the existing tree:")
        existing_tree.print_tree()

    if student_tree:
        print("Here is a text representation of the student tree:")
        student_tree.print_tree()

    # 1. Solve the task yourself (with existing_tree and or values, depending on task)
    # 2. Compare your solution with the student tree
    # 3. Calculate a score and generate feedback text
    # 4. Send response
    example_score, example_feedback, example_solution = example_evaluation(
        existing_tree, values, student_tree)

    return jsonify({"score": example_score, "feedback": example_feedback, "solution": example_solution.to_dict()})


if __name__ == "__main__":
    app.run()
