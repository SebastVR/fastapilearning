"""Create project and detection table

Revision ID: f7e32fb7397a
Revises: 47cc2fee693b
Create Date: 2024-04-26 05:01:53.787551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f7e32fb7397a"
down_revision: Union[str, None] = "47cc2fee693b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.create_index(op.f("ix_projects_name"), "projects", ["name"], unique=False)

    op.create_table(
        "detections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("datalake_image_path", sa.String(), nullable=True),
        sa.Column("arnes", sa.Integer(), nullable=False),
        sa.Column("barbuquejo", sa.Integer(), nullable=False),
        sa.Column("botas", sa.Integer(), nullable=False),
        sa.Column("casco", sa.Integer(), nullable=False),
        sa.Column("chaleco", sa.Integer(), nullable=False),
        sa.Column("eslingas", sa.Integer(), nullable=False),
        sa.Column("guantes", sa.Integer(), nullable=False),
        sa.Column("personas", sa.Integer(), nullable=False),
        sa.Column("proteccion_auditiva", sa.Integer(), nullable=False),
        sa.Column("proteccion_respiratoria", sa.Integer(), nullable=False),
        sa.Column("proteccion_visual", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_detections_id"), "detections", ["id"], unique=False)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_detections_id"), table_name="detections")
    op.drop_table("detections")

    op.drop_index(op.f("ix_projects_name"), table_name="projects")
    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.drop_table("projects")
