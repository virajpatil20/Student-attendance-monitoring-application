"""Migrate attendance to lecture-session-based structure.

Revision ID: 76657232c728
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "76657232c728"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # 1. Add session_id as nullable temporarily.
    op.add_column(
        "attendance",
        sa.Column("session_id", sa.Integer(), nullable=True)
    )

    # 2. Add foreign key to lecture_sessions.
    op.create_foreign_key(
        "fk_attendance_session_id_lecture_sessions",
        "attendance",
        "lecture_sessions",
        ["session_id"],
        ["id"],
        ondelete="RESTRICT"
    )

    # 3. Make session_id mandatory.
    # Existing attendance count is currently zero.
    op.alter_column(
        "attendance",
        "session_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # 4. Remove old unique constraint.
    op.drop_constraint(
        "uq_student_course_attendance_date",
        "attendance",
        type_="unique"
    )

    # 5. Add new unique constraint.
    op.create_unique_constraint(
        "uq_student_lecture_attendance",
        "attendance",
        ["student_id", "session_id"]
    )

    # 6. Remove old foreign keys.
    op.drop_constraint(
        "attendance_course_id_fkey",
        "attendance",
        type_="foreignkey"
    )

    op.drop_constraint(
        "attendance_faculty_id_fkey",
        "attendance",
        type_="foreignkey"
    )

    # 7. Remove old indexes.
    op.drop_index(
        "ix_attendance_attendance_date",
        table_name="attendance"
    )

    op.drop_index(
        "ix_attendance_course_id",
        table_name="attendance"
    )

    op.drop_index(
        "ix_attendance_faculty_id",
        table_name="attendance"
    )

    # 8. Add session_id index.
    op.create_index(
        "ix_attendance_session_id",
        "attendance",
        ["session_id"],
        unique=False
    )

    # 9. Remove obsolete columns.
    op.drop_column("attendance", "faculty_id")
    op.drop_column("attendance", "attendance_date")
    op.drop_column("attendance", "course_id")


def downgrade() -> None:

    # Restore old columns as nullable initially.
    op.add_column(
        "attendance",
        sa.Column("course_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "attendance",
        sa.Column("attendance_date", sa.Date(), nullable=True)
    )

    op.add_column(
        "attendance",
        sa.Column("faculty_id", sa.Integer(), nullable=True)
    )

    # Restore old values using the associated lecture session.
    op.execute(
        sa.text("""
            UPDATE attendance AS a
            SET
                course_id = ls.course_id,
                attendance_date = ls.session_date,
                faculty_id = ls.faculty_id
            FROM lecture_sessions AS ls
            WHERE a.session_id = ls.id
        """)
    )

    # Restore mandatory fields.
    op.alter_column(
        "attendance",
        "course_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    op.alter_column(
        "attendance",
        "attendance_date",
        existing_type=sa.Date(),
        nullable=False
    )

    # Restore old foreign keys.
    op.create_foreign_key(
        "attendance_course_id_fkey",
        "attendance",
        "courses",
        ["course_id"],
        ["id"],
        ondelete="RESTRICT"
    )

    op.create_foreign_key(
        "attendance_faculty_id_fkey",
        "attendance",
        "faculty",
        ["faculty_id"],
        ["id"],
        ondelete="SET NULL"
    )

    # Restore old unique constraint.
    op.drop_constraint(
        "uq_student_lecture_attendance",
        "attendance",
        type_="unique"
    )

    op.create_unique_constraint(
        "uq_student_course_attendance_date",
        "attendance",
        ["student_id", "course_id", "attendance_date"]
    )

    # Restore indexes.
    op.create_index(
        "ix_attendance_course_id",
        "attendance",
        ["course_id"]
    )

    op.create_index(
        "ix_attendance_attendance_date",
        "attendance",
        ["attendance_date"]
    )

    op.create_index(
        "ix_attendance_faculty_id",
        "attendance",
        ["faculty_id"]
    )

    # Remove new foreign key and index.
    op.drop_constraint(
        "fk_attendance_session_id_lecture_sessions",
        "attendance",
        type_="foreignkey"
    )

    op.drop_index(
        "ix_attendance_session_id",
        table_name="attendance"
    )

    op.drop_column("attendance", "session_id")