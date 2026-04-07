from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    try:
        pass
    except:
        leaderboard = []

    return render_template("leaderboard.html")

if __name__ == "__main__":
    app.run(debug=True)