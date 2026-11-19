from pathlib import Path

# Main project directory
PROJECT_ROOT = Path(r"D:\DS Project\credit-portfolio-risk-modeling")

# Raw data locations
DATA_2006_2010 = PROJECT_ROOT / "dataset"
DATA_2011_2012 = Path(
    r"E:\DS_project_backup\credit-risk-portfolio\data"
)

# Get raw quarterly file
def get_vintage_file(file_type, year, quarter):

    if file_type not in ["orig", "perf"]:
        raise ValueError("file_type must be 'orig' or 'perf'")

    if not 1 <= quarter <= 4:
        raise ValueError("quarter must be between 1 and 4")

    filename = f"{file_type}_{year}Q{quarter}.txt"

    if 2006 <= year <= 2010:
        path = DATA_2006_2010 / filename

    elif 2011 <= year <= 2012:
        path = DATA_2011_2012 / filename

    else:
        raise ValueError(f"Unsupported vintage year: {year}")

    if not path.exists():
        raise FileNotFoundError(path)

    return path


# Processed data locations (E drive)
PROCESSED_DIR = Path(
    r"E:\DS_project_backup\credit-risk-portfolio\processed"
)

ORIG_PARQUET_DIR = PROCESSED_DIR / "origination"
PERF_PARQUET_DIR = PROCESSED_DIR / "performance"
AUDIT_DIR = PROCESSED_DIR / "audit"

DUCKDB_TEMP_DIR = Path(
    r"E:\DS_project_backup\credit-risk-portfolio\duckdb_temp"
)

# Create directories if they do not exist
for folder in [
    PROCESSED_DIR,
    ORIG_PARQUET_DIR,
    PERF_PARQUET_DIR,
    AUDIT_DIR,
    DUCKDB_TEMP_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)