"""add_product_table

Revision ID: a9de9be8c913
Revises: 3fb3489ce42d
Create Date: 2024-08-12 22:06:50.259060

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a9de9be8c913"
down_revision = "3fb3489ce42d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("average_unit_weight", sa.Numeric(), nullable=False),
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
    op.create_index(
        "ix_product_name_uniqueness",
        "product",
        ["name"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_product_name_uniqueness",
        table_name="product",
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.drop_table("product")
