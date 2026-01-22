from fastapi import APIRouter, Depends

from .auth import verify_auth_token
from .routers import building_router, organization_router

main_router = APIRouter(prefix="/api", dependencies=[Depends(verify_auth_token)])
main_router.include_router(organization_router)
main_router.include_router(building_router)
