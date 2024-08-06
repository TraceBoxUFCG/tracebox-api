"""add_address_table

Revision ID: 8768ce960212
Revises:
Create Date: 2024-08-06 02:51:44.170159

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = "8768ce960212"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    states_enum = ENUM(
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
        name="statesenum",
        create_type=True,
    )
    states_enum.create(op.get_bind(), checkfirst=False)
    op.create_table(
        "address",
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", ENUM(name="statesenum", create_type=False), nullable=True),
        sa.Column("street", sa.String(), nullable=True),
        sa.Column("zipcode", sa.String(), nullable=True),
        sa.Column("number", sa.String(), nullable=True),
        sa.Column("complement", sa.String(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("address")
    op.execute("DROP TYPE statesenum")
