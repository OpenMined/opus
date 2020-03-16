from flask import Flask, Response
app = Flask(__name__)

@app.route("/")
def hello():
    return Response("Hello World!")
if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
