from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FOLDER = str(PROJECT_ROOT / "out")
BETSLIPS_RAW_FOLDER = str(PROJECT_ROOT / "out" / "betslips_raw")
BETSLIPS_FORMATTED_FOLDER = str(PROJECT_ROOT / "out" / "betslips_formatted")
