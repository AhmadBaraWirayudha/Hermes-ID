"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-07-07
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
        sa.Column("url", sa.Text),
        sa.Column("source_type", sa.Text, nullable=False, server_default="html_table"),
        sa.Column("table_index", sa.Integer, server_default="0"),
        sa.Column("notes", sa.Text),
        sa.Column("active", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.Text, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "market_observations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date", sa.Text, nullable=False),
        sa.Column("source", sa.Text, nullable=False),
        sa.Column("category", sa.Text, nullable=False),
        sa.Column("item", sa.Text, nullable=False),
        sa.Column("region", sa.Text, server_default="Indonesia"),
        sa.Column("price", sa.Float),
        sa.Column("volume", sa.Float),
        sa.Column("metric", sa.Text, server_default="price"),
        sa.Column("currency", sa.Text, server_default="IDR"),
        sa.Column("raw_payload", sa.Text),
        sa.Column("created_at", sa.Text, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("date", "source", "category", "item", "region", "metric", name="uq_market_obs"),
    )
    op.create_table(
        "scrape_runs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("source_name", sa.Text, nullable=False),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column("rows_collected", sa.Integer, server_default="0"),
        sa.Column("raw_csv_path", sa.Text),
        sa.Column("processed_csv_path", sa.Text),
        sa.Column("message", sa.Text),
        sa.Column("started_at", sa.Text, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("finished_at", sa.Text),
    )

def downgrade():
    op.drop_table("scrape_runs")
    op.drop_table("market_observations")
    op.drop_table("sources")
