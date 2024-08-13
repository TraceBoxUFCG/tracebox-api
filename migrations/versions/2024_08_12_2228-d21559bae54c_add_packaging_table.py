"""add_packaging_table

Revision ID: d21559bae54c
Revises: a9de9be8c913
Create Date: 2024-08-12 22:28:11.989178

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = "d21559bae54c"
down_revision = "a9de9be8c913"
branch_labels = None
depends_on = None


def upgrade() -> None:
    unit_enum = ENUM(
        "KG",
        "UN",
        name="unitenum",
        create_type=True,
    )
    unit_enum.create(op.get_bind(), checkfirst=False)

    op.execute(
        """
        CREATE OR REPLACE FUNCTION enum_to_text(unit_enum unitenum)
        RETURNS TEXT
        IMMUTABLE LANGUAGE SQL AS $$
        SELECT $1::text;
        $$;
    """
    )

    op.create_table(
        "packaging",
        sa.Column("quantity", sa.Numeric(), nullable=False),
        sa.Column("unit", ENUM(name="unitenum", create_type=False), nullable=False),
        sa.Column(
            "descripton",
            sa.String(),
            sa.Computed(
                "'PAC(' || quantity || enum_to_text(unit) || ')'",
            ),
            nullable=True,
        ),
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
    op.drop_table("packaging")
    op.execute("DROP FUNCTION enum_to_text")
    op.execute("DROP TYPE unitenum")
