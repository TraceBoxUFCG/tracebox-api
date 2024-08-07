"""feat_add_supplier_table

Revision ID: 3fb3489ce42d
Revises: 8768ce960212
Create Date: 2024-08-06 08:39:59.524400

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fb3489ce42d"
down_revision = "8768ce960212"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "supplier",
        sa.Column("document", sa.String(), nullable=False),
        sa.Column("business_name", sa.String(), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_id"], ["address.id"], name="supplier_address_id_fk"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_supplier_address_id"), "supplier", ["address_id"], unique=False
    )
    op.create_index(
        "ix_supplier_document_uniqueness",
        "supplier",
        ["document"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_supplier_document_uniqueness",
        table_name="supplier",
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.drop_index(op.f("ix_supplier_address_id"), table_name="supplier")
    op.drop_table("supplier")
