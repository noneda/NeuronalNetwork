from Domain.Repository.Prediction import InterfasePrediction
from Core.Api.Request import Request
from Core.Api.Response import Response
from Application.Serializer.Prediction import PredictionSerializer


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
