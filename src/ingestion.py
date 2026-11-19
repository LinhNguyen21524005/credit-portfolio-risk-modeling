from pathlib import Path
import duckdb
import pandas as pd


def get_column_names(mapping):
    """
    Return standardized column names ordered by
    original Freddie Mac field position.
    """

    ordered = (
        mapping
        .sort_values("Field Position")
        ["standard_name"]
        .tolist()
    )

    if len(ordered) != len(set(ordered)):
        raise ValueError(
            "Duplicate standardized column names detected."
        )

    return ordered


def ingest_txt_to_parquet(
    file_path,
    output_path,
    mapping,
    temp_directory
):
    """
    Stream one pipe-delimited TXT file into Parquet.

    All input fields are initially stored as VARCHAR.
    """

    file_path = Path(file_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    column_names = get_column_names(mapping)

    columns = {
        name: "VARCHAR"
        for name in column_names
    }

    con = duckdb.connect()

    try:
        con.execute(
            f"SET temp_directory = '{Path(temp_directory).as_posix()}'"
        )

        relation = con.read_csv(
            str(file_path),
            delim="|",
            header=False,
            columns=columns,
            nullstr="__NULL_SENTINEL__",
            ignore_errors=False
        )

        # Validate schema
        actual_columns = relation.columns

        if actual_columns != column_names:
            raise ValueError(
                f"Schema mismatch in {file_path.name}"
            )

        # Stream result to Parquet
        relation.write_parquet(
            str(output_path),
            compression="zstd"
        )

        # Validate output row count
        result = con.execute(
            "SELECT COUNT(*) FROM read_parquet(?)",
            [str(output_path)]
        ).fetchone()

        row_count = result[0]

        return {
            "source_file": file_path.name,
            "output_file": str(output_path),
            "row_count": row_count,
            "column_count": len(column_names),
            "output_size_mb": round(
                output_path.stat().st_size / 1024**2,
                2
            )
        }

    finally:
        con.close()