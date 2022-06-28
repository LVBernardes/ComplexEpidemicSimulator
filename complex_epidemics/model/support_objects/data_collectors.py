from typing import Any


class ModelCollectors:

    @staticmethod
    def collect_model_clock(model: Any) -> str:
        return model.clock.get_datetime_formated()

    @staticmethod
    def collect_susceptible_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if host.is_alive and host.health.is_susceptible:
                population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_incubated_no_symptoms_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if host.is_alive and not host.health.is_susceptible:
                for disease_instance in host.health.diseases:
                    if (
                        disease_instance.active
                        and disease_instance.state.__class__.__name__
                        == "IncubatedNoSymptoms"
                    ):
                        population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_infectious_no_symptoms_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if host.is_alive and host.health.is_infectious:
                for disease_instance in host.health.diseases:
                    if (
                        disease_instance.active
                        and disease_instance.state.__class__.__name__
                        == "InfectiousNoSymptoms"
                    ):
                        population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_infectious_mild_moderated_symptoms_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if host.is_alive and host.health.is_infectious:
                for disease_instance in host.health.diseases:
                    if (
                        disease_instance.active
                        and disease_instance.state.__class__.__name__
                        == "InfectiousMildModerateSymptoms"
                    ):
                        population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_infectious_severe_symptoms_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if host.is_alive and host.health.is_infectious:
                for disease_instance in host.health.diseases:
                    if (
                        disease_instance.active
                        and disease_instance.state.__class__.__name__
                        == "InfectiousSevereSymptoms"
                    ):
                        population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_infectious_critical_symptoms_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if host.is_alive and host.health.is_infectious:
                for disease_instance in host.health.diseases:
                    if (
                        disease_instance.active
                        and disease_instance.state.__class__.__name__
                        == "InfectiousCriticalSymptoms"
                    ):
                        population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_recovered_immune_population(model: Any):
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if (
                host.is_alive
                and not host.health.is_susceptible
                and not host.health.is_infectious
            ):
                for immunity_instance in host.health.immunity:
                    if immunity_instance.active:
                        population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_deceased_population(model: Any) -> int:
        population_list = list()
        for host_id in model.mobile_agents:
            host = model.get_agent_by_id(host_id)
            if not host.is_alive:
                population_list.append(host_id)
        return len(population_list)

    @staticmethod
    def collect_patients_occupancy(model: Any) -> int:
        total_occupancy = 0
        for item_id in model.get_agents_by_class('HealthCareUnit'):
            item = model.get_agent_by_id(item_id)
            total_occupancy += len(item.all_patients)
        return total_occupancy
