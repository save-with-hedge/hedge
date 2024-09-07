"""
This is the API handler entry point
"""

import os
from contextlib import asynccontextmanager
from http import HTTPStatus

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from service.hedge_service import HedgeService
from models.api.api_models import CreateAccountLinkRequest
from repository.mongo_repository import MongoRepository
from utils.log import get_logger


LOGGER = get_logger("HedgeController")

security = HTTPBasic()
app = FastAPI()
hedge_service = HedgeService()
mongo_repository = MongoRepository()


# Daily refresh job
def refresh_betslips_daily():
    """
    Daily job for refreshing all bettor betslips and stats.
    """
    lock_file = "lock.txt"
    # Check if lock file exists (if it does, another worker is already performing the task)
    if os.path.exists(lock_file):
        return
    else:
        with open(lock_file, "w") as f:
            pass
    try:
        LOGGER.info("Starting daily betslip refresh job...")
        hedge_service.refresh_all_betslips()
        hedge_service.refresh_all_stats()
        LOGGER.info("Done!")
    except Exception as e:
        LOGGER.error(e)
    # Remove lock file to mark job as complete
    os.remove(lock_file)


# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(
    hour=5, minute=0, timezone=pytz.timezone("America/New_York")
)  # Run every day at 5am ET
scheduler.add_job(func=refresh_betslips_daily, trigger=trigger)
scheduler.start()


# Ensure the scheduler shuts down properly on application exit
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()


allowed_origins = [
    "http://localhost:3000",
    "https://savewithvercel.app",
    "https://www.savewithco",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO improve this authentication method
def authenticate(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    pwd = creds.password
    LOGGER.info(f"Authenticating user {username}")
    if mongo_repository.is_admin(username, pwd):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Failed to authenticate {username}",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/v1/ping")
def ping():
    LOGGER.info("Received Ping request")
    return {"message": "Ping successful!"}


@app.get("/v1/test-auth")
def test_auth(is_authenticated=Depends(authenticate)):
    if is_authenticated:
        return {"message": "Successfully authenticated!"}


@app.get("/v1/bettors")
def get_bettors(is_authenticated=Depends(authenticate)):
    LOGGER.info("Request to get_bettors")
    if is_authenticated:
        bettors = hedge_service.get_bettors()
        return {"bettors": bettors}


@app.post("/v1/bettors/betslips/refresh")
def refresh_all_betslips(is_authenticated=Depends(authenticate)):
    """
    Ad hoc betslip refresh endpoint, betslips normally refresh every 24 hours
    """
    LOGGER.info("Request to refresh_all_betslips")
    if is_authenticated:
        hedge_service.refresh_all_betslips()
        hedge_service.refresh_all_stats()
        return {"status": HTTPStatus.OK}


@app.get("/v1/bettors/{internal_id}/betslips")
def get_betslips_for_bettor(internal_id: str, is_authenticated=Depends(authenticate)):
    LOGGER.info(f"Request to get_betslips_for_bettor {internal_id}")
    if is_authenticated:
        betslips = hedge_service.get_betslips_for_bettor(internal_id)
        if betslips is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No betslips found for {internal_id}",
            )
        else:
            return {"betslips": betslips}


@app.get("/v1/bettors/{internal_id}/stats")
def get_stats_for_bettor(internal_id: str, is_authenticated=Depends(authenticate)):
    LOGGER.info(f"Request to get_stats_for_bettor {internal_id}")
    if is_authenticated:
        stats = hedge_service.get_stats_for_bettor(internal_id)
        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No stats found for {internal_id}",
            )
        else:
            return {"stats": stats}


@app.post("/v1/bettors/link")
def create_account_link(
    is_authenticated=Depends(authenticate), request: CreateAccountLinkRequest = None
):
    LOGGER.info(f"Request to create_account_link ${request}")
    if is_authenticated:
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request body must contain first, last, phone, book, state_abbr",
            )
        try:
            request.format_inputs()
            cid, url, exc_message = hedge_service.create_account_link(request)
            return {"cid": cid, "url": url, "exc_message": exc_message}
        except Exception:
            raise


@app.get("/v1/books")
def get_books(is_authenticated=Depends(authenticate)):
    LOGGER.info(f"Request to get_books")
    if is_authenticated:
        books = hedge_service.get_books()
        return {"books": books}


@app.get("/v1/books/{book_name}/regions")
def get_regions_for_book(book_name: str, is_authenticated=Depends(authenticate)):
    LOGGER.info(f"Request to get_regions_for_book {book_name}")
    if is_authenticated:
        regions = hedge_service.get_regions_for_book(book_name)
        return {"regions": regions}
