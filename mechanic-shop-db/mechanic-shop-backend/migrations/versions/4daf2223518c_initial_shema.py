"""Initial shema

Revision ID: 4daf2223518c
Revises:
Create Date: 2025-06-18 01:46:10.545270
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4daf2223518c'
down_revision = None
branch_labels = None
depends_on = None

# --- define the enum ONCE and reuse it ---
service_ticket_status_enum = sa.Enum(
    'open', 'in_progress', 'closed',
    name='service_ticket_status'
)

def upgrade():
    # Create the enum type before using it in a column (idempotent on re-run)
    bind = op.get_bind()
    service_ticket_status_enum.create(bind, checkfirst=True)

    op.create_table(
        'customer',
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('address', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('customer_id')
    )

    op.create_table(
        'mechanic',
        sa.Column('mechanic_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('address', sa.String(length=200), nullable=True),
        sa.Column('salary', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.PrimaryKeyConstraint('mechanic_id')
    )

    op.create_table(
        'vehicle',
        sa.Column('vin', sa.String(length=17), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('make', sa.String(length=50), nullable=True),
        sa.Column('model', sa.String(length=50), nullable=True),
        sa.Column('year', sa.SmallInteger(), nullable=True),
        sa.Column('license_plate', sa.String(length=15), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('vin')
    )

    op.create_table(
        'service_ticket',
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('vin', sa.String(length=17), nullable=False),
        sa.Column('date_in', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('date_out', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', service_ticket_status_enum, nullable=False),  # use the defined enum
        sa.Column('total_cost', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['vin'], ['vehicle.vin'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ticket_id')
    )

    op.create_table(
        'service_assignment',
        sa.Column('service_ticket_id', sa.Integer(), nullable=False),
        sa.Column('mechanic_id', sa.Integer(), nullable=False),
        sa.Column('hours_worked', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['mechanic_id'], ['mechanic.mechanic_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['service_ticket_id'], ['service_ticket.ticket_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('service_ticket_id', 'mechanic_id')
    )

def downgrade():
    op.drop_table('service_assignment')
    op.drop_table('service_ticket')
    op.drop_table('vehicle')
    op.drop_table('mechanic')
    op.drop_table('customer')
    # Drop the enum type after tables that used it have been dropped
    bind = op.get_bind()
    service_ticket_status_enum.drop(bind, checkfirst=True)
