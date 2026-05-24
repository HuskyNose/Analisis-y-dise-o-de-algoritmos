from fastapi import APIRouter
from controllers import graph_controller

router = APIRouter()

router.add_api_route(
    path="/",
    endpoint=graph_controller.get_graph,
    methods=["GET"]
)

router.add_api_route(
    path="/import",
    endpoint=graph_controller.import_graph,
    methods=["POST"]
)