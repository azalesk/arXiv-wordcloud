from flask import Flask, render_template, request
from urllib import parse, request as urlreq
import feedparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt#, mpld3
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/",methods=["GET"])
@app.route("/index/")
def index():
    fname = request.args.get("first")
    lname = request.args.get("last")
    if lname is None or lname == '':
        return render_template("index.html")
    elif fname is None or fname == "":
        fname = "*"
        name = lname
    elif len(fname) == 1 or fname[1] == ".":
        fname = fname[0]
        name = fname[0] + ". " + lname
    else:
        name = fname + " " + lname
    author = lname + "_" + fname
    
    max_results = 50
    query = "http://export.arxiv.org/api/query?"
    query += "search_query=au:" + author
    query += "&start=0&max_results=%i" % (max_results)

    response = urlreq.urlopen(query).read()
    feed = feedparser.parse(response)

    text = ""

    for entry in feed.entries:
        text = text + " " + entry.summary

    if text == "":
        return render_template("index.html")
    
    wordcloud = WordCloud(background_color="white",
                              width=800, height=600,
                              max_font_size=100, max_words=100,
                              stopwords=None).generate(text)
    plt.figure(figsize=(8, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    figfile = BytesIO()
    plt.savefig(figfile, format="png")
    figfile.seek(0)  
    figdata_png = parse.quote(base64.b64encode(figfile.read()).decode())

    return render_template("index.html", name=name, PLOTSTR=figdata_png)
        #results=mpld3.fig_to_html(f)
