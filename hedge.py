from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from service.hedge_service import HedgeService
from api.models import CreateAccountLinkRequest
from repository.mongo_repository import MongoRepository
from utils.log import get_logger

LOGGER = get_logger(__name__)

security = HTTPBasic()
app = FastAPI()
hedge_service = HedgeService()
mongo_repository = MongoRepository()

allowed_origins = [
    "http://localhost:3000"
    "https://hedge-ui.vercel.app"
    "https://savewithhedge.co"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# TODO improve this authentication method
def authenticate(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    pwd = creds.password
    LOGGER.info(f"Hedge Controller: Authenticating user {username}")
    if mongo_repository.is_admin(username, pwd):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Failed to authenticate {username}",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/v1/ping")
def ping():
    LOGGER.info("Hedge Controller: Received Ping request")
    return {"message": "Ping successful!"}


@app.get("/v1/test-auth")
def test_auth(is_authenticated=Depends(authenticate)):
    if is_authenticated:
        return {"message": "Successfully authenticated!"}


@app.get("/v1/bettors")
def get_bettors(is_authenticated=Depends(authenticate)):
    LOGGER.info("Hedge Controller: Request to get_bettors")
    if is_authenticated:
        bettors = hedge_service.get_bettors()
        return {"message": bettors}


@app.post("/v1/bettors/link")
def create_account_link(
    is_authenticated=Depends(authenticate), request: CreateAccountLinkRequest = None
):
    LOGGER.info(f"Hedge Controller: Request to create_account_link ${request}")
    if is_authenticated:
        if request is None:
            raise HTTPException(
                status_code=400,
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
    LOGGER.info(f"Hedge Controller: Request to get_books")
    if is_authenticated:
        books = hedge_service.get_books()
        return {"books": books}


@app.get("/v1/books/{book_name}/regions")
def get_regions_for_book(book_name: str, is_authenticated=Depends(authenticate)):
    LOGGER.info(f"Hedge Controller: Request to get_regions_for_book {book_name}")
    if is_authenticated:
        regions = hedge_service.get_regions_for_book(book_name)
        return {"regions": regions}
