from mesa import Model
from mesa.time import SimultaneousActivation

from complex_epidemics.utils.step_utils import StepUtils


class ModelScheduler(SimultaneousActivation):

    __slots__ = ["_activation_order"]

    def __init__(self, model: Model):
        super().__init__(model=model)
        self._activation_order: dict[int, list[int]] = dict()

    @property
    def activation_order(self):
        return self._activation_order

    def add_agent_to_activation_order(
        self, agent_id_list: list[int], order: int
    ) -> None:
        if order not in self._activation_order.keys():
            self._activation_order[order] = []
        self._activation_order[order].extend(agent_id_list)

    def step(self) -> None:
        """Step all agents, then advance them."""
        order_list_length = len(self.activation_order.keys())
        for i in range(order_list_length):
            agent_keys = self.activation_order[i]
            for agent_key in agent_keys:
                self._agents[agent_key].step()
            for agent_key in agent_keys:
                agent = self._agents[agent_key]
                if StepUtils.has_advance_method(agent, remove_protected=True):
                    self._agents[agent_key].advance()
        self.steps += 1
        self.time += 1
