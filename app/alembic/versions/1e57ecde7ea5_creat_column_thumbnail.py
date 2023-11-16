"""creat column thumbnail

Revision ID: 1e57ecde7ea5
Revises: 4d0d20525148
Create Date: 2023-11-12 18:01:58.230733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1e57ecde7ea5"
down_revision = "4d0d20525148"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "vendors", sa.Column("logo_thumbnail", sa.String(length=256), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("vendors", "logo_thumbnail")
    # ### end Alembic commands ###
