import tensorflow as tf
from tensorflow import keras as ks
import numpy as np
import os

SAVE_PATH = "./model_hours_study_saved.keras"

if os.path.exists(SAVE_PATH) and not os.path.isdir(SAVE_PATH):
    print(f"--- 🔄 Cargando Modelo Existente de: {SAVE_PATH} ---")
    try:
        model = ks.models.load_model(SAVE_PATH)
        print("✅ Modelo cargado exitosamente. No se requiere reentrenamiento.")
    except Exception as e:
        print(f"❌ Error al cargar el modelo. Lo reentrenaremos: {e}")
        model = None
else:
    model = None


if model is None:
    print("--- 🆕 Creando y Entrenando Nuevo Modelo ---")

    study_time = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    exams_note = np.array([(obj * 5) + 50 for obj in study_time], dtype=float)

    model = ks.Sequential()
    model.add(ks.layers.Dense(units=1, input_shape=[1]))
    model.summary()

    model.compile(optimizer="adam", loss="mean_squared_error")

    print("\n--- 🧠 Comenzando el Entrenamiento (2000 Épocas) ---")
    model.fit(study_time, exams_note, epochs=2000, verbose=3)
    print("✅ Entrenamiento terminado.")

    loss = model.evaluate(study_time, exams_note, verbose=0)
    print(f"Pérdida (Loss) final del modelo: {loss:.6f}")

    print(f"\n--- 💾 Guardando el Modelo en {SAVE_PATH} ---")
    model.save(SAVE_PATH)
    print("✅ Modelo guardado exitosamente.")
