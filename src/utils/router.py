from fastapi import APIRouter


def include_routers(root_router: APIRouter, routers: list | tuple) -> APIRouter:
    for router in routers:
        root_router.include_router(router)
    return root_router
