from api.models import CreateAccountLinkRequest
from repository.mongo_repository import MongoRepository
from service.sharp_sports_service import SharpSportsService
from utils.constants import BOOK_REGIONS_HEDGE_FILENAME
from utils.user_utils import get_internal_id
from utils.path_anchor import BOOK_INFO_FOLDER
from utils.json_utils import read_json
from utils.log import get_logger

LOGGER = get_logger()


class HedgeService:
    def __init__(self):
        self.sharp_sports_service = SharpSportsService()
        self.mongo_repository = MongoRepository()

    def create_account_link(self, request: CreateAccountLinkRequest):
        """
        :return: A tuple containing a user-specific contextId, account linking url, and an exception message
        """
        # Create user and save to db
        try:
            internal_id = self.create_user(request.first, request.last, request.phone)
        except Exception as e:
            LOGGER.error(e)
            return None, None, "Error creating or fetching user"

        # Get bookRegionId and SDK required
        book_regions_path = (
            BOOK_INFO_FOLDER + "/" + BOOK_REGIONS_HEDGE_FILENAME + ".json"
        )
        book_regions = read_json(book_regions_path)
        book_region_id = (
            book_regions.get(request.book)
            .get("bookRegionAbbrId")
            .get(request.state_abbr)
        )
        sdk_required = book_regions.get(request.book).get("sdkRequired")

        auth_token = None
        if sdk_required:
            auth_token = self.sharp_sports_service.create_extension_auth_token(
                internal_id
            )

        cid = self.sharp_sports_service.create_context(internal_id, auth_token)
        url = self.format_link_url(cid, book_region_id, sdk_required)
        return cid, url, ""

    def create_user(self, first, last, phone):
        internal_id = get_internal_id(first, last)
        user = self.mongo_repository.get_user(internal_id)
        if user is None:
            self.mongo_repository.create_user(internal_id, first, last, phone)
        return internal_id

    @staticmethod
    def format_link_url(cid, book_region_id, sdk_required):
        url = "https://ui.sharpsports.io/link/" + cid
        if sdk_required:
            url += "/region/" + book_region_id + "/login"
        return url

    def get_bettors(self):
        return self.sharp_sports_service.get_bettors()


if __name__ == "__main__":
    # For testing only
    service = HedgeService()
