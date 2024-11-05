from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
# load model
dt = pickle.load(open("weather-model.sav", "rb"))


@app.route("/")
def home():
    result = ""
    image_filename = ""  # Default image filename
    return render_template("index.html", **locals())


@app.route("/predict", methods=["POST", "GET"])
def predict():
    result = ""
    image_filename = "default.png"
    precipitation = float(request.form["precipitation"])
    temp_max = float(request.form["temp_max"])
    temp_min = float(request.form["temp_min"])
    wind = float(request.form["wind"])
    result = dt.predict([[precipitation, temp_max, temp_min, wind]])[0]
    result = result.upper()

    # dictionary to map weather type to image
    weather_images = {
        "SUN": "sun.png",
        "RAIN": "rain.png",
        "FOG": "fog.png",
        "SNOW": "snow.png",
        "DRIZZLE": "drizzle.png",
    }

    # Get image filename based weather prediction result
    image_filename = weather_images.get(result, "default.png")

    return render_template("index.html", **locals())


if __name__ == "__main__":
    app.run(debug=True)
