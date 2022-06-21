from enum import Enum


class HouseholdCategory(Enum):
    GENERIC = "Household"


class WorkplaceCategory(Enum):
    GENERIC = "Workplace"
    CUSTOMERSERVICESPLACE = "CustomerServicesPlace"
    NONCUSTOMERSERVICESPLACE = "NonCustomerServicesPlace"
    INDUSTRY = "Industry"


class EducationalInstitutionCategory(Enum):
    GENERIC = "EducationalInstitution"
    # PRIMARY = 'Primary'
    # SECONDARY = 'Secondary'
    # COLLEGE = 'College'


class HealthCareCategory(Enum):
    GENERIC = "HealthCareUnit"
    # SMALLCLINIC = 'SmallClinic'
    # LARGECLINIC = 'LargeClinic'
    # HOSPITAL = 'Hospital'


class PublicPlaceCategory(Enum):
    GENERIC = "PublicPlace"
    # PARK = 'Park'
    # THEATER = 'Theater'
    # MOVIETHEATER = 'Movietheater'
