from Core.Api.Router import Router
from Core.Api.Middleware.require_json import require_json
from Core.Api.Middleware.validate_fields import validate_fields

from Application.Controller.Users import (
    post_login,
    post_register,
    get_me,
    # get_by_id,
    # update_user,
    # delete_delete,
)


def register_user_routes(router: Router):
    router.route("/login", methods=["POST"])(
        require_json(validate_fields("name", "password")(post_login))
    )
    router.route("/register", methods=["POST"])(
        require_json(validate_fields("name", "password")(post_register))
    )
    router.route("user/me/:name", methods=["GET"])(get_me)
