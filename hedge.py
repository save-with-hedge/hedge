from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from service.hedge_service import HedgeService
from models.api.api_models import CreateAccountLinkRequest, GetStatsForBettorRequest
from repository.mongo_repository import MongoRepository
from utils.log import get_logger

LOGGER = get_logger("HedgeController")

security = HTTPBasic()
app = FastAPI()
hedge_service = HedgeService()
mongo_repository = MongoRepository()

allowed_origins = [
    "http://localhost:3000",
    "https://savewithhedge.vercel.app",
    "https://www.savewithhedge.co",
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
        return {"message": bettors}


@app.get("/v1/bettors/{internal_id}/stats")
def get_stats_for_bettor(
    internal_id: str,
    request: GetStatsForBettorRequest = None,
    is_authenticated=Depends(authenticate),
):
    LOGGER.info(f"Request to get_stats_for_bettor {internal_id}")
    if is_authenticated:
        if request and request.refresh:
            LOGGER.info(f"Refresh stats requested")
            hedge_service.refresh_stats_for_bettor(internal_id)
        stats = hedge_service.get_stats_for_bettor(internal_id)
        if stats is None or len(stats) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No stats found for {internal_id}",
            )
        else:
            return {"stats": stats}


@app.get("/v1/bettors/stats/refresh")
def refresh_stats_all(is_authenticated=Depends(authenticate)):
    LOGGER.info("Request to refresh_stats_all")
    if is_authenticated:
        hedge_service.refresh_stats_all()


@app.get("/v1/bettors/stats")
def get_stats_all(is_authenticated=Depends(authenticate)):
    LOGGER.info(f"Request to get_stats_all")
    if is_authenticated:
        stats = hedge_service.get_stats_all()
        if stats is None or len(stats) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No stats found",
            )
        else:
            return {"stats": stats}


@app.get("/v1/bettors/{internal_id}/history")
def get_history_for_bettor(
    internal_id: str,
    request: GetStatsForBettorRequest = None,
    is_authenticated=Depends(authenticate),
):
    LOGGER.info(f"Request to get_history_for_bettor {internal_id}")
    if is_authenticated:
        if request and request.refresh:
            LOGGER.info(f"Refresh stats requested")
            hedge_service.refresh_stats_for_bettor(internal_id)
        history = hedge_service.get_history_for_bettor(internal_id)
        if history is None or len(history) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No history found for {internal_id}",
            )
        else:
            return {"history": history}


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
