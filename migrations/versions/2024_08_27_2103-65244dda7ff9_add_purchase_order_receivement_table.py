"""add_purchase_order_receivement_table

Revision ID: 65244dda7ff9
Revises: 3e6c6a3a4ee2
Create Date: 2024-08-27 21:03:18.490295

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "65244dda7ff9"
down_revision = "3e6c6a3a4ee2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "purchase_order_receivement",
        sa.Column("purchase_order_item_id", sa.Integer(), nullable=False),
        sa.Column("received_quantity", sa.Numeric(), nullable=False),
        sa.Column("rejected_quantity", sa.Numeric(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["purchase_order_item_id"],
            ["purchase_order_item.id"],
            name="purchase_order_receivement_purchase_order_item_id_fk",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_purchase_order_receivement_purchase_order_item_id"),
        "purchase_order_receivement",
        ["purchase_order_item_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_purchase_order_receivement_purchase_order_item_id"),
        table_name="purchase_order_receivement",
    )
    op.drop_table("purchase_order_receivement")
