"""3

Revision ID: 6864ca7d6b89
Revises: a4d2d00c21f4
Create Date: 2024-03-16 21:00:45.638520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6864ca7d6b89'
down_revision = 'a4d2d00c21f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faq', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faq', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
