import logging

from complex_epidemics.agents.support_objects.locale.locale_factory import LocaleFactory
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class InfrastructureBuilder:
    def __init__(self) -> None:
        self._model = None
        self._infrastructure = list()
        self._household_config = None
        self._workplace_config = None
        self._educational_config = None
        self._healthcare_config = None
        self._public_config = None
        self._public_transport_config = None

    def _batch_processing(self, batch_data: dict) -> None:
        for data in batch_data:
            category = data.get("category")
            count = data.get("count")
            capacity = data.get("capacity")

            for _ in range(count):
                new_locale = LocaleFactory.new_workplace(
                    model=self._model, category=category, capacity_data=capacity
                )
                self._infrastructure.append(new_locale)

    def get_result(self):

        new_city = self._infrastructure
        model_enriched = self._model
        self.reset()
        return model_enriched, new_city

    def reset(self):

        self._model = None
        self._infrastructure = list()
        self._household_config = None
        self._workplace_config = None
        self._educational_config = None
        self._healthcare_config = None
        self._public_config = None
        self._public_transport_config = None

    def build(self):

        if self._model is None:
            LOG.error("Model not defined.")
            raise ValueError("Model not defined.")

        if self._household_config is not None:
            self._batch_processing(batch_data=self._household_config)

        if self._workplace_config is not None:
            self._batch_processing(batch_data=self._workplace_config)

        if self._educational_config is not None:
            self._batch_processing(batch_data=self._educational_config)

        if self._healthcare_config is not None:
            self._batch_processing(batch_data=self._healthcare_config)

        if self._public_config is not None:
            self._batch_processing(batch_data=self._public_config)

        if self._public_transport_config is not None:
            self._batch_processing(batch_data=self._public_transport_config)

    def set_model(self, model: SimulationModel) -> None:
        self._model = model

    def set_household_config(self, household_config: dict = None) -> None:
        self._household_config = household_config
        # workplace_data = [
        #     {
        #         'category': WorkplaceCategory.GENERIC,
        #         'count': 10,
        #         'capacity': {
        #             'nominal': {
        #                 'type': 'normal',
        #                 'parameters': [15, 3.5]
        #             }
        #         }
        #     }
        # ]

    def set_workplace_config(self, workplace_config: dict = None) -> None:
        self._workplace_config = workplace_config

    def set_educational_config(self, educational_config: dict = None) -> None:
        self._educational_config = educational_config

    def set_healthcare_config(self, healthcare_config: dict = None) -> None:
        self._healthcare_config = healthcare_config

    def set_public_config(self, public_config: dict = None) -> None:
        self._public_config = public_config

    def set_public_transport_config(self, public_transport_config: dict = None) -> None:
        self._public_transport_config = public_transport_config
