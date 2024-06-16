from ...database.models.subject import Subject
from .schemas import SubjectOut, SubjectOutMinimal


def subject_to_out(subject: Subject) -> SubjectOut:
    from ..programmes.utils import programme_to_minimal

    return SubjectOut(
        id=subject.id,
        name=subject.name,
        abbreviation=subject.abbreviation,
        semester=subject.semester,
        course_professor_id=subject.course_professor_id,
        laboratory_professor_id=subject.laboratory_professor_id,
        seminar_professor_id=subject.seminar_professor_id,
        project_professor_id=subject.project_professor_id,
        programmes=[
            programme_to_minimal(programme) for programme in subject.programmes
        ],
    )


def subject_to_minimal(subject: Subject) -> SubjectOutMinimal:
    return SubjectOutMinimal(
        id=subject.id,
        name=subject.name,
        abbreviation=subject.abbreviation,
        semester=subject.semester,
        course_professor_id=subject.course_professor_id,
        laboratory_professor_id=subject.laboratory_professor_id,
        seminar_professor_id=subject.seminar_professor_id,
        project_professor_id=subject.project_professor_id,
    )
