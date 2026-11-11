from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Analyze symptoms using Ollama
def analyze_symptoms(details):

    prompt = f"""
    You are a medical information assistant.

    Analyze the following user information:

    {details}

    Provide the following sections:

    1. Symptom Summary
    2. Possible Associated Conditions
    3. Follow-up Questions
    4. General Health Guidance
    5. Recommended Medical Attention

    Important safety rules:
    - Do not provide a medical diagnosis.
    - Do not claim that a condition is confirmed.
    - Mention that possible conditions are only general possibilities.
    - Do not prescribe medicines or dosages.
    - Recommend consulting a qualified doctor.
    - If symptoms suggest an emergency, advise immediate
      emergency medical attention.
    - If information is insufficient, clearly state that.

    End with:
    "This information is not a medical diagnosis."
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    error = ""

    if request.method == "POST":

        age = request.form["age"]
        sex = request.form["sex"]
        symptoms = request.form["symptoms"]
        duration = request.form["duration"]
        severity = request.form["severity"]
        history = request.form["history"]
        medication = request.form["medication"]
        allergies = request.form["allergies"]
        additional = request.form["additional"]

        details = f"""
        Age: {age}
        Sex: {sex}
        Symptoms: {symptoms}
        Duration: {duration}
        Severity: {severity}
        Medical History: {history}
        Medication: {medication}
        Allergies: {allergies}
        Additional Information: {additional}
        """

        try:
            result = analyze_symptoms(details)

        except requests.exceptions.RequestException:
            error = "Ollama is not running. Start Ollama first."

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)