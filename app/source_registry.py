"""Source registry helpers for configured scrape targets."""
import pandas as pd
from db import connect


def add_source(name, url, source_type="html_table", table_index=0, notes="", active=True):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO sources(name, url, source_type, table_index, notes, active)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                url=excluded.url,
                source_type=excluded.source_type,
                table_index=excluded.table_index,
                notes=excluded.notes,
                active=excluded.active
            """,
            (name, url, source_type, int(table_index or 0), notes, 1 if active else 0),
        )


def list_sources(active_only=False):
    where = "WHERE active = 1" if active_only else ""
    with connect() as conn:
        return pd.read_sql_query(f"SELECT * FROM sources {where} ORDER BY created_at DESC", conn)


def delete_source(source_id):
    with connect() as conn:
        conn.execute("DELETE FROM sources WHERE id = ?", (source_id,))


def get_source(source_id):
    with connect() as conn:
        rows = pd.read_sql_query("SELECT * FROM sources WHERE id = ?", conn, params=(source_id,))
    return None if rows.empty else rows.iloc[0].to_dict()
