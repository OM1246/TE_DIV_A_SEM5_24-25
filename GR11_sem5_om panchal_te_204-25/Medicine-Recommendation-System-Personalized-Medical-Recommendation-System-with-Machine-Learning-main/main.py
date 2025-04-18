from flask import Flask, request, render_template, jsonify  # Import jsonify
import numpy as np
import pandas as pd
import pickle

# Flask app
app = Flask(__name__)

# Load datasets
sym_des = pd.read_csv(
    r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\symtoms_df.csv"
)
precautions = pd.read_csv(
    r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\precautions_df.csv"
)
workout = pd.read_csv(
    r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\workout_df.csv"
)
description = pd.read_csv(
    r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\description.csv"
)
medications = pd.read_csv(
    r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\medications.csv"
)
diets = pd.read_csv(
    r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\diets.csv"
)

# Load model
svc = pickle.load(
    open(
        r"C:\Users\ASUS\OneDrive\Documents\HELLO\Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning-main\svc.pkl",
        "rb",
    )
)


# Helper function to get disease details
def helper(dis):
    desc = description[description["Disease"] == dis]["Description"]
    desc = " ".join([w for w in desc])

    pre = precautions[precautions["Disease"] == dis][
        ["Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"]
    ]
    pre = [col for col in pre.values]

    med = medications[medications["Disease"] == dis]["Medication"]
    med = [med for med in med.values]

    die = diets[diets["Disease"] == dis]["Diet"]
    die = [die for die in die.values]

    wrkout = workout[workout["disease"] == dis]["workout"]

    return desc, pre, med, die, wrkout


# Symptoms and diseases dictionary
symptoms_dict = {
    "itching": 0,
    "skin_rash": 1,
    "nodal_skin_eruptions": 2,
    "continuous_sneezing": 3,
    "shivering": 4,
    "chills": 5,
    "joint_pain": 6,
    "stomach_pain": 7,
    "acidity": 8,
    "ulcers_on_tongue": 9,
    "muscle_wasting": 10,
    "vomiting": 11,
    "burning_micturition": 12
}

diseases_list = {
    15: "Fungal infection",
    4: "Allergy",
    16: "GERD",
    9: "Chronic cholestasis",
    14: "Drug Reaction",
    33: "Peptic ulcer disease",
    1: "AIDS",
    12: "Diabetes"
}


# Model prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]


# Flask routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        symptoms = request.form.get("symptoms")
        if symptoms == "Symptoms":
            message = (
                "Please either write symptoms or you have written misspelled symptoms"
            )
            return render_template("index.html", message=message)
        else:
            user_symptoms = [s.strip() for s in symptoms.split(",")]
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(
                predicted_disease
            )

            my_precautions = [i for i in precautions[0]]

            return render_template(
                "index.html",
                predicted_disease=predicted_disease,
                dis_des=dis_des,
                my_precautions=my_precautions,
                medications=medications,
                my_diet=rec_diet,
                workout=workout,
            )

    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/developer")
def developer():
    return render_template("developer.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


if __name__ == "__main__":
    app.run(debug=True)
