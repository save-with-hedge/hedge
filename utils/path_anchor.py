from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FOLDER = str(PROJECT_ROOT / "out")
BETSLIPS_RAW_FOLDER = str(PROJECT_ROOT / "out" / "betslips_raw")
BETSLIPS_FORMATTED_FOLDER = PROJECT_ROOT / "out" / "betslips_formatted"
STATS_FOLDER = PROJECT_ROOT / "out" / "stats"
CUSTOMER_URLS_FILEPATH = str(PROJECT_ROOT / "customer_urls/customer_urls.csv")
BOOK_INFO_FOLDER = str(PROJECT_ROOT / "book_info")
