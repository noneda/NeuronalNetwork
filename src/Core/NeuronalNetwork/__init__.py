import tensorflow as tf
from tensorflow import keras as ks
import numpy as np
import os

# TODO: Esto puede ser un Repository XD
# TODO: Falta Diagramas...
LOAD_PATH = "./model_hours_study_saved.keras"
loaded_model = None

# Datos de entrenamiento por defecto (usados en retrain_model)
study_time = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
exams_note = np.array([(obj * 5) + 50 for obj in study_time], dtype=float)

try:
    if not os.path.exists(LOAD_PATH):
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


def retrain_model(additional_epochs: int = 500, verbose_level: int = 2):
    """
    Carga el modelo existente y lo entrena por épocas adicionales.
    """
    global loaded_model
    global study_time
    global exams_note

    if loaded_model is None:
        print(
            "🛑 Error: No se puede reentrenar. El modelo no fue cargado inicialmente."
        )
        return

    print(
        f"\n--- 🧠 Comenzando Reentrenamiento Adicional ({additional_epochs} Épocas) ---"
    )

    history = loaded_model.fit(
        study_time, exams_note, epochs=additional_epochs, verbose=verbose_level
    )
    print("✅ Reentrenamiento adicional terminado.")

    loss = loaded_model.evaluate(study_time, exams_note, verbose=0)
    print(f"Pérdida (Loss) final después del reentrenamiento: {loss:.6f}")

    print(f"\n--- 💾 Guardando el Modelo Actualizado en {LOAD_PATH} ---")
    loaded_model.save(LOAD_PATH)
    print("✅ Modelo actualizado guardado exitosamente.")

    return history
