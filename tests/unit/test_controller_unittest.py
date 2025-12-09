import unittest
import importlib


class DummyReq:
    def __init__(self, body=None, params=None):
        self.body = body or {}
        self.params = params or {}


class DummyRes:
    def __init__(self):
        self.data = None
        self.status = None

    def json(self, data, status=200):
        self.data = data
        self.status = status


class ControllerTests(unittest.TestCase):
    def setUp(self):
        # patch predict_note to deterministic value by setting on repo module
        import Domain.Repository.Prediction as repo_pred

        repo_pred.predict_note = lambda hours: {"predicted_note": 55.5}
        import Application.Controller.Predictions as controller

        importlib.reload(controller)
        self.controller = controller

    def test_create_prediction_returns_201(self):
        from Domain.Service.User import UserService

        us = UserService()
        user = us.create_user("unittest_user", "pw")

        req = DummyReq(body={"user": user.id, "prompt": 1.0})
        res = DummyRes()
        self.controller.create_prediction(req, res)
        self.assertEqual(res.status, 201)


if __name__ == "__main__":
    unittest.main()
