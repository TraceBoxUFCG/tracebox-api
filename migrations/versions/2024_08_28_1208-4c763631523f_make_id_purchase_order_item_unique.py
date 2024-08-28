"""make_id_purchase_order_item unique

Revision ID: 4c763631523f
Revises: 65244dda7ff9
Create Date: 2024-08-28 12:08:16.774024

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c763631523f"
down_revision = "65244dda7ff9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_purchase_order_item_id_uniqueness",
        "receivement_item",
        ["purchase_order_item_id"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_purchase_order_item_id_uniqueness",
        table_name="receivement_item",
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
