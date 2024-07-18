from pydantic import BaseModel


class CreateAccountLinkRequest(BaseModel):
    first: str
    last: str
    phone: str
    book: str
    state_abbr: str
