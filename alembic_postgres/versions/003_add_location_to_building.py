"""add location to Building

Revision ID: 9ac28b2c4e28
Revises: 4c6f4416435a
Create Date: 2026-01-20 22:59:56.802331

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ac28b2c4e28"
down_revision: Union[str, Sequence[str], None] = "4c6f4416435a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.add_column(
        "buildings",
        sa.Column("location", geoalchemy2.types.Geography(geometry_type="POINT", srid=4326), nullable=False),
        schema="directory",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_buildings_location", table_name="buildings", schema="directory")
    op.drop_column("buildings", "location", schema="directory")
    # ### end Alembic commands ###
