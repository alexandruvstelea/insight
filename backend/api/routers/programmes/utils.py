from ...database.models.programme import Programme
from .schemas import ProgrammeOut, ProgrammeOutMinimal


def programme_to_out(programme: Programme) -> ProgrammeOut:
    from ..faculties.utils import faculty_to_minimal
    from ..subjects.utils import subject_to_minimal

    return ProgrammeOut(
        id=programme.id,
        name=programme.name,
        type=programme.type,
        abbreviation=programme.abbreviation,
        faculty=faculty_to_minimal(programme.faculty),
        subjects=[subject_to_minimal(subject) for subject in programme.subjects],
    )
