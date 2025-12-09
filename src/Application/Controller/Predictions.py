from Domain.Repository.Prediction import InterfasePrediction
from Core.Api.Request import Request
from Core.Api.Response import Response

interfase = InterfasePrediction()


def create_prediction(req: Request, res: Response):
    user_id = req.body["user"]
    prompt = req.body["prompt"]

    try:
        prediction = interfase.create_prediction(user_id, prompt)
        res.json({"prediction": prediction}, 201)
    except Exception as e:
        res.json({"message": "Error with Server", "error": str(e)}, 500)


# GET /search?user=(int)
def get_by_user(req: Request, res: Response):
    user = req.query.get("user")

    if not user:
        return res.json({"message": "User parameter required"}, 400)

    try:
        predictions = interfase.get_by_user(user)
        predictions_data = [
            {"id": p.id, "prompt": p.prompt, "response": p.response, "user": p.user}
            for p in predictions
        ]
        res.json({"data": predictions_data}, 200)
    except Exception as e:
        res.json({"message": "Error with Server", "error": str(e)}, 500)
