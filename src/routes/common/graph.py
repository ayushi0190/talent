# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Graph routes
@author <ankits@simplifyvms.com>
"""
from fastapi import Request, APIRouter
from fastapi import Depends
from fastapi.security.api_key import APIKey

from starlette.responses import JSONResponse
from src.services.common.apis.graph_services import GraphServices
from src.utilities.verify import get_api_key
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

graph_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@graph_router.get('/data/graph.json')
async def get_graph_by_id(request: Request,  id : str, source: str) -> JSONResponse:
    """
    Get Graph by Resume Id with any services like sovren or simpai or opening
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    graph_obj = GraphServices()
    return JSONResponse(graph_obj.call_get_graph(request, id, source))


@graph_router.get('/graph',response_class=HTMLResponse)
async def get_graph(request: Request, id:str, source: str):

    """
    Get Graph by Resume Id with any services like sovren or simpai or opening
    :param request:
    :param data:
    :param id:
    :return:
    """
    return templates.TemplateResponse("indexnew.html", {"request": request, "id": id, "source" : source})


