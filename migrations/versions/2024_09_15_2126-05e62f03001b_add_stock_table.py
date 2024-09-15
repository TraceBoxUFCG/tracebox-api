"""add_stock_table

Revision ID: 05e62f03001b
Revises: 2fae09c6b6f1
Create Date: 2024-09-08 21:26:47.749870

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05e62f03001b"
down_revision = "2fae09c6b6f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stock",
        sa.Column("quantity", sa.Numeric(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["product.id"], name="stock_product_id_fk"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_product_id_uniqueness",
        "stock",
        ["product_id"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_product_id_uniqueness",
        table_name="stock",
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.drop_table("stock")
