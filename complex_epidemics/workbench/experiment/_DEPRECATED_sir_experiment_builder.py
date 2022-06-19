# import enum
#
# from mesa import Model
# from mesa.time import RandomActivation
#
# from complex_epidemics.graph import GraphFactory
# from complex_epidemics.model import Clock, SimulationModelBuilder
# from complex_epidemics.workbench.experiment.abstract_experiment import (
#     AbstractExperiment,
# )
# from complex_epidemics.workbench.experiment.abstract_experiment_builder import (
#     IExperimentBuilder,
# )
# from complex_epidemics.workbench.experiment.experiment import Experiment
#
#
# class SIRExperimentBuilder(IExperimentBuilder):
#     def __init__(self):
#         self._experiment = None
#         self._model_recipe = None
#
#     def build(self) -> None:
#         self._experiment = Experiment()
#         self.setup_agents()
#         self.setup_model()
#         self.setup_runner()
#         self.setup_report()
#
#     def generate_recipe(self, model: Model):
#         recipe = self._model_recipe = enum.Enum(
#             "SIR",
#             {
#                 "clock": Clock(),
#                 "schedule": RandomActivation(model),
#                 "graph": GraphFactory.new_contact_graph(),
#             },
#         )
#         return recipe
#
#     def setup_model(self):
#         _model_builder = SimulationModelBuilder()
#         _recipe = self.generate_recipe(_model_builder._model)
#         for element in _recipe:
#             _model_builder.assemble_element(element)
#         _result_model = _model_builder.get_result()
#
#         if self._experiment is None:
#             self.create_experiment_skeleton()
#
#         setattr(self._experiment, "model", _result_model)
#
#     def setup_agents(self):
#         pass
#
#     def setup_runner(self):
#         pass
#
#     def setup_report(self):
#         pass
#
#     def get_result(self) -> AbstractExperiment:
#         experiment = self._experiment
#         self.reset()
#         return experiment
#
#     def create_experiment_skeleton(self) -> None:
#         self._experiment = Experiment()
#
#     def reset(self):
#         self._experiment = None
