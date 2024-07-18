from fastapi import FastAPI, HTTPException

from service.hedge_service import HedgeService
from api.models import CreateAccountLinkRequest

app = FastAPI()
hedge_service = HedgeService()


@app.get("/v1/ping")
def ping():
    return {"message": "Ping successful!"}


@app.post("/v1/bettors/link")
def create_account_link(request: CreateAccountLinkRequest = None):
    if request is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must contain first, last, phone, book, state_abbr",
        )
    try:
        cid, url, exc_message = hedge_service.create_account_link(request)
        if exc_message:
            raise HTTPException(status_code=400, detail=exc_message)
        return {"cid": cid, "url": url}
    except Exception as e:
        raise
