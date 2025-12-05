import tensorflow as tf
from tensorflow import keras as ks
import numpy as np
import os


LOAD_PATH = "./model_hours_study_saved"
loaded_model = None

try:
    if not os.path.isdir(LOAD_PATH):
        raise FileNotFoundError(f"El directorio del modelo no existe en: {LOAD_PATH}")

    print("Cargando el modelo de Keras (Formato SavedModel)...")

    loaded_model = ks.models.load_model(LOAD_PATH)
    print("✅ Modelo cargado exitosamente.")

except FileNotFoundError as e:
    print(f"❌ ERROR: {e}")
    print(
        "Asegúrate de ejecutar el script de entrenamiento con model.export() primero."
    )

except Exception as e:
    print(f"❌ ERROR inesperado al cargar el modelo: {e}")


def predict_note(hours: float):
    """
    Función de predicción para la nota de examen.
    """
    if loaded_model is None:
        return {"error": "Modelo no cargado. Revisa los logs de inicio."}

    try:
        input_data = np.array([[hours]], dtype=np.float32)

        prediction = loaded_model.predict(input_data)[0][0]

        return {
            "hours_studied": hours,
            "predicted_note": float(prediction),
        }
    except Exception as e:
        return {"error": f"Error durante la predicción: {str(e)}"}
