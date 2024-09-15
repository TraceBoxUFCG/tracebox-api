"""add_stock_transaction_table

Revision ID: f7ce66c87ead
Revises: 05e62f03001b
Create Date: 2024-09-15 17:05:32.171425

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = "f7ce66c87ead"
down_revision = "05e62f03001b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    stock_transaction_type_enum = ENUM(
        "ENTRY",
        "OUT",
        name="stocktransactiontypeenum",
        create_type=True,
    )
    stock_transaction_type_enum.create(op.get_bind(), checkfirst=False)

    op.create_table(
        "stock_transaction",
        sa.Column("quantity", sa.Numeric(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("packaging_id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            ENUM(name="stocktransactiontypeenum", create_type=False),
            nullable=False,
        ),
        sa.Column("meta", sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["packaging_id"], ["packaging.id"], name="stock_transaction_packaging_id_fk"
        ),
        sa.ForeignKeyConstraint(
            ["product_id"], ["product.id"], name="stock_transaction_product_id_fk"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("stock_transaction")
    op.execute("DROP TYPE stocktransactiontypeenum")
