"""migration 1

Revision ID: b16066c56f35
Revises: 423d928cb4f3
Create Date: 2024-03-14 12:58:11.540490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b16066c56f35'
down_revision = '423d928cb4f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assign_badge', schema=None) as batch_op:
        batch_op.alter_column('badge_name',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assign_badge', schema=None) as batch_op:
        batch_op.alter_column('badge_name',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
