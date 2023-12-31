"""add table attribute

Revision ID: 197039e4c21e
Revises: 
Create Date: 2023-11-11 08:18:26.498441

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "197039e4c21e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attribute",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_attribute_id"), "attribute", ["id"], unique=False)
    op.create_index(op.f("ix_attribute_name"), "attribute", ["name"], unique=False)
    op.add_column("product", sa.Column("id_attribute", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "product", "attribute", ["id_attribute"], ["id"])
    op.drop_column("product", "attribute")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product", sa.Column("attribute", mysql.VARCHAR(length=256), nullable=True)
    )
    op.drop_constraint(None, "product", type_="foreignkey")
    op.drop_column("product", "id_attribute")
    op.drop_index(op.f("ix_attribute_name"), table_name="attribute")
    op.drop_index(op.f("ix_attribute_id"), table_name="attribute")
    op.drop_table("attribute")
    # ### end Alembic commands ###
