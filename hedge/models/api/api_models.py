from pydantic import BaseModel


class CreateAccountLinkRequest(BaseModel):
    first: str
    last: str
    phone: str
    book: str
    state_abbr: str

    def format_inputs(self):
        self.state_abbr = self.state_abbr.upper()
        self.book = self.book[0].upper() + self.book[1:]
