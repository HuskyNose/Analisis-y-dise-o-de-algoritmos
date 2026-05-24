from fastapi import APIRouter
from controllers import history_controller

router = APIRouter()

router.add_api_route(
    path="/",
    endpoint=history_controller.list_history,
    methods=["GET"]
)

router.add_api_route(
    path="/",
    endpoint=history_controller.clear_history,
    methods=["DELETE"]
)