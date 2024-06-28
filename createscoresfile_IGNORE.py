import json

scores_json = {
    "15": [],
    "30": [],
    "60": []
}


def create_scores_file():
    with open("scores.json", "w") as scores_file:
        json.dump(scores_json, scores_file)
