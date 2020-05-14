"""empty message

Revision ID: 291b09f1d83c
Revises: a391c2d1df2d
Create Date: 2020-05-13 23:28:45.548174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '291b09f1d83c'
down_revision = 'a391c2d1df2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('Admin', sa.Integer(), nullable=True))
    op.add_column('card', sa.Column('card_set_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card', 'card_set', ['card_set_id'], ['id'])
    op.create_foreign_key(None, 'card', 'user', ['Admin'], ['id'])
    op.add_column('card_position', sa.Column('Card', sa.Integer(), nullable=True))
    op.add_column('card_position', sa.Column('Response', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card_position', 'response', ['Response'], ['id'])
    op.create_foreign_key(None, 'card_position', 'card', ['Card'], ['id'])
    op.add_column('card_set', sa.Column('Admin', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card_set', 'user', ['Admin'], ['id'])
    op.add_column('data_value', sa.Column('DataValueLabel', sa.Integer(), nullable=True))
    op.add_column('data_value', sa.Column('Response', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'data_value', 'data_value_label', ['DataValueLabel'], ['id'])
    op.create_foreign_key(None, 'data_value', 'response', ['Response'], ['id'])
    op.add_column('data_value_label', sa.Column('Admin', sa.Integer(), nullable=True))
    op.add_column('data_value_label', sa.Column('Study', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'data_value_label', 'user', ['Admin'], ['id'])
    op.create_foreign_key(None, 'data_value_label', 'study', ['Study'], ['id'])
    op.add_column('response', sa.Column('Participant', sa.Integer(), nullable=True))
    op.add_column('response', sa.Column('Study', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'response', 'user', ['Participant'], ['id'])
    op.create_foreign_key(None, 'response', 'study', ['Study'], ['id'])
    op.add_column('study', sa.Column('Admin', sa.Integer(), nullable=True))
    op.add_column('study', sa.Column('card_set_x_id', sa.Integer(), nullable=True))
    op.add_column('study', sa.Column('card_set_y_id', sa.Integer(), nullable=True))
    op.add_column('study', sa.Column('user_group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'study', 'user', ['Admin'], ['id'])
    op.create_foreign_key(None, 'study', 'user_group', ['user_group_id'], ['id'])
    op.create_foreign_key(None, 'study', 'card_set', ['card_set_x_id'], ['id'])
    op.create_foreign_key(None, 'study', 'card_set', ['card_set_y_id'], ['id'])
    op.add_column('user', sa.Column('UserGroup', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'user_group', ['UserGroup'], ['id'])
    op.add_column('user_group', sa.Column('Admin', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_group', 'user', ['Admin'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_group', type_='foreignkey')
    op.drop_column('user_group', 'Admin')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'UserGroup')
    op.drop_constraint(None, 'study', type_='foreignkey')
    op.drop_constraint(None, 'study', type_='foreignkey')
    op.drop_constraint(None, 'study', type_='foreignkey')
    op.drop_constraint(None, 'study', type_='foreignkey')
    op.drop_column('study', 'user_group_id')
    op.drop_column('study', 'card_set_y_id')
    op.drop_column('study', 'card_set_x_id')
    op.drop_column('study', 'Admin')
    op.drop_constraint(None, 'response', type_='foreignkey')
    op.drop_constraint(None, 'response', type_='foreignkey')
    op.drop_column('response', 'Study')
    op.drop_column('response', 'Participant')
    op.drop_constraint(None, 'data_value_label', type_='foreignkey')
    op.drop_constraint(None, 'data_value_label', type_='foreignkey')
    op.drop_column('data_value_label', 'Study')
    op.drop_column('data_value_label', 'Admin')
    op.drop_constraint(None, 'data_value', type_='foreignkey')
    op.drop_constraint(None, 'data_value', type_='foreignkey')
    op.drop_column('data_value', 'Response')
    op.drop_column('data_value', 'DataValueLabel')
    op.drop_constraint(None, 'card_set', type_='foreignkey')
    op.drop_column('card_set', 'Admin')
    op.drop_constraint(None, 'card_position', type_='foreignkey')
    op.drop_constraint(None, 'card_position', type_='foreignkey')
    op.drop_column('card_position', 'Response')
    op.drop_column('card_position', 'Card')
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.drop_column('card', 'card_set_id')
    op.drop_column('card', 'Admin')
    # ### end Alembic commands ###