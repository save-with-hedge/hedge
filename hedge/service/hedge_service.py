import datetime
import json
from typing import Dict

from hedge.models.api.api_models import CreateAccountLinkRequest
from hedge.models.hedge_betslip import HedgeBetslip
from hedge.repository.drive_repository import DriveRepository
from hedge.repository.mongo_repository import MongoRepository
from hedge.scripts.calculate_stats import calculate_stats
from hedge.scripts.fetch_betslips import fetch_betslips
from hedge.scripts.format_betslips import format_betslips
from hedge.service.sharp_sports_service import SharpSportsService
from hedge.utils.betslip_utils import filter_betslips_by_timestamp, get_wtd_delta
from hedge.utils.constants import (
    BOOK_REGIONS_HEDGE_FILENAME,
    MONGO_BETSLIPS_COLLECTION, MONGO_STATS_COLLECTION,
)
from hedge.utils.user_utils import get_internal_id
from hedge.utils.path_anchor import BOOK_INFO_FOLDER, STATS_FOLDER
from hedge.utils.json_utils import read_json, write_json
from hedge.utils.log import get_logger

LOGGER = get_logger("HedgeService")


class HedgeService:
    def __init__(self):
        self.sharp_sports_service = SharpSportsService()
        self.mongo_repository = MongoRepository()
        self.drive_repository = DriveRepository()

    def create_account_link(self, request: CreateAccountLinkRequest):
        """
        :return: A tuple containing a user-specific contextId, account linking url, and an exception message
        """
        # Create user and save to db
        try:
            internal_id = self.create_bettor(request.first, request.last, request.phone)
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

    def create_bettor(self, first, last, phone):
        internal_id = get_internal_id(first, last)
        user = self.mongo_repository.get_bettor(internal_id)
        if user is None:
            self.mongo_repository.create_bettor(internal_id, first, last, phone)
        return internal_id

    @staticmethod
    def format_link_url(cid, book_region_id, sdk_required):
        url = "https://ui.sharpsports.io/link/" + cid
        if sdk_required:
            url += "/region/" + book_region_id + "/login"
        return url

    def get_bettors(self):
        return self.sharp_sports_service.get_bettors()

    @staticmethod
    def get_books():
        try:
            path = BOOK_INFO_FOLDER + "/book_regions_hedge.json"
            books = read_json(path)
            book_names = [key for key in books.keys()]
            return book_names
        except Exception as e:
            LOGGER.error(f"{e}")
            return e

    @staticmethod
    def get_regions_for_book(book_name):
        try:
            path = BOOK_INFO_FOLDER + "/book_regions_hedge.json"
            books = read_json(path)
            book = books.get(book_name)
            regions = [key for key in book.get("bookRegionAbbrId").keys()]
            return regions
        except Exception as e:
            LOGGER.error(f"{e}")
            return e

    def refresh_all_betslips(self) -> None:
        """
        Refresh betslips and stats YTD for all bettors in the system
        """
        time_now = datetime.datetime.now().strftime("%H:%M:%S %m/%d/%Y")
        bettors = self.sharp_sports_service.get_bettors()
        internal_ids = [bettor.get("internalId") for bettor in bettors]
        for internal_id in internal_ids:
            raw_betslips = fetch_betslips(internal_id)
            hedge_betslips = format_betslips(raw_betslips=raw_betslips)
            if len(hedge_betslips) == 0:
                LOGGER.info(f"No betslips found for {internal_id} YTD")
            betslips_mongo_doc = {
                "internal_id": internal_id,
                "refresh_time": time_now,
                "betslips_ytd": [betslip.to_dict() for betslip in hedge_betslips],
            }
            self.mongo_repository.upsert_document(
                MONGO_BETSLIPS_COLLECTION, internal_id, betslips_mongo_doc
            )
            if len(hedge_betslips) > 0:
                self.drive_repository.upload_betslips(filename=f"{internal_id}.csv", betslips=hedge_betslips)

    def refresh_all_stats(self) -> None:
        """
        Refresh stats YTD, WTD, 7-day for all bettors in the system
        """
        time_now = datetime.datetime.now().strftime("%H:%M:%S %m/%d/%Y")
        bettors = self.sharp_sports_service.get_bettors()
        stats_all = {}
        internal_ids = [bettor.get("internalId") for bettor in bettors]
        for internal_id in internal_ids:
            betslips_doc = self.get_betslips_for_bettor(internal_id=internal_id)
            if betslips_doc is None:
                LOGGER.info(f"No betslips found for {internal_id}")
                continue
            betslips_ytd = betslips_doc.get("betslips_ytd")
            if betslips_ytd is None or len(betslips_ytd) == 0:
                LOGGER.info(f"No betslips_ytd found for {internal_id}")
                continue
            hedge_betslips_ytd = [HedgeBetslip(data) for data in betslips_ytd]
            hedge_betslips_wtd = filter_betslips_by_timestamp(betslips=hedge_betslips_ytd, delta=get_wtd_delta())
            hedge_betslips_7_days = filter_betslips_by_timestamp(betslips=hedge_betslips_ytd,
                                                                 delta=datetime.timedelta(days=7))
            stats_ytd = calculate_stats(hedge_betslips_ytd)
            stats_wtd = calculate_stats(hedge_betslips_wtd)
            stats_7_days = calculate_stats(hedge_betslips_7_days)
            stats_mongo_doc = {
                "internal_id": internal_id,
                "refresh_time": time_now,
                "stats_ytd": stats_ytd,
                "stats_wtd": stats_wtd,
                "stats_7_days": stats_7_days,
            }
            self.mongo_repository.upsert_document(MONGO_STATS_COLLECTION, internal_id, stats_mongo_doc)
            stats_all[internal_id] = {
                "ytd": stats_ytd,
                "wtd": stats_wtd,
                "7_days": stats_7_days,
            }
        filepath = str(STATS_FOLDER / "all_stats.json")
        write_json(filepath=filepath, json_data=stats_all)
        self.drive_repository.upload(filepath=filepath)

    def get_betslips_for_bettor(self, internal_id: str) -> Dict[str, any] | None:
        """
        :return: A list of betslips info for a user, or None if the document does not exist
        """
        return self.mongo_repository.find_document(MONGO_BETSLIPS_COLLECTION, {"internal_id": internal_id})

    def get_stats_for_bettor(self, internal_id):
        """
        :return: A dictionary of stats info for a user, or None if the document does not exist
        """
        return self.mongo_repository.find_document(MONGO_STATS_COLLECTION, {"internal_id": internal_id})

    def get_stats_all(self):
        all_stats = []
        bettors = self.get_bettors()
        for bettor in bettors:
            stats = self.get_stats_for_bettor(bettor.get("internalId"))
            if stats:
                all_stats.append(stats)
        return all_stats


if __name__ == "__main__":
    # For testing only
    service = HedgeService()
    service.refresh_all_stats()
