from Infrastructure.Routes.Users import register_user_routes
from Infrastructure.Routes.Predictions import register_prediction_routes

from Core.Api.Router import Router
from Core.Api.Response import Response
from Core.Api.Request import Request

from Core.Api import RestAPIHandler

router = Router()


@router.route("/", methods=["GET"])
def get_users(req, res: Response):
    res.json(
        {
            "version": "0.0.1",
            "made by": "Sebaxsus && noneda",
            "message": "Hello Word!!",
        },
        200,
    )


register_prediction_routes(router)
register_user_routes(router)


def makeRouter(api: RestAPIHandler):
    api.router = router
