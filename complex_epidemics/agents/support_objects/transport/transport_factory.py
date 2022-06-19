import logging
from functools import partial

from complex_epidemics.agents.transport import (
    PrivateTransport,
    PrivateTransportCategory,
    PublicTransport,
    PublicTransportCategory,
    Transport,
)
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.capacity_utils import CapUtils
from complex_epidemics.utils.id_utils import IDUtils

LOG = logging.getLogger(__name__)


class TransportFactory:
    @staticmethod
    def new_public_transport(
        model: SimulationModel,
        category: PublicTransportCategory.GENERIC = PublicTransportCategory.GENERIC,
        capacity_data: dict = None,
    ) -> PublicTransport:

        if capacity_data is None:
            capacity_data = {
                "nominal": {"type": "uniform", "parameters": [20, 25]},
                "effective": {"type": "uniform", "parameters": [30, 35]},
            }

        transport_capacity = CapUtils.generata_capacity_data(cap_input=capacity_data)

        try:
            new_transport_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_transport = new_transport_init()
            new_transport.graph_node_id = new_transport.unique_id
            new_transport.max_capacity_effective = transport_capacity["effective"]
            new_transport.max_capacity_nominal = transport_capacity["nominal"]
            new_transport.model.graph.add_node_to_component_zero(
                new_transport.unique_id
            )
            new_transport.model.schedule.add(new_transport)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_transport

    @staticmethod
    def new_private_transport(
        model: SimulationModel,
        category: PrivateTransportCategory.GENERIC = PrivateTransportCategory.GENERIC,
        capacity_data: dict = None,
        owner: int = 0,
    ) -> PrivateTransport:

        if capacity_data is None:
            capacity_data = {"nominal": {"type": "uniform", "parameters": [3, 4]}}

        transport_capacity = CapUtils.generata_capacity_data(cap_input=capacity_data)

        try:
            new_transport_init = partial(
                eval(f"{category.value}"), unique_id=IDUtils.generate_id(), model=model
            )
            new_transport = new_transport_init()
            new_transport.graph_node_id = new_transport.unique_id
            new_transport.max_capacity_effective = transport_capacity["effective"]
            new_transport.max_capacity_nominal = transport_capacity["nominal"]
            new_transport.owner = owner
            new_transport.model.graph.add_node_to_component_zero(
                new_transport.unique_id
            )
            new_transport.model.schedule.add(new_transport)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return new_transport
