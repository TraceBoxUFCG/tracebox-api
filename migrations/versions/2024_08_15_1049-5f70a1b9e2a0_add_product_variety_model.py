"""add_product_variety_model

Revision ID: 5f70a1b9e2a0
Revises: 14355b2275ab
Create Date: 2024-08-15 10:49:35.532103

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f70a1b9e2a0"
down_revision = "14355b2275ab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_variety",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["product.id"], name="product_variety_product_id_fk"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_product_variety_name_uniqueness",
        "product_variety",
        ["name"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        op.f("ix_product_variety_product_id"),
        "product_variety",
        ["product_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_product_variety_product_id"), table_name="product_variety")
    op.drop_index(
        "ix_product_variety_name_uniqueness",
        table_name="product_variety",
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.drop_table("product_variety")
