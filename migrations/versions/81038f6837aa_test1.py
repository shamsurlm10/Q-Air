"""test1

Revision ID: 81038f6837aa
Revises: 
Create Date: 2022-05-07 15:20:52.737597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81038f6837aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flight_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_name', sa.String(), nullable=True),
    sa.Column('airplane_id', sa.Integer(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['airplane_id'], ['airplane.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('flight_id', sa.Integer(), nullable=True),
    sa.Column('seat_no', sa.Integer(), nullable=True),
    sa.Column('eticket_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flight.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    op.drop_table('flight_class')
    # ### end Alembic commands ###
