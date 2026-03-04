from fastapi import APIRouter

from src.controllers.healthy_controller import get_health, get_liveness, get_root

router = APIRouter()

router.add_api_route("/", get_root, methods=["GET"])
router.add_api_route("/healthy", get_health, methods=["GET"])
router.add_api_route("/liveness", get_liveness, methods=["GET"])
