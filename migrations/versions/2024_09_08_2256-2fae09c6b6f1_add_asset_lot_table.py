"""add_asset_lot_table

Revision ID: 2fae09c6b6f1
Revises: dc07d3946649
Create Date: 2024-09-08 22:56:03.412865

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2fae09c6b6f1"
down_revision = "dc07d3946649"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "asset_lot",
        sa.Column("receivement_item_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"], ["asset.id"], name="asset_lot_asset_id_fk"
        ),
        sa.ForeignKeyConstraint(
            ["receivement_item_id"],
            ["receivement_item.id"],
            name="asset_lot_receivement_item_id_fk",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_asset_lot_asset_id"), "asset_lot", ["asset_id"], unique=False
    )
    op.create_index(
        op.f("ix_asset_lot_receivement_item_id"),
        "asset_lot",
        ["receivement_item_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_asset_lot_receivement_item_id"), table_name="asset_lot")
    op.drop_index(op.f("ix_asset_lot_asset_id"), table_name="asset_lot")
    op.drop_table("asset_lot")
