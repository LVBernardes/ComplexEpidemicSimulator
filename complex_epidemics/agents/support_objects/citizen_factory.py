import logging
from types import NoneType

from complex_epidemics.agents.support_objects.human.human_builder import HumanBuilder
from complex_epidemics.agents.support_objects.human.human_occupation import (
    Worker,
    Student,
    GenericOccupation,
)
from complex_epidemics.agents.support_objects.human.human_occupation_categories import (
    GenericOccupationCategory,
    StudentCategory,
    WorkerCategory,
)
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class CitizenFactory:

    __slots__ = ["_model", "_builder"]

    def __init__(self, model: SimulationModel) -> None:
        self._model = model
        self._builder = HumanBuilder()

    @property
    def model(self) -> SimulationModel:
        return self._model

    def set_model(self, model: SimulationModel) -> None:
        self._model = model

    def new_worker(
        self, category: WorkerCategory = WorkerCategory.GENERIC, **kwargs
    ) -> None:

        attributes = dict()
        if kwargs:
            for key, value in kwargs.items():
                attributes[key] = value

        try:
            new_occupation = Worker()
            new_occupation.category = category
            self._builder.set_simulation_model(simulation_model=self.model)
            self._builder.set_occupation(occupation=new_occupation)
            self._builder.set_physical_attrs(attributes.get("physical_attrs", None))
            self._builder.set_social_attrs(attributes.get("social_attrs", None))
            self._builder.set_psychological_attrs(
                attributes.get("psychological_attrs", None)
            )
            self._builder.set_behaviour_controller(attributes.get("behaviour", None))
            self._builder.build()
            new_human = self._builder.get_result()
        except Exception as err:
            LOG.exception(err)
        else:
            return new_human

    def new_student(
        self, category: StudentCategory = StudentCategory.GENERIC, **kwargs
    ):
        attributes = dict()
        if kwargs:
            for key, value in kwargs.items():
                attributes[key] = value

        try:
            new_occupation = Student()
            new_occupation.category = category
            self._builder.set_simulation_model(simulation_model=self.model)
            self._builder.set_occupation(occupation=new_occupation)
            self._builder.set_physical_attrs(attributes.get("physical_attrs", None))
            self._builder.set_social_attrs(attributes.get("social_attrs", None))
            self._builder.set_psychological_attrs(
                attributes.get("psychological_attrs", None)
            )
            self._builder.set_behaviour_controller(attributes.get("behaviour", None))
            self._builder.build()
            new_human = self._builder.get_result()
        except Exception as err:
            LOG.exception(err)
        else:
            return new_human

    def new_generic_citizen(
        self,
        category: GenericOccupationCategory = GenericOccupationCategory.GENERIC,
        **kwargs
    ):
        attributes = dict()
        if kwargs:
            for key, value in kwargs.items():
                attributes[key] = value

        try:
            new_occupation = GenericOccupation()
            new_occupation.category = category
            self._builder.set_simulation_model(simulation_model=self.model)
            self._builder.set_occupation(occupation=new_occupation)
            self._builder.set_physical_attrs(attributes.get("physical_attrs", None))
            self._builder.set_social_attrs(attributes.get("social_attrs", None))
            self._builder.set_psychological_attrs(
                attributes.get("psychological_attrs", None)
            )
            self._builder.set_behaviour_controller(attributes.get("behaviour", None))
            self._builder.build()
            new_human = self._builder.get_result()
        except Exception as err:
            LOG.exception(err)
        else:
            return new_human
