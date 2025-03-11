"""empty message

Revision ID: 224774cc9308
Revises: 
Create Date: 2025-02-22 14:07:02.774884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '224774cc9308'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workers2')
    op.drop_table('user')
    op.add_column('resumes', sa.Column('worker_id', sa.Integer(), nullable=False))
    op.add_column('resumes', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('resumes', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    
    # Добавляем явное преобразование с использованием USING
    op.execute('ALTER TABLE resumes ALTER COLUMN workload TYPE workload USING workload::text::workload')
    
    op.create_foreign_key(None, 'resumes', 'workers', ['worker_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'resumes', type_='foreignkey')
    op.alter_column('resumes', 'workload',
               existing_type=sa.Enum('parttime', 'fulltime', name='workload'),
               type_=sa.BOOLEAN(),
               existing_nullable=False)
    op.drop_column('resumes', 'updated_at')
    op.drop_column('resumes', 'created_at')
    op.drop_column('resumes', 'worker_id')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_table('workers2',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='workers2_pkey')
    )
    # ### end Alembic commands ###
