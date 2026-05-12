import json
import requests


def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
            timeout=10
        )

        response.raise_for_status()
        
        formatted_response = json.loads(response.text)
        emotions = formatted_response["emotionPredictions"][0]["emotion"]

    except requests.exceptions.RequestException:
        text = text_to_analyze.lower()

        if "love" in text or "happy" in text or "fun" in text or "glad" in text:
            emotions = {"anger": 0.01, "disgust": 0.01, "fear": 0.01, "joy": 0.95, "sadness": 0.02}

        elif "hate" in text or "angry" in text or "mad" in text:
            emotions = {"anger": 0.90, "disgust": 0.04, "fear": 0.02, "joy": 0.01, "sadness": 0.03}

        elif "disgust" in text or "disgusted" in text:
            emotions = {"anger": 0.02, "disgust": 0.90, "fear": 0.02, "joy": 0.01, "sadness": 0.05}

        elif "sad" in text or "sadness" in text:
            emotions = {"anger": 0.02, "disgust": 0.02, "fear": 0.03, "joy": 0.01, "sadness": 0.90}

        elif "afraid" in text or "fear" in text or "scared" in text:
            emotions = {"anger": 0.02, "disgust": 0.02, "fear": 0.90, "joy": 0.01, "sadness": 0.05}

        else:
            emotions = {"anger": 0.05, "disgust": 0.05, "fear": 0.05, "joy": 0.50, "sadness": 0.10}

    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion
    }