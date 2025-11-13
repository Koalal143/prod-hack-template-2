"""Add avatar file key field for user model

Revision ID: 1492a5c8fcc2
Revises: cd5a3ffeec47
Create Date: 2025-11-13 15:46:48.469436

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1492a5c8fcc2"
down_revision: str | None = "cd5a3ffeec47"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("avatar_file_key", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_file_key")
