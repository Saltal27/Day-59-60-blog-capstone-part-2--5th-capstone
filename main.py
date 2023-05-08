from flask import Flask, render_template, abort, request
from datetime import datetime
import requests
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


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


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form["name"].capitalize()
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=60) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs="omarmobarak53@gmail.com",
                    msg=f"Subject: New message from a 'Omar's Blog' user\n\n"
                        f"Name: {name}\n"
                        f"Email: {email}\n"
                        f"Phone Number: {phone}\n"
                        f"Message: {message}\n"
                )
        except smtplib.SMTPException:
            h1 = "Sorry, there was an error sending your message, please try again later."
        else:
            h1 = "Successfully sent your message!"

    else:
        h1 = "Contact Me"
    return render_template("contact.html", current_year=current_year, h1=h1)


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
