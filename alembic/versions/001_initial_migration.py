"""Initial migration

Revision ID: 9fb924c39e4b
Revises: 
Create Date: 2024-12-22 09:10:42.992731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fb924c39e4b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('telephone_number', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('favorite_routes', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('salt_hashed_password', sa.String(), nullable=False),
    sa.Column('token_mobile', sa.String(), nullable=False),
    sa.Column('authorized_time', sa.DateTime(), nullable=True),
    sa.Column('birth', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routes',
    sa.Column('route_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('users_travel_time', sa.Integer(), nullable=True),
    sa.Column('avg_travel_time_on_foot', sa.Integer(), nullable=True),
    sa.Column('avg_travel_velo_time', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('operation_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('route_id'),
    sa.UniqueConstraint('route_id')
    )
    op.create_table('coordinates',
    sa.Column('cord_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('locname', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['route_id'], ['routes.route_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('cord_id')
    )
    op.create_table('estimations',
    sa.Column('estimation_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('estimation_value', sa.Integer(), nullable=False),
    sa.Column('estimator_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['estimator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['routes.route_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('estimation_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('estimations')
    op.drop_table('coordinates')
    op.drop_table('routes')
    op.drop_table('users')
    # ### end Alembic commands ###