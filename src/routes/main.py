# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Main setup file which includes routes
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
@author <ankits@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.common.comp_cand import comp_cand_router
from src.routes.common.matchers import matcher_router
from src.routes.common.parsers import parser_router
from src.routes.common.scorers import scorer_router
from src.routes.common.searchers import searcher_router
from src.routes.common.submission import submission_router
from src.utilities.custom_logging import CustomizeLogger
from src.routes.admin.configs import config_router
from src.tests.score_test import score_test_router
from src.config.config import settings
from src.routes.common.graph import graph_router
from fastapi.staticfiles import StaticFiles
from src.routes.common.stats import stats_router
from src.routes.admin.profile_settings import profile_router

config_path = Path(__file__).with_name("logging_config.json")

app = FastAPI(title="Talent Matcher",
              debug=settings[settings.env].logging.loggers_default_level)
logger = CustomizeLogger.make_logger()
app.logger = logger

app.mount("/static", StaticFiles(directory="static"), name="static")

# add cors link
origins = settings.default.allowed_hosts

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    config_router,
    tags=["Admin"],
)

app.include_router(
    profile_router,
    tags=["Profile"],
)

app.include_router(
    matcher_router,
    tags=["Matchers"],
)

app.include_router(
    searcher_router,
    tags=["Searchers"],
)

app.include_router(
    parser_router,
    tags=["Parsers"],
)

app.include_router(
    scorer_router,
    tags=["Scorer"],
)

app.include_router(
    comp_cand_router,
    tags=["Comparer"],
)

app.include_router(
    submission_router,
    tags=["Submission"],
)


app.include_router(
    score_test_router,
    tags=["ScoreTest"],
)


app.include_router(
    graph_router,
    tags=["Graph"],
)

app.include_router(
    stats_router,
    tags=["Stats"]
)

url_list = app.routes
def main():
    """ main function """
    uvicorn.run(
        "src.routes.main:app",
        host="0.0.0.0",
        port=settings.default.port,
        reload=True,
        log_level="info")




if __name__ == "__main__":
    #main()
    pass
