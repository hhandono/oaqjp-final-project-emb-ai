"""
Server module for Emotion Detection Flask application.
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Analyze text emotions and return formatted response.
    """

    text_to_analyze = request.args.get("textToAnalyze")

    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return str(response)


@app.route("/")
def render_index_page():
    """
    Render the main index page.
    """

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
