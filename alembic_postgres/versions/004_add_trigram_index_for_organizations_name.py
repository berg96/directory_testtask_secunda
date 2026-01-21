"""add trigram index for organizations.name

Revision ID: 8f06028aa950
Revises: 9ac28b2c4e28
Create Date: 2026-01-21 00:01:15.970008

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8f06028aa950"
down_revision: Union[str, Sequence[str], None] = "9ac28b2c4e28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.create_index(
        "idx_organizations_name_trgm",
        "organizations",
        ["name"],
        schema="directory",  # если у тебя схемы
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )


def downgrade() -> None:
    op.drop_index(
        "idx_organizations_name_trgm",
        table_name="organizations",
        schema="directory",
    )
