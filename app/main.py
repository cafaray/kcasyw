from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute

from dependencies import get_query_token, get_token_header
from routers import draws, groups, participants, gifts, events

# dependencies=[Depends(get_query_token)]
app = FastAPI()

app.include_router(draws.router, prefix="/draws", tags=["Draws"], responses={404: {"RESOURCE_NOT_FOUND": "Not found"}}) # , dependencies=[Depends(get_token_header)],)
app.include_router(groups.router, prefix="/groups", tags=["Groups"], responses={404: {"RESOURCE_NOT_FOUND": "Not found"}})
app.include_router(participants.router, prefix="/participants", tags=["Participants"], responses={404: {"RESOURCE_NOT_FOUND": "Not found"}})
app.include_router(gifts.router, prefix="/gifts", tags=["Gifts"], responses={404: {"RESOURCE_NOT_FOUND": "Not found"}})
app.include_router(events.router, prefix="/events", tags=["Events"], responses={404: {"RESOURCE_NOT_FOUND": "Not found"}})

@app.get("/")
async def root():
    return {"message": "Wellcome to kcasyw!"}

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)