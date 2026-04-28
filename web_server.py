import os

from database_setup import get_overall_leaderboard
from flask import Flask, render_template, url_for, request

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        print(request.files['userdb'])

        # if 'userdb' not in request.files['userdb']:
        #     return "No database part.", 400

        file = request.files['userdb']
        if file.filename == '':
            return "No selected database.", 400

        dbpath = os.path.join(app.config['UPLOAD_FOLDER'], 'user.db')
        print(dbpath)
        file.save(dbpath)

        try:
            leaderboard = get_overall_leaderboard(path=dbpath)
        except:
            leaderboard = []

        print(leaderboard)

        return render_template("leaderboard.html", scores=leaderboard)
    return render_template("leaderboard.html", scores=[])

if __name__ == "__main__":
    app.run(debug=True)