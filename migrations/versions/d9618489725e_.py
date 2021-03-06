"""empty message

Revision ID: d9618489725e
Revises: 56b276095242
Create Date: 2017-02-05 18:33:02.324697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9618489725e'
down_revision = '56b276095242'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('label', 'name',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    op.drop_constraint('label_name_key', 'label', type_='unique')
    op.create_unique_constraint(None, 'project', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='unique')
    op.create_unique_constraint('label_name_key', 'label', ['name'])
    op.alter_column('label', 'name',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
    # ### end Alembic commands ###
