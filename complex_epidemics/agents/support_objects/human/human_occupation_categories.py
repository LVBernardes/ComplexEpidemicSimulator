from enum import Enum


class WorkerCategory(Enum):
    GENERIC = "GenericWorker"
    HEALTH = "HealthWorker"
    INDUSTRY = "IndustryWorker"
    CUSTOMERSERVICES = "CustomerServicesWorker"
    NONCUSTOMERSERVICES = "NonCustomerServicesWorker"
    EDUCATION = "EducationWorker"
    PUBLIC = "PublicServiceWorker"


class StudentCategory(Enum):
    GENERIC = "GenericStudent"
    ELEMENTARY = "ElementaryStudent"
    MIDDLESCHOOL = "MiddleSchoolStudent"
    HIGHSCHOOL = "HighSchoolStudent"
    COLLEGE = "CollegeStudent"


class GenericOccupationCategory(Enum):
    GENERIC = "GenericOccupation"
    HOUSECARE = "Housecare"
    RETIRED = "Retired"
    INFANT = "Infant"
