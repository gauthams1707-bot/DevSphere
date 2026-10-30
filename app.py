
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from database import (
    initialize_database,
    create_post,
    get_all_posts,
    get_post_by_id,
    update_post,
    delete_post,
    search_posts,
    get_posts_by_category,
    get_post_count
)

import os

# Initialize Flask application
app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "devsphere-local-development-key"
)

# Available blog categories
CATEGORIES = [
    "Java",
    "Python",
    "Artificial Intelligence",
    "Web Development"
]

# Initialize database
initialize_database()


# HOME PAGE
@app.route("/")
def home():

    search_query = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    if search_query:
        posts = search_posts(search_query)

    elif category and category in CATEGORIES:
        posts = get_posts_by_category(category)

    else:
        posts = get_all_posts()

    total_posts = get_post_count()

    return render_template(
        "index.html",
        posts=posts,
        categories=CATEGORIES,
        search_query=search_query,
        selected_category=category,
        total_posts=total_posts
    )


# VIEW SINGLE BLOG ARTICLE
@app.route("/article/<int:post_id>")
def article(post_id):

    post = get_post_by_id(post_id)

    if post is None:
        abort(404)

    return render_template(
        "article.html",
        post=post
    )


# CREATE NEW BLOG ARTICLE
@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "Admin").strip() or "Admin"

        if not all([title, category, excerpt, content]):
            flash("Please fill in all required fields.", "error")

        elif category not in CATEGORIES:
            flash("Please select a valid category.", "error")

        else:
            create_post(
                title,
                category,
                excerpt,
                content,
                author
            )

            flash("Your article was published successfully!", "success")

            return redirect(url_for("home"))

    return render_template(
        "create.html",
        categories=CATEGORIES,
        post=None
    )


# EDIT EXISTING BLOG ARTICLE
@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):

    post = get_post_by_id(post_id)

    if post is None:
        abort(404)

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()

        if not all([title, category, excerpt, content]):
            flash("Please fill in all required fields.", "error")

        elif category not in CATEGORIES:
            flash("Please select a valid category.", "error")

        else:
            update_post(
                post_id,
                title,
                category,
                excerpt,
                content
            )

            flash("Article updated successfully!", "success")

            return redirect(
                url_for("article", post_id=post_id)
            )

    return render_template(
        "create.html",
        categories=CATEGORIES,
        post=post
    )


# DELETE BLOG ARTICLE
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):

    post = get_post_by_id(post_id)

    if post is None:
        abort(404)

    delete_post(post_id)

    flash("Article deleted successfully!", "success")

    return redirect(url_for("home"))


# ABOUT PAGE
@app.route("/about")
def about():

    return render_template("about.html")


# CONTACT PAGE
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, message]):
            flash("Please complete all contact fields.", "error")

        elif len(name) > 100 or len(email) > 254 or len(message) > 3000:
            flash("Your message exceeds the allowed length.", "error")

        elif "@" not in email:
            flash("Please enter a valid email address.", "error")

        else:
            flash(
                "Thank you for contacting us! "
                "This demo form does not send emails yet.",
                "success"
            )

            return redirect(url_for("contact"))

    return render_template("contact.html")


# PAGE NOT FOUND
@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


# RUN APPLICATION
if __name__ == "__main__":

    print("===================================")
    print("   DevSphere Blog Application")
    print("   Starting Flask Server...")
    print("===================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
