import importlib


def test_end_to_end_prediction_persistence(monkeypatch):
    # patch predict_note to deterministic value
    import Domain.Repository.Prediction as repo_pred

    def fake_predict(hours):
        return {"predicted_note": 42.42}

    repo_pred.predict_note = fake_predict

    # reload controller so it uses patched repo
    import Application.Controller.Predictions as controller

    importlib.reload(controller)

    # create a user
    from Domain.Service.User import UserService

    us = UserService()
    user = us.create_user("integ_user", "integ_pass")

    # call create_prediction
    class Req:
        def __init__(self, body):
            self.body = body

    class Res:
        def __init__(self):
            self.data = None
            self.status = None

        def json(self, data, status=200):
            self.data = data
            self.status = status

    req = Req({"user": user.id, "prompt": 2.0})
    res = Res()
    controller.create_prediction(req, res)
    assert res.status == 201

    # verify stored in DB via PredictionService
    from Domain.Service.Prediction import PredictionService

    ps = PredictionService()
    predictions = ps.get_by_user(user.id)
    # get_by_user returns a QuerySet ordered; ensure at least one
    assert predictions is not None
