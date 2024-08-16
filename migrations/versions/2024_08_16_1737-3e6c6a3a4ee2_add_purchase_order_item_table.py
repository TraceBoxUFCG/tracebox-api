"""add_purchase_order_item_table

Revision ID: 3e6c6a3a4ee2
Revises: 2d7c3e26449d
Create Date: 2024-08-16 17:37:38.068956

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e6c6a3a4ee2"
down_revision = "2d7c3e26449d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "purchase_order_item",
        sa.Column("purchase_order_id", sa.Integer(), nullable=False),
        sa.Column("product_variety_id", sa.Integer(), nullable=False),
        sa.Column("boxes_quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_variety_id"],
            ["product_variety.id"],
            name="purchase_order_item_product_variety_id_fk",
        ),
        sa.ForeignKeyConstraint(
            ["purchase_order_id"],
            ["purchase_order.id"],
            name="purchase_order_item_purchase_order_id_fk",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_purchase_order_item_product_variety_id"),
        "purchase_order_item",
        ["product_variety_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_purchase_order_item_purchase_order_id"),
        "purchase_order_item",
        ["purchase_order_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_purchase_order_item_purchase_order_id"),
        table_name="purchase_order_item",
    )
    op.drop_index(
        op.f("ix_purchase_order_item_product_variety_id"),
        table_name="purchase_order_item",
    )
    op.drop_table("purchase_order_item")
