from enum import Enum

from complex_epidemics.agents.support_objects.locale.locale_categories import (
    EducationalInstitutionCategory,
    HealthCareCategory,
    HouseholdCategory,
    PublicPlaceCategory,
    WorkplaceCategory,
)


class OccupationToLocale(Enum):
    WorkerCategoryGENERIC = {WorkplaceCategory.GENERIC.value}
    WorkerCategoryHEALTH = {HealthCareCategory.GENERIC.value}
    WorkerCategoryINDUSTRY = {
        WorkplaceCategory.INDUSTRY.value,
        WorkplaceCategory.GENERIC.value,
    }
    WorkerCategoryCUSTOMERSERVICES = {
        WorkplaceCategory.CUSTOMERSERVICESPLACE.value,
        WorkplaceCategory.GENERIC.value,
    }
    WorkerCategoryNONCUSTOMERSERVICES = {
        WorkplaceCategory.NONCUSTOMERSERVICESPLACE.value,
        WorkplaceCategory.GENERIC.value,
    }
    WorkerCategoryEDUCATION = {EducationalInstitutionCategory.GENERIC.value}
    WorkerCategoryPUBLIC = {PublicPlaceCategory.GENERIC.value}
    StudentCategoryGENERIC = {EducationalInstitutionCategory.GENERIC.value}
    StudentCategoryELEMENTARY = {EducationalInstitutionCategory.GENERIC.value}
    StudentCategoryMIDDLESCHOOL = {EducationalInstitutionCategory.GENERIC.value}
    StudentCategoryHIGHSCHOOL = {EducationalInstitutionCategory.GENERIC.value}
    StudentCategoryCOLLEGE = {EducationalInstitutionCategory.GENERIC.value}
    GenericOccupationCategoryGENERIC = {HouseholdCategory.GENERIC.value}
    GenericOccupationCategoryHOUSECARE = {HouseholdCategory.GENERIC.value}
    GenericOccupationCategoryRETIRED = {HouseholdCategory.GENERIC.value}
    GenericOccupationCategoryINFANT = {HouseholdCategory.GENERIC.value}
