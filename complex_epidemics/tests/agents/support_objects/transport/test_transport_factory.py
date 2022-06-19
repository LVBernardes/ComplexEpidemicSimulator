from mesa.time import BaseScheduler


from complex_epidemics.agents.support_objects.transport.transport_factory import (
    TransportFactory,
)
from complex_epidemics.agents.transport import PrivateTransport, PublicTransport
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestLocaleFactory:
    def test_instantiation(self):

        new_factory = TransportFactory()

        assert isinstance(new_factory, TransportFactory)

    def test_method_new_public_transport(self):

        new_factory = TransportFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {
            "nominal": {"type": "none", "parameters": [25]},
            "effective": {"type": "none", "parameters": [40]},
        }

        public_transport_a = new_factory.new_public_transport(model=model)
        public_transport_b = new_factory.new_public_transport(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(public_transport_a, PublicTransport)
            and public_transport_b.max_capacity_nominal == 25
        )

    def test_method_new_private_transport(self):

        new_factory = TransportFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {"nominal": {"type": "none", "parameters": [7]}}

        private_transport_a = new_factory.new_private_transport(model=model)
        private_transport_b = new_factory.new_private_transport(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(private_transport_a, PrivateTransport)
            and private_transport_b.max_capacity_nominal == 7
        )
