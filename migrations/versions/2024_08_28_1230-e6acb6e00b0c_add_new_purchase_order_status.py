"""add_new_purchase_order_status

Revision ID: e6acb6e00b0c
Revises: 4c763631523f
Create Date: 2024-08-28 12:30:35.762672

"""

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e6acb6e00b0c"
down_revision = "4c763631523f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.sync_enum_values(
        "public",
        "purchaseorderstatusenum",
        [
            "DRAFT",
            "CONFIRMED",
            "RECEIVED",
            "LOTTED",
        ],
        [
            "DRAFT",
            "CONFIRMED",
            "RECEIVED",
            "LOTTED",
            "RECEIVEMENT_STARTED",
            "LOTTING_STARTED",
        ],
    )


def downgrade() -> None:
    op.sync_enum_values(
        "public",
        "purchaseorderstatusenum",
        [
            "DRAFT",
            "CONFIRMED",
            "RECEIVED",
            "LOTTED",
            "RECEIVEMENT_STARTED",
            "LOTTING_STARTED",
        ],
        [
            "DRAFT",
            "CONFIRMED",
            "RECEIVED",
            "LOTTED",
        ],
    )
