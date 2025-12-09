import importlib


def test_retrain_model_endpoint_success(monkeypatch):
    """Test que retrain_model_endpoint llama a Core.NeuronalNetwork.retrain_model y devuelve 200."""
    # mock retrain_model para evitar entrenamiento real
    import Core.NeuronalNetwork as nn_mod

    call_history = {"called": False, "args": {}}

    def fake_retrain(additional_epochs=500, verbose_level=2):
        call_history["called"] = True
        call_history["args"] = {"epochs": additional_epochs, "verbose": verbose_level}

        # return a mock history object
        class MockHistory:
            history = {"loss": [5.0, 4.5, 4.0, 3.5]}

        return MockHistory()

    monkeypatch.setattr(nn_mod, "retrain_model", fake_retrain)

    # reload controller to use patched retrain_model
    import Application.Controller.Predictions as controller

    importlib.reload(controller)

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

    req = Req({"additional_epochs": 100, "verbose_level": 1})
    res = Res()

    controller.retrain_model_endpoint(req, res)

    assert res.status == 200
    assert res.data["message"] == "Retrain completed"
    assert res.data["epochs"] == 100
    assert call_history["called"] is True
    assert call_history["args"]["epochs"] == 100


def test_retrain_model_endpoint_default_values(monkeypatch):
    """Test que retrain_model_endpoint usa valores por defecto si no se proporcionan en el body."""
    import Core.NeuronalNetwork as nn_mod

    call_history = {"called": False, "args": {}}

    def fake_retrain(additional_epochs=500, verbose_level=2):
        call_history["called"] = True
        call_history["args"] = {"epochs": additional_epochs, "verbose": verbose_level}

        class MockHistory:
            history = {}

        return MockHistory()

    monkeypatch.setattr(nn_mod, "retrain_model", fake_retrain)

    import Application.Controller.Predictions as controller

    importlib.reload(controller)

    class Req:
        def __init__(self):
            self.body = {}

    class Res:
        def __init__(self):
            self.data = None
            self.status = None

        def json(self, data, status=200):
            self.data = data
            self.status = status

    req = Req()
    res = Res()

    controller.retrain_model_endpoint(req, res)

    assert res.status == 200
    assert call_history["args"]["epochs"] == 500
    assert call_history["args"]["verbose"] == 2


def test_retrain_model_endpoint_error(monkeypatch):
    """Test que retrain_model_endpoint devuelve 500 si retrain_model lanza una excepción."""
    import Core.NeuronalNetwork as nn_mod

    def fake_retrain(additional_epochs=500, verbose_level=2):
        raise RuntimeError("Model not loaded")

    monkeypatch.setattr(nn_mod, "retrain_model", fake_retrain)

    import Application.Controller.Predictions as controller

    importlib.reload(controller)

    class Req:
        def __init__(self):
            self.body = {}

    class Res:
        def __init__(self):
            self.data = None
            self.status = None

        def json(self, data, status=200):
            self.data = data
            self.status = status

    req = Req()
    res = Res()

    controller.retrain_model_endpoint(req, res)

    assert res.status == 500
    assert "Error during retrain" in res.data.get("message", "")
