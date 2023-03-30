from flask import Flask, render_template

app = Flask(__name__)

# Define routes for the home page and about page
@app.route("/")
def home():
    # Render the home.html template
    return render_template("home.html")

@app.route("/about")
def about():
    # Render the about.html template
    return render_template("about.html")

@app.route("/project")
def project():
    # Render the myproject.html template
    return render_template("myproject.html")

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
