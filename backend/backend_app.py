from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


# Attaches the flask app to the POST route.
@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Creates a new post by loading first the list of POSTS, validates data for the title and content
    , and initializes a new list to store values if there is no title or content, then shows an error
    to the user.
    :return: if there is no title or content, it returns an error to the user.
    Otherwise, it returns the new post.
    """
    new_post = request.get_json()
    # data validation
    title = new_post.get('title')
    content = new_post.get('content')
    if not title or not content:
        missing_fields = []
        if not title:
            missing_fields.append('title')
        if not content:
            missing_fields.append('content')
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields )}"}), 400

    # Generate new ID:
    new_id = max((post['id'] for post in POSTS), default=0) + 1

    # Create new post:
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    POSTS.append(new_post)
    print("The new post created successfully.")
    return jsonify(new_post), 201


# Attaches the flask app to the DELETE route.
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Runs an iteration over POSTS and if the ID unique key matches, deletes it immediately,
    then it returns a message to the user with the deleted post, defined by its ID number.
    :param post_id:
    :return: otherwise, it returns a message to the user that the ID is not found.
    """
    for i, post in enumerate(POSTS):
        if post['id'] == post_id:
            POSTS.pop(i)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
