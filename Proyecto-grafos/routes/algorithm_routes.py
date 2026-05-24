from fastapi import APIRouter, Depends
from controllers import algorithm_controller
from middleware.validate_request import require_fields

router = APIRouter()

router.add_api_route(
    path="/run",
    endpoint=algorithm_controller.run_algorithm,
    methods=["POST"],
    dependencies=[Depends(require_fields(["algorithm"]))]
)