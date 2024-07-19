from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from service.hedge_service import HedgeService
from api.models import CreateAccountLinkRequest
from repository.mongo_repository import MongoRepository

security = HTTPBasic()
app = FastAPI()
hedge_service = HedgeService()
mongo_repository = MongoRepository()


# TODO improve this authentication method
def authenticate(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    pwd = creds.password
    return True
    # if mongo_repository.is_admin(username, pwd):
    #     return True
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed",
    #                     headers={"WWW-Authenticate": "Basic"})


@app.get("/v1/ping")
def ping():
    return {"message": "Ping successful!"}


@app.get("/v1/ping-mongo")
def ping_mongo():
    response = mongo_repository.ping()
    return {"mongo_response": response}


@app.get("/v1/test-auth")
def test_auth(is_authenticated=Depends(authenticate)):
    if is_authenticated:
        return {"message": "Successfully authenticated!"}


@app.post("/v1/bettors/link")
def create_account_link(is_authenticated=Depends(authenticate), request: CreateAccountLinkRequest = None):
    if is_authenticated:
        if request is None:
            raise HTTPException(
                status_code=400,
                detail="Request body must contain first, last, phone, book, state_abbr",
            )
        try:
            cid, url, exc_message = hedge_service.create_account_link(request)
            # if exc_message:
            #     raise HTTPException(status_code=400, detail=exc_message)
            return {"cid": cid, "url": url, "exc_message": exc_message}
        except Exception:
            raise
