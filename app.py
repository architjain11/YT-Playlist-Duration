from flask import Flask, render_template, request
from test import calc

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate")
def newQR():
    url = request.args.get('url')
    loc = url.find("list=")
    if loc!=-1:loc+=5
    else:
        return render_template("index.html", output='Invalid URL')
    url=url[loc:]

    total_seconds = calc(url)

    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    h = str(h)+'hours'
    m = str(m)+'minutes'
    s = str(s)+'seconds'

    return render_template("index.html", output='Playlist duration is: ', h=h, m=m, s=s)