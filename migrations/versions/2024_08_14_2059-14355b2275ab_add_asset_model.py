"""add_asset_model

Revision ID: 14355b2275ab
Revises: 8211398a9f77
Create Date: 2024-08-14 20:59:45.521046

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = "14355b2275ab"
down_revision = "8211398a9f77"
branch_labels = None
depends_on = None


def upgrade() -> None:
    asset_status_enum = ENUM(
        "EMPTY",
        "OCCUPIED",
        "DISABLED",
        name="assetstatusenum",
        create_type=True,
    )

    asset_status_enum.create(op.get_bind(), checkfirst=False)
    op.create_table(
        "asset",
        sa.Column(
            "status",
            ENUM(name="assetstatusenum", create_type=False),
            server_default="EMPTY",
            nullable=False,
        ),
        sa.Column("packaging_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["packaging_id"], ["packaging.id"], name="asset_packaging_id_fk"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("asset")
    op.execute("DROP TYPE assetstatusenum")
