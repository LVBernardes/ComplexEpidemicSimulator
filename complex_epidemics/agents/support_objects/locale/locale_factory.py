import logging
from functools import partial


from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.capacity_utils import CapUtils
from complex_epidemics.utils.id_utils import IDUtils
from complex_epidemics.agents.locale import (
    HouseholdCategory,
    Locale,
    Household,
    Workplace,
    WorkplaceCategory,
    EducationalInstitution,
    EducationalInstitutionCategory,
    HealthCareUnit,
    HealthCareCategory,
    PublicPlace,
    PublicPlaceCategory,
    CustomerServicesPlace,
    NonCustomerServicesPlace,
)

LOG = logging.getLogger(__name__)


class LocaleFactory:
    @staticmethod
    def new_household(
        model: SimulationModel,
        category: HouseholdCategory = HouseholdCategory.GENERIC,
        capacity_data: dict = None,
    ) -> Household:

        if capacity_data is None:
            capacity_data = {"nominal": {"type": "uniform", "parameters": [3, 5]}}

        locale_capacity = CapUtils.generata_capacity_data(cap_input=capacity_data)

        try:
            new_locale_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_locale = new_locale_init()
            new_locale.graph_node_id = new_locale.unique_id
            new_locale.max_capacity_effective = locale_capacity["effective"]
            new_locale.max_capacity_nominal = locale_capacity["nominal"]
            new_locale.model.graph.add_node_to_component_zero(new_locale.unique_id)
            new_locale.model.schedule.add(new_locale)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_locale

    @staticmethod
    def new_workplace(
        model: SimulationModel,
        category: WorkplaceCategory = WorkplaceCategory.GENERIC,
        capacity_data: dict = None,
    ) -> Workplace:

        if capacity_data is None:
            capacity_data = {"nominal": {"type": "uniform", "parameters": [3, 5]}}

        locale_capacity = CapUtils.generata_capacity_data(cap_input=capacity_data)

        try:
            new_locale_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_locale = new_locale_init()
            new_locale.graph_node_id = new_locale.unique_id
            new_locale.max_capacity_effective = locale_capacity["effective"]
            new_locale.max_capacity_nominal = locale_capacity["nominal"]
            new_locale.model.graph.add_node_to_component_zero(new_locale.unique_id)
            new_locale.model.schedule.add(new_locale)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_locale

    @staticmethod
    def new_educational_institution(
        model: SimulationModel,
        category: EducationalInstitutionCategory = EducationalInstitutionCategory.GENERIC,
        capacity_data: dict = None,
    ) -> EducationalInstitution:

        if capacity_data is None:
            capacity_data = {
                "nominal": {"type": "uniform", "parameters": [50, 60]},
                "students": {"type": "uniform", "parameters": [45, 55]},
            }

        locale_capacity = CapUtils.generata_capacity_data(
            cap_input=capacity_data, specific_cap_type_list=["students"]
        )

        try:
            new_locale_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_locale = new_locale_init()
            new_locale.graph_node_id = new_locale.unique_id
            new_locale.max_capacity_effective = locale_capacity["effective"]
            new_locale.max_capacity_nominal = locale_capacity["nominal"]
            new_locale.max_capacity_students = locale_capacity["students"]
            new_locale.model.graph.add_node_to_component_zero(new_locale.unique_id)
            new_locale.model.schedule.add(new_locale)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_locale

    @staticmethod
    def new_health_care_unit(
        model: SimulationModel,
        category: HealthCareCategory = HealthCareCategory.GENERIC,
        capacity_data: dict = None,
    ) -> HealthCareUnit:

        if capacity_data is None:
            capacity_data = {
                "nominal": {"type": "uniform", "parameters": [13, 17]},
                "patients": {"type": "uniform", "parameters": [8, 12]},
            }

        locale_capacity = CapUtils.generata_capacity_data(
            cap_input=capacity_data, specific_cap_type_list=["patients"]
        )

        try:
            new_locale_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_locale = new_locale_init()
            new_locale.graph_node_id = new_locale.unique_id
            new_locale.max_capacity_effective = locale_capacity["effective"]
            new_locale.max_capacity_nominal = locale_capacity["nominal"]
            new_locale.max_capacity_patients = locale_capacity["patients"]
            new_locale.model.graph.add_node_to_component_zero(new_locale.unique_id)
            new_locale.model.schedule.add(new_locale)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_locale

    @staticmethod
    def new_public_place(
        model: SimulationModel,
        category: PublicPlaceCategory = PublicPlaceCategory.GENERIC,
        capacity_data: dict = None,
    ) -> PublicPlace:

        if capacity_data is None:
            capacity_data = {
                "nominal": {"type": "uniform", "parameters": [45, 55]},
                "effective": {"type": "uniform", "parameters": [65, 75]},
            }

        locale_capacity = CapUtils.generata_capacity_data(cap_input=capacity_data)

        try:
            new_locale_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_locale = new_locale_init()
            new_locale.graph_node_id = new_locale.unique_id
            new_locale.max_capacity_effective = locale_capacity["effective"]
            new_locale.max_capacity_nominal = locale_capacity["nominal"]
            new_locale.model.graph.add_node_to_component_zero(new_locale.unique_id)
            new_locale.model.schedule.add(new_locale)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_locale
