from flask import Flask, render_template
import weather
app = Flask(__name__)

@app.route("/")
def index():
    return """<h2>This is your weather info:</h2>
    {}""".format(weather.get_tweet(weather.get_forecast()).replace("\n","<br>"))


#for local testing only
if __name__ == "__main__":
    app.run()
