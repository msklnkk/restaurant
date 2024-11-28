"""empty message

Revision ID: e220ff2a0047
Revises: ce749835cd2b
Create Date: 2024-11-20 19:48:03.379635

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = 'e220ff2a0047'
down_revision = 'ce749835cd2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ordered_drinks_copy',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('orderid', sa.Integer(), nullable=True),
    sa.Column('drinkid', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='my_app_schema'
    )
    op.create_table('orders_copy',
    sa.Column('orderid', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('tableid', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.Date(), nullable=True),
    sa.Column('total_sum', sa.Numeric(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('staffid', sa.Integer(), nullable=True),
    sa.Column('clientid', sa.Integer(), nullable=True),
    sa.Column('payment_method', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('orderid'),
    schema='my_app_schema'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_copy', schema='my_app_schema')
    op.drop_table('ordered_drinks_copy', schema='my_app_schema')
    # ### end Alembic commands ###