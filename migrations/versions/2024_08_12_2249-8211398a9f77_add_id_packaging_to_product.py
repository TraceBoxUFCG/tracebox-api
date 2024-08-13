"""add_id_packaging_to_product

Revision ID: 8211398a9f77
Revises: d21559bae54c
Create Date: 2024-08-12 22:49:14.144556

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8211398a9f77"
down_revision = "d21559bae54c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("product", sa.Column("packaging_id", sa.Integer(), nullable=False))
    op.create_index(
        op.f("ix_product_packaging_id"), "product", ["packaging_id"], unique=False
    )
    op.create_foreign_key(
        "product_packaging_id_fk", "product", "packaging", ["packaging_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("product_packaging_id_fk", "product", type_="foreignkey")
    op.drop_index(op.f("ix_product_packaging_id"), table_name="product")
    op.drop_column("product", "packaging_id")
