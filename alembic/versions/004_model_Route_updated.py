"""updated ROUTE model

Revision ID: 63096a400fa1
Revises: 66f467264ee5
Create Date: 2025-01-03 00:53:24.712705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '63096a400fa1'
down_revision: Union[str, None] = '66f467264ee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('routes', 'route_id', new_column_name='id')

    op.drop_constraint('coordinates_route_id_fkey', 'coordinates', type_='foreignkey')
    op.create_foreign_key(None, 'coordinates', 'routes', ['route_id'], ['id'])
    op.drop_column('coordinates', 'locname')

    op.add_column('estimations', sa.Column('value', sa.Integer(), nullable=False))
    op.drop_constraint('estimations_route_id_fkey', 'estimations', type_='foreignkey')
    op.drop_constraint('estimations_estimator_id_fkey', 'estimations', type_='foreignkey')
    op.create_foreign_key(None, 'estimations', 'routes', ['route_id'], ['id'])
    op.drop_column('estimations', 'estimator_id')
    op.drop_column('estimations', 'estimation_value')

    op.add_column('routes', sa.Column('users_travel_speed', sa.Integer(), nullable=True))
    op.add_column('routes', sa.Column('users_transport', sa.String(), nullable=True))
    op.add_column('routes', sa.Column('created_time', sa.DateTime(), nullable=True))
    op.add_column('routes', sa.Column('locname_start', sa.String(), nullable=True))
    op.add_column('routes', sa.Column('locname_finish', sa.String(), nullable=True))
    op.drop_column('routes', 'avg_travel_velo_time')
    op.drop_column('routes', 'operation_time')
    op.drop_column('routes', 'avg_travel_time_on_foot')

    op.drop_column('users', 'favorite_routes')


def downgrade() -> None:
    op.add_column('users',
                  sa.Column('favorite_routes', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))

    op.add_column('routes', sa.Column('avg_travel_time_on_foot', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('routes', sa.Column('operation_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('routes', sa.Column('avg_travel_velo_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('routes', 'locname_finish')
    op.drop_column('routes', 'locname_start')
    op.drop_column('routes', 'created_time')
    op.drop_column('routes', 'users_transport')
    op.drop_column('routes', 'users_travel_speed')
    op.alter_column('routes', 'id', new_column_name='route_id')

    op.add_column('estimations', sa.Column('estimation_value', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('estimations', sa.Column('estimator_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'estimations', type_='foreignkey')
    op.create_foreign_key('estimations_estimator_id_fkey', 'estimations', 'users', ['estimator_id'], ['id'])
    op.create_foreign_key('estimations_route_id_fkey', 'estimations', 'routes', ['route_id'], ['route_id'])
    op.drop_column('estimations', 'value')

    op.add_column('coordinates', sa.Column('locname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'coordinates', type_='foreignkey')
    op.create_foreign_key('coordinates_route_id_fkey', 'coordinates', 'routes', ['route_id'], ['route_id'])
