"""add_purchase_order_table

Revision ID: 2d7c3e26449d
Revises: 5f70a1b9e2a0
Create Date: 2024-08-16 17:29:43.031538

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = "2d7c3e26449d"
down_revision = "5f70a1b9e2a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    purchase_order_status_enum = ENUM(
        "DRAFT",
        "CONFIRMED",
        "RECEIVED",
        "LOTTED",
        name="purchaseorderstatusenum",
        create_type=True,
    )
    purchase_order_status_enum.create(op.get_bind(), checkfirst=False)

    op.create_table(
        "purchase_order",
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("expected_arrival_date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            ENUM(name="purchaseorderstatusenum", create_type=False),
            server_default="DRAFT",
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["supplier_id"], ["supplier.id"], name="purchase_order_supplier_id_fk"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_purchase_order_supplier_id"),
        "purchase_order",
        ["supplier_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_purchase_order_supplier_id"), table_name="purchase_order")
    op.drop_table("purchase_order")
    op.execute("DROP TYPE purchaseorderstatusenum")
