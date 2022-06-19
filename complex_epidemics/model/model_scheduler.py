from mesa import Model
from mesa.time import SimultaneousActivation

from complex_epidemics.utils.step_utils import StepUtils


class ModelScheduler(SimultaneousActivation):
    def __init__(self, model: Model):
        super().__init__(model=model)
        self._activation_order = dict
        self._activation_order: dict[int, list[int]] = dict()

    def add_agent_to_activation_order(self, agent_list: list[int], order: int) -> None:
        if order not in self._activation_order.keys():
            self._activation_order[order] = []
        self._activation_order[order].extend(agent_list)

    def step(self) -> None:
        """Step all agents, then advance them."""
        order_list_length = len(self._activation_order.keys())
        for i in range(order_list_length):
            agent_keys = self._activation_order[i]
            for agent_key in agent_keys:
                self._agents[agent_key].step()
            for agent_key in agent_keys:
                agent = self._agents[agent_key]
                if StepUtils.has_advance_method(__obj=agent, remove_protected=True):
                    self._agents[agent_key].advance()
            self.steps += 1
            self.time += 1
