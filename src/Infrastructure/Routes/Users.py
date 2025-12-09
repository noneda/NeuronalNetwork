from Core.Api.Router import Router
from Core.Api.Middleware.require_json import require_json
from Core.Api.Middleware.validate_fields import validate_fields

from Application.Controller.Users import (
    post_login,
    post_register,
    # get_by_id,
    # update_user,
    # delete_delete,
)


def register_user_routes(router: Router):
    router.post("/login", methods=["POST"])(
        require_json(validate_fields("user", "prompt")(post_login))
    )
    router.get("/register", methods=["POST"])(
        require_json(validate_fields("user", "prompt")(post_register))
    )

    # router.get("/predictions/:id")(get_by_id)
    # router.put("/predictions/:id")(update_prediction)
    # router.delete("/predictions/:id")(delete_prediction)
