# import necessary libraries
import getResult

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<lat>/<lng>/<category>")
def calcResult(lat, lng, category):


    result = getResult.getResult(lat, lng, category)    
    
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
