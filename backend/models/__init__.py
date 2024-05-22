from .faculty import Faculty, FacultyBase, FacultyInput, FacultyOutput
from .building import Building, BuildingBase, BuildingInput, BuildingOutput

Faculty.model_rebuild()
Building.model_rebuild()
