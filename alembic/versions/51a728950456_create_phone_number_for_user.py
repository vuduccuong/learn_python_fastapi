"""create phone number for user

Revision ID: 51a728950456
Revises: 
Create Date: 2022-09-27 08:37:33.835832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "51a728950456"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(15), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
