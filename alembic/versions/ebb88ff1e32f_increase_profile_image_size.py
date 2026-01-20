"""Increase profile_image size

Revision ID: ebb88ff1e32f
Revises: a0f370625a65
Create Date: 2026-01-21 00:33:42.833042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ebb88ff1e32f'
down_revision: Union[str, None] = 'a0f370625a65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "profile_image",
        existing_type=sa.String(length=500),  # adjust if yours differs
        type_=mysql.LONGTEXT(),
        existing_nullable=True,
    )

    op.alter_column(
        "product_images",
        "image_url",
        existing_type=sa.String(length=500),  # adjust if yours differs
        type_=mysql.LONGTEXT(),
        existing_nullable=True,
    )

def downgrade():
    op.alter_column(
        "users",
        "profile_image",
        existing_type=mysql.LONGTEXT(),
        type_=sa.String(length=500),
        existing_nullable=True,
    )

    op.alter_column(
        "product_images",
        "image_url",
        existing_type=mysql.LONGTEXT(),
        type_=sa.String(length=500),
        existing_nullable=True,
    )