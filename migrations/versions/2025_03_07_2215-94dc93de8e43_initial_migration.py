"""initial migration

Revision ID: 94dc93de8e43
Revises: 
Create Date: 2025-03-07 22:15:11.820856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94dc93de8e43'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.Unicode(length=255), nullable=False),
    sa.Column('email', sa.Unicode(length=255), nullable=False),
    sa.Column('password_hash', sa.Unicode(length=255), nullable=False),
    sa.Column('username', sa.Unicode(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('projects',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.Unicode(length=255), nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False),
    sa.Column('description', sa.Unicode(length=255), nullable=False),
    sa.Column('created_by', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('tasks',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.Unicode(length=255), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=False),
    sa.Column('description', sa.Unicode(length=255), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('project_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('timesheets',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.Unicode(length=255), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('task_id', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('hours_worked', sa.Float(), nullable=False),
    sa.Column('sap_hours', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timesheets')
    op.drop_table('tasks')
    op.drop_table('projects')
    op.drop_table('users')
    # ### end Alembic commands ###
