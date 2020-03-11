"""empty message

Revision ID: b6f8c052ce11
Revises: 
Create Date: 2020-03-07 15:21:22.572509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6f8c052ce11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # op.create_table('user',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('email', sa.String(length=320), nullable=True),
    # sa.Column('username', sa.String(length=100), nullable=True),
    # sa.Column('password_hash', sa.String(length=128), nullable=True),
    # sa.Column('is_admin', sa.Boolean(), nullable=True),
    # sa.Column('gender', sa.String(length=10), nullable=True),
    # sa.Column('age_group', sa.String(length=10), nullable=True),
    # sa.Column('country_of_birth', sa.String(length=100), nullable=True),
    # sa.Column('education_level', sa.String(length=100), nullable=True),
    # sa.Column('occupation', sa.String(length=100), nullable=True),
    # sa.Column('country_born', sa.String(length=100), nullable=True),
    # sa.Column('latest_country', sa.String(length=100), nullable=True),
    # sa.Column('income', sa.String(length=100), nullable=True),
    # sa.Column('completed_form', sa.Boolean(), nullable=True),
    # sa.Column('completed_study', sa.Boolean(), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    # op.create_table('user_group',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=100), nullable=True),
    # sa.Column('User', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['User'], ['user.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    
    # op.create_table('card',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=16), nullable=True),
    # sa.Column('desc', sa.String(length=500), nullable=True),
    # sa.Column('image', sa.String(length=100), nullable=True),
    # sa.Column('creator', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['creator'], ['user.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('card_set',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=100), nullable=True),
    # sa.Column('measure', sa.String(length=100), nullable=True),
    # sa.Column('creator', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['creator'], ['user.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    op.create_table('card_sets',
    sa.Column('card_set_id', sa.Integer(), nullable=False),
    sa.Column('study_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_set_id'], ['card_set.id'], ),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ),
    sa.PrimaryKeyConstraint('card_set_id', 'study_id')
    )
    op.create_table('cards',
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('card_set_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['card_set_id'], ['card_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('card_id', 'card_set_id')
    )
    op.create_table('data_values_labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=500), nullable=True),
    sa.Column('Study', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Study'], ['study.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.Column('Study', sa.Integer(), nullable=True),
    sa.Column('cards_x', sa.JSON(), nullable=True),
    sa.Column('cards_y', sa.JSON(), nullable=True),
    sa.Column('data_values', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['Study'], ['study.id'], ),
    sa.ForeignKeyConstraint(['User'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_table('study',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=100), nullable=True),
    # sa.Column('desc', sa.String(length=100), nullable=True),
    # sa.Column('image', sa.String(length=100), nullable=True),
    # sa.Column('data_values', sa.Integer(), nullable=True),
    # sa.Column('number_of_columns', sa.Integer(), nullable=True),
    # sa.Column('number_of_rows', sa.Integer(), nullable=True),
    # sa.Column('user_group_id', sa.Integer(), nullable=True),
    # sa.Column('User', sa.Integer(), nullable=True),
    # sa.Column('start_date', sa.Date(), nullable=True),
    # sa.Column('end_date', sa.Date(), nullable=True),
    # sa.ForeignKeyConstraint(['User'], ['user.id'], ),
    # sa.ForeignKeyConstraint(['user_group_id'], ['user_group.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('study')
    op.drop_table('response')
    op.drop_table('data_values_labels')
    op.drop_table('cards')
    op.drop_table('card_sets')
    op.drop_table('card_set')
    op.drop_table('card')
    # ### end Alembic commands ###