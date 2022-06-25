from pprint import pprint

from complex_epidemics.agents.human import Human
from complex_epidemics.agents.locale import Locale
from complex_epidemics.agents.transport import Transport
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestSimulationModel:
    def test_class_instantiation(self):

        new_model = SimulationModel()

        assert isinstance(new_model, SimulationModel)

    def test_class_attributes_required(self):

        nem_model = SimulationModel()

        assert (
            hasattr(nem_model, "step")
            and hasattr(nem_model, "clock")
            and hasattr(nem_model, "graph")
            and hasattr(nem_model, "schedule")
        )

    def test_method_get_agents_by_class(self):

        model = SimulationModel()
        expected_locale_agent_id_list = list()
        expected_transport_agent_id_list = list()
        for i in range(0, 10):
            model.schedule.add(Locale(unique_id=i, model=model))
            expected_locale_agent_id_list.append(i)
        for i in range(10, 20):
            model.schedule.add(Transport(unique_id=i, model=model))
            expected_transport_agent_id_list.append(i)

        result_locale_agent_id_list = model.get_agents_by_class("Locale")
        result_transport_agent_id_list = model.get_agents_by_class("Transport")

        assert (
            expected_locale_agent_id_list == result_locale_agent_id_list
            and expected_transport_agent_id_list == result_transport_agent_id_list
        )

    def test_method_container_agents_getter(self):

        model = SimulationModel()
        locale_agent_id_list = list()
        transport_agent_id_list = list()
        for i in range(0, 10):
            model.schedule.add(Locale(unique_id=i, model=model))
            locale_agent_id_list.append(i)
        for i in range(10, 20):
            model.schedule.add(Transport(unique_id=i, model=model))
            transport_agent_id_list.append(i)

        expected_agent_id_list = locale_agent_id_list + transport_agent_id_list

        result_agent_id_list = model.container_agents

        assert expected_agent_id_list == result_agent_id_list

    def test_method_mobile_agents_getter(self):

        model = SimulationModel()
        human_agent_id_list = list()
        for i in range(0, 10):
            model.schedule.add(Human(unique_id=i, model=model))
            human_agent_id_list.append(i)

        expected_agent_id_list = human_agent_id_list

        result_agent_id_list = model.mobile_agents

        assert expected_agent_id_list == result_agent_id_list

    def test_method_step(self):

        model = SimulationModel()
        graph = NetworkxBipartiteGraph()
        model.graph = graph

        locale_agent_id_list = list()
        transport_agent_id_list = list()
        human_agent_id_list = list()
        for i in range(0, 10):
            model.schedule.add(Locale(unique_id=i, model=model))
            model.graph.add_node_to_component_zero(i)
            locale_agent_id_list.append(i)
        for i in range(10, 20):
            model.schedule.add(Transport(unique_id=i, model=model))
            model.graph.add_node_to_component_zero(i)
            transport_agent_id_list.append(i)
        for i in range(20, 30):
            model.schedule.add(Human(unique_id=i, model=model))
            model.graph.add_node_to_component_one(i)
            human_agent_id_list.append(i)

        expected_agent_id_list = (
            human_agent_id_list + locale_agent_id_list + transport_agent_id_list
        )

        model.step()

        assert (
            model.schedule.steps == 1
            and list(model.schedule._agents.keys()) == sorted(expected_agent_id_list)
            and model.is_activation_order_configured is True
        )

    def test_method_step_with_nodes_association(self):

        model = SimulationModel()
        graph = NetworkxBipartiteGraph()
        model.graph = graph

        locale_agent_id_list = list()
        transport_agent_id_list = list()
        human_agent_id_list = list()
        for i in range(0, 10):
            model.schedule.add(Locale(unique_id=i, model=model))
            model.graph.add_node_to_component_zero(i)
            locale_agent_id_list.append(i)
        for i in range(10, 20):
            model.schedule.add(Transport(unique_id=i, model=model))
            model.graph.add_node_to_component_zero(i)
            transport_agent_id_list.append(i)
        for i in range(20, 30):
            model.schedule.add(Human(unique_id=i, model=model))
            model.graph.add_node_to_component_one(i)
            human_agent_id_list.append(i)

        locale_occupants = dict()
        transport_occupants = dict()

        for j in range(2):
            model.step()
            locale_occupants[j] = list()
            transport_occupants[j] = list()

            for i in range(0, 10):
                occupants = model.schedule._agents[i].occupants
                locale_occupants[j].extend(occupants) if len(occupants) > 0 else None
                print(f"Locale {i} has: {occupants}")
            for i in range(10, 20):
                occupants = model.schedule._agents[i].occupants
                transport_occupants[j].extend(occupants) if len(occupants) > 0 else None
                print(f"Transport {i} has: {occupants}")
            for i in range(20, 30):
                mobile_agent = model.schedule._agents[i]
                mobile_agent.change_position(i - 10 * (j + 1))
                print(
                    f"Human {i} position is: {mobile_agent.position}; "
                    f"and last positions was {mobile_agent.get_last_positions()}"
                )

        model.step()
        locale_occupants[2] = list()
        transport_occupants[2] = list()
        for i in range(0, 10):
            occupants = model.schedule._agents[i].occupants
            locale_occupants[2].extend(occupants) if len(occupants) > 0 else None
            print(f"Locale {i} has: {occupants}")
        for i in range(10, 20):
            occupants = model.schedule._agents[i].occupants
            transport_occupants[2].extend(occupants) if len(occupants) > 0 else None
            print(f"Transport {i} has: {occupants}")

        assert (
            locale_occupants[0] == []
            and transport_occupants[0] == []
            and locale_occupants[1] == []
            and transport_occupants[1] == human_agent_id_list
            and locale_occupants[2] == human_agent_id_list
            and transport_occupants[2] == []
        )
