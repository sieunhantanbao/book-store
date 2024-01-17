"""Add new column new

Revision ID: 54dc23367250
Revises: 74c0343d846e
Create Date: 2024-01-11 13:22:12.667096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54dc23367250'
down_revision = '74c0343d846e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'book', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_column('book', 'category_id')
    # ### end Alembic commands ###
