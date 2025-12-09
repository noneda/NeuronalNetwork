import importlib


def test_create_prediction_success(monkeypatch, tmp_path):
    # patch the neural network prediction to avoid TF dependency
    import Domain.Repository.Prediction as repo_pred

    def fake_predict(hours):
        return {"predicted_note": 88.5}

    repo_pred.predict_note = fake_predict

    # ensure controller reloads and uses patched repo
    import Application.Controller.Predictions as controller

    importlib.reload(controller)

    # dummy request and response
    class DummyReq:
        def __init__(self, body):
            self.body = body

    class DummyRes:
        def __init__(self):
            self.data = None
            self.status = None

        def json(self, data, status=200):
            self.data = data
            self.status = status

    # create a user first via UserService
    from Domain.Service.User import UserService

    us = UserService()
    user = us.create_user("tester", "pass123")

    req = DummyReq({"user": user.id, "prompt": 5.0})
    res = DummyRes()

    controller.create_prediction(req, res)

    assert res.status == 201
    # controller now returns the created resource under the `data` key
    assert "data" in res.data
    assert all(k in res.data["data"] for k in ("id", "prompt", "response", "user"))


def test_get_by_user_empty_and_with_predictions(monkeypatch):
    # patch prediction function
    import Domain.Repository.Prediction as repo_pred

    def fake_predict(hours):
        return {"predicted_note": 77.0}

    repo_pred.predict_note = fake_predict

    importlib.invalidate_caches()
    import Application.Controller.Predictions as controller

    importlib.reload(controller)

    class DummyReq:
        def __init__(self, params=None, body=None):
            self.params = params or {}
            self.body = body or {}

    class DummyRes:
        def __init__(self):
            self.data = None
            self.status = None

        def json(self, data, status=200):
            self.data = data
            self.status = status

    # create user
    from Domain.Service.User import UserService

    us = UserService()
    user = us.create_user("tester2", "pass123")

    # call get_by_user when no predictions
    req = DummyReq(params={"user": user.id})
    res = DummyRes()
    controller.get_by_user(req, res)
    # When no predictions, controller returns 400 with message
    assert res.status in (400,)

    # create a prediction via controller
    req_create = DummyReq(body={"user": user.id, "prompt": 3.0})
    res_create = DummyRes()
    controller.create_prediction(req_create, res_create)
    assert res_create.status == 201

    # now get_by_user should return data
    req2 = DummyReq(params={"user": user.id})
    res2 = DummyRes()
    controller.get_by_user(req2, res2)
    assert res2.status == 200
    assert "data" in res2.data
