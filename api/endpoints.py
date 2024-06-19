from flask import Blueprint, request, jsonify
import openai
from utils.openai_config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/results_report", methods=["POST"])
def check_health():
    data = request.json

    required_params = [
        "prediction_probability",
        "predicted_class",
        "age",
        "weight",
        "length",
        "sex",
        "bmi",
        "dm",
        "htn",
        "current_Smoker",
        "ex_Smoker",
        "fh",
        "obesity",
        "cva",
        "thyroid_Disease",
        "bp",
        "pr",
        "weak_Peripheral_Pulse",
        "q_Wave",
        "st_Elevation",
        "st_Depression",
        "tinversion",
        "lvh",
        "poor_R_Progression",
        "tg",
        "ldl",
        "hdl",
        "hb",
    ]

    missing_params = [param for param in required_params if param not in data]

    if missing_params:
        return jsonify({"error": "Missing parameters", "missing": missing_params}), 400

    prediction_probability = data.get("prediction_probability")
    predicted_class = data.get("predicted_class")
    age = data.get("age")
    weight = data.get("weight")
    length = data.get("length")
    sex = data.get("sex")
    bmi = data.get("bmi")
    dm = data.get("dm")
    htn = data.get("htn")
    current_Smoker = data.get("current_Smoker")
    ex_Smoker = data.get("ex_Smoker")
    fh = data.get("fh")
    obesity = data.get("obesity")
    cva = data.get("cva")
    thyroid_Disease = data.get("thyroid_Disease")
    bp = data.get("bp")
    pr = data.get("pr")
    weak_Peripheral_Pulse = data.get("weak_Peripheral_Pulse")
    q_Wave = data.get("q_Wave")
    st_Elevation = data.get("st_Elevation")
    st_Depression = data.get("st_Depression")
    tinversion = data.get("tinversion")
    lvh = data.get("lvh")
    poor_R_Progression = data.get("poor_R_Progression")
    tg = data.get("tg")
    ldl = data.get("ldl")
    hdl = data.get("hdl")
    hb = data.get("hb")

    prompt = (
        f"Actúa como un asistente de un cardiólogo. Con los siguientes datos porcentuales de probabilidad de que un paciente específico tenga Enfermedad Arterial Coronaria (EAC), proporciona una lista de recomendaciones que debe tomar el paciente para cuidar su salud. "
        f"La probabilidad de EAC es de {prediction_probability:.2f}% y la predicción de clase de EAC es {'positiva' if predicted_class else 'negativa'}. "
        f"Los datos del paciente son: "
        f"Edad: {age} años, Peso: {weight} kg, Talla: {length} cm, Sexo: {sex}, IMC: {bmi:.2f}, Diabetes: {'Sí' if dm != 0 else 'No'}, Hipertensión: {'Sí' if htn != 0 else 'No'}, "
        f"Fumador actual: {'Sí' if current_Smoker != 0 else 'No'}, Ex fumador: {'Sí' if ex_Smoker != 0 else 'No'}, Historia familiar: {'Sí' if fh != 0 else 'No'}, "
        f"Obesidad: {'Sí' if obesity != 0 else 'No'}, Enfermedad cerebrovascular: {'Sí' if cva != 0 else 'No'}, Enfermedad tiroidea: {'Sí' if thyroid_Disease != 0 else 'No'}, "
        f"Presión arterial: {bp} mmHg, Frecuencia cardíaca: {pr} bpm, Pulso periférico débil: {'Sí' if weak_Peripheral_Pulse != 0 else 'No'}, Onda Q: {'Sí' if q_Wave != 0 else 'No'}, "
        f"Elevación ST: {'Sí' if st_Elevation != 0 else 'No'}, Depresión ST: {'Sí' if st_Depression != 0 else 'No'}, Inversión T: {'Sí' if tinversion != 0 else 'No'}, "
        f"Hipertrofia ventricular izquierda: {'Sí' if lvh != 0 else 'No'}, Progresión pobre R: {'Sí' if poor_R_Progression != 0 else 'No'}, "
        f"Triglicéridos: {tg} mg/dL, LDL: {ldl} mg/dL, HDL: {hdl:.2f} mg/dL, Hemoglobina: {hb:.2f} g/dL."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de un médico cardiólogo."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        answer = response.choices[0]["message"]["content"].strip()
        return jsonify({"message": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
