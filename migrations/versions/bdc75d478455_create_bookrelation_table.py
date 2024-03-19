"""create bookrelation table

Revision ID: bdc75d478455
Revises: 400578f219d9
Create Date: 2024-03-17 14:52:16.816153

"""
from typing import Sequence, Union
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdc75d478455'
down_revision: Union[str, None] = '400578f219d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("book_relations",
                    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
                    sa.Column('book_id_1', sa.UUID, nullable=False),
                    sa.Column("book_id_2", sa.UUID, nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.now()),
                    sa.Column('updated_at', sa.DateTime))
    op.create_foreign_key("fb_book_id_1", "book_relations", "books", ['book_id_1'], ['id'])
    op.create_foreign_key("fb_book_id_2", "book_relations", "books", ['book_id_2'], ['id'])

def downgrade() -> None:
    op.drop_table("book_relations")