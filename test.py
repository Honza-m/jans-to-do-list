from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "THIS IS THE INDEX PAGE!"

if __name__ == "__main__":
    app.run()
