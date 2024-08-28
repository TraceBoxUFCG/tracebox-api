"""add_status_to_receivement_item

Revision ID: dc07d3946649
Revises: e6acb6e00b0c
Create Date: 2024-08-28 14:48:59.906049

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = "dc07d3946649"
down_revision = "e6acb6e00b0c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    receivement_item_status = ENUM(
        "PENDING",
        "RECEIVED",
        name="receivementitemstatusenum",
        create_type=True,
    )

    receivement_item_status.create(op.get_bind(), checkfirst=False)

    op.add_column(
        "receivement_item",
        sa.Column(
            "status",
            ENUM(name="receivementitemstatusenum", create_type=False),
            server_default="PENDING",
            nullable=True,
        ),
    )

    op.execute(
        """
               UPDATE
               receivement_item
               SET status = 'RECEIVED'
                """
    )

    op.alter_column("receivement_item", "status", nullable=False)


def downgrade() -> None:
    op.drop_column("receivement_item", "status")
    op.execute("DROP TYPE assetstatusenum")
