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
    """
    Returns a list of posts, optionally sorted by title or content
    """
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    # Validate sort field if provided
    if sort_field and sort_field not in ('title', 'content'):
        return jsonify({"error": f"Invalid sort field. Use 'title' or 'content'."}), 400

    # Validate direction if provided
    if direction not in ('asc', 'desc'):
        return jsonify({"error": f"Invalid direction. Use 'asc' or 'desc'."}), 400


    # Sort posts if valid parameters are given
    if sort_field:
        reverse = direction == 'desc'
        sorted_posts = sorted(POSTS, key=lambda x: x[sort_field].lowe(), reverse =reverse)
        return jsonify(sorted_posts), 200

    # Return original order if no sort parameter is found
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



# Attaches the flask app to the PUT route.
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Updates on a particular post by defining its ID by extracting JSON data from the body, and iterating
    over POSTS, then if the ID unique key matches, or the title and content exist, it returns the data as
    a response to the HTTP request.
    :param post_id:
    :return: otherwise, it returns a message to the user that the ID is not found.
    """
    data = request.get_json()

    for post in POSTS:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 200


# Attaches the flask app to the search route.
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Searches posts by title or content by initializing their queries.
    Then returns a result to the user if something is matched based on the title or content.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()


    results = [
        post for post in POSTS
        if title_query in post['title'].lower() or content_query in post['content'].lower()
    ]

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
