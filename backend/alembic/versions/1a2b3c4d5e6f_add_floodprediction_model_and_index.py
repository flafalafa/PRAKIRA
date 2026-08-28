"""Add FloodPrediction model and index

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2026-08-08 22:59:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create Enum types
    risk_level_enum = postgresql.ENUM('VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME', name='risklevel')
    risk_level_enum.create(op.get_bind())
    
    prediction_status_enum = postgresql.ENUM('DRAFT', 'GENERATED', 'VALIDATED', 'EXPIRED', 'CANCELLED', name='predictionstatus')
    prediction_status_enum.create(op.get_bind())

    # Create flood_predictions table
    op.create_table(
        'flood_predictions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('prediction_code', sa.String(50), nullable=False),
        sa.Column('area_id', sa.String(36), nullable=False),
        sa.Column('river_id', sa.String(36), nullable=True),
        sa.Column('prediction_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('forecast_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('forecast_end', sa.DateTime(timezone=True), nullable=False),
        sa.Column('prediction_source', sa.String(100), nullable=False),
        sa.Column('prediction_method', sa.String(100), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('flood_probability', sa.Float(), nullable=False),
        sa.Column('estimated_flood_depth', sa.Float(), nullable=False),
        sa.Column('estimated_arrival_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expected_duration_seconds', sa.Float(), nullable=False),
        sa.Column('rainfall_reference', sa.String(100), nullable=True),
        sa.Column('river_reference', sa.String(100), nullable=True),
        sa.Column('weather_reference', sa.String(100), nullable=True),
        sa.Column('recommended_action', sa.String(500), nullable=False),
        sa.Column('risk_level', postgresql.ENUM(name='risklevel', create_type=False), nullable=False),
        sa.Column('status', postgresql.ENUM(name='predictionstatus', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Create Indexes
    op.create_index(op.f('ix_flood_predictions_area_id'), 'flood_predictions', ['area_id'], unique=False)
    op.create_index(op.f('ix_flood_predictions_prediction_code'), 'flood_predictions', ['prediction_code'], unique=True)
    # The REQUIRED Index for Prediction History filtering (P2 Remediation)
    op.create_index(op.f('ix_flood_predictions_prediction_time'), 'flood_predictions', ['prediction_time'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_flood_predictions_prediction_time'), table_name='flood_predictions')
    op.drop_index(op.f('ix_flood_predictions_prediction_code'), table_name='flood_predictions')
    op.drop_index(op.f('ix_flood_predictions_area_id'), table_name='flood_predictions')
    op.drop_table('flood_predictions')
    
    risk_level_enum = postgresql.ENUM('VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME', name='risklevel')
    risk_level_enum.drop(op.get_bind())
    prediction_status_enum = postgresql.ENUM('DRAFT', 'GENERATED', 'VALIDATED', 'EXPIRED', 'CANCELLED', name='predictionstatus')
    prediction_status_enum.drop(op.get_bind())
