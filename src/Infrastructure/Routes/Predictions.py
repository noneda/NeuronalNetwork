from Core.Api.Router import Router
from Core.Api.Middleware.require_json import require_json
from Core.Api.Middleware.validate_fields import validate_fields

from Application.Controller.Predictions import (
    create_prediction,
    get_by_user,
    # get_by_id,
    # update_prediction,
    # delete_prediction,
)


def register_prediction_routes(router: Router):
    router.route("/predictions", methods=["POST"])(
        require_json(validate_fields("user", "prompt")(create_prediction))
    )
    router.route("/predictions/:user", methods=["GET"])(get_by_user)

    # router.get("/predictions/:id")(get_by_id)
    # router.put("/predictions/:id")(update_prediction)
    # router.delete("/predictions/:id")(delete_prediction)
