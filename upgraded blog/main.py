from flask import Flask, render_template, abort
from datetime import datetime
import requests


app = Flask(__name__)

now = datetime.now()
current_year = now.year

blog_posts_response = requests.get("https://api.npoint.io/2dc49c4d353ae264277f")
blog_posts = blog_posts_response.json()


@app.route("/")
def home():
    return render_template("index.html", current_year=current_year, blog_posts=blog_posts)


@app.route("/about")
def about():
    return render_template("about.html", current_year=current_year)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_year=current_year)


@app.route("/post/<int:post_id>")
def post(post_id):
    # loop through the blog_posts list and find the post with the matching ID
    for blog_post in blog_posts:
        if blog_post["id"] == post_id:
            current_post = blog_post
            break
    else:
        # if no matching post is found, return a 404 error
        return abort(404)

    return render_template("post.html", current_year=current_year, post=current_post)


if __name__ == "__main__":
    app.run(debug=True)
