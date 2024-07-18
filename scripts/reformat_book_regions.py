"""
Format book regions so the bookRegionId is more easily accessible by book and state, as such
{
    "Fanduel": {
        "bookRegionId": {
            "New York": "...",
            "California": "...",
        }
        "bookRegionAbbrId": {
            "NY": "...",
            "CA": "...",
        }
        "sdkRequired": true
    }
}
"""

from utils.constants import BOOK_REGIONS_HEDGE_FILENAME
from utils.json_utils import read_json, write_json
from utils.path_anchor import BOOK_INFO_FOLDER


def reformat_book_regions():
    # Read sharp book regions in
    sharp_path = BOOK_INFO_FOLDER + "/book_regions.json"
    sharp_book_regions = read_json(sharp_path)

    # Reformat
    hedge_book_regions = {}
    for book_region in sharp_book_regions:
        book_region_id = book_region.get("id")
        book_name = book_region.get("book").get("name")
        state = book_region.get("name")
        state_abbr = book_region.get("abbr").upper()
        sdk_required = book_region.get("sdkRequired")

        if book_name not in hedge_book_regions:
            hedge_book_regions[book_name] = {
                "bookRegionId": {},
                "bookRegionAbbrId": {},
                "sdkRequired": sdk_required,
            }
        book = hedge_book_regions[book_name]
        book["bookRegionId"][state] = book_region_id
        book["bookRegionAbbrId"][state_abbr] = book_region_id

    # Write to json
    hedge_path = BOOK_INFO_FOLDER + "/" + BOOK_REGIONS_HEDGE_FILENAME + ".json"
    write_json(hedge_path, hedge_book_regions)


if __name__ == "__main__":
    reformat_book_regions()
