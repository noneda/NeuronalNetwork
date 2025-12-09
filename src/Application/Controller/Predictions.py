from Domain.Repository.Prediction import InterfasePrediction
from Core.Api.Request import Request
from Core.Api.Response import Response
from Application.Serializer.Prediction import PredictionSerializer
from Application.Util.Graphics import generate_predictions_chart
from Core.NeuronalNetwork import retrain_model
from Core.Logger import Logger


interfase = InterfasePrediction()


def create_prediction(req: Request, res: Response):
    user_id = req.body["user"]
    prompt = req.body["prompt"]

    try:
        prediction = interfase.create_for_user(user_id, prompt)
        send = PredictionSerializer.from_model(prediction)
        res.json({"data": send}, 201)
    except Exception as e:
        res.json({"message": "Error with Server", "error": str(e)}, 500)


def get_by_user(req: Request, res: Response):
    user = req.params["user"]

    if not user:
        return res.json({"message": "User parameter required"}, 400)

    try:
        predictions = interfase.get_by_user(user)
        if len(predictions) == 0:
            res.json({"message": "User don`t have Predictions"}, 400)
        else:
            send = PredictionSerializer.from_model(predictions, many=True)
            res.json({"data": send}, 200)
    except Exception as e:
        res.json({"message": "Error with Server", "error": str(e)}, 500)


def export_user_predictions_chart(req: Request, res: Response):
    """Genera un gráfico básico (horas vs nota) para las predicciones de un usuario
    y guarda la imagen en `/uploads` en formato .webp. Devuelve la ruta relativa.
    """
    user = req.params.get("user") if hasattr(req, "params") else None
    if not user:
        # allow body fallback
        user = req.body.get("user") if hasattr(req, "body") else None

    if not user:
        return res.json({"message": "User parameter required"}, 400)

    try:
        predictions = interfase.get_by_user(int(user))

        preds_list = list(predictions) if predictions is not None else []
        if len(preds_list) == 0:
            return res.json({"message": "User don`t have Predictions"}, 400)

        try:
            generated_path = generate_predictions_chart(preds_list, int(user))
            rel_path = os.path.relpath(generated_path, os.getcwd())
            return res.json({"data": {"path": rel_path}}, 200)
        except Exception as e:
            return res.json({"message": "Error generating chart", "error": str(e)}, 500)
    except Exception as e:
        return res.json({"message": "Error generating chart", "error": str(e)}, 500)


def retrain_model_endpoint(req: Request, res: Response):
    """Endpoint para reentrenar el modelo desde el Core.
    Body JSON opcional:
      - additional_epochs: int (por defecto 500)
      - verbose_level: int (por defecto 2)
    Este endpoint llama a `Core.NeuronalNetwork.retrain_model` y espera a que termine.
    """
    try:
        body = req.body if hasattr(req, "body") else {}
        additional_epochs = int(body.get("additional_epochs", 500))
        verbose_level = int(body.get("verbose_level", 2))

        Logger.log(
            f"Iniciando reentrenamiento: epochs={additional_epochs}, verbose={verbose_level}"
        )

        history = retrain_model(
            additional_epochs=additional_epochs, verbose_level=verbose_level
        )

        # intentar extraer resumen simple del History si está disponible
        history_summary = None
        try:
            if hasattr(history, "history") and isinstance(history.history, dict):
                history_summary = {
                    k: v[-1] if isinstance(v, (list, tuple)) and len(v) > 0 else v
                    for k, v in history.history.items()
                }
        except Exception:
            history_summary = None

        Logger.log("Reentrenamiento finalizado.")
        return res.json(
            {
                "message": "Retrain completed",
                "epochs": additional_epochs,
                "history_summary": history_summary,
            },
            200,
        )
    except Exception as e:
        Logger.log(f"Error en retrain_model_endpoint: {e}")
        return res.json({"message": "Error during retrain", "error": str(e)}, 500)
    except Exception as e:
        return res.json({"message": "Error generating chart", "error": str(e)}, 500)
