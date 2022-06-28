import inspect
import logging
from typing import Any, Union

LOG = logging.getLogger(__name__)


class StepUtils:
    @staticmethod
    def has_step_method(__obj, remove_protected: bool = False):
        if "step" in set(
            StepUtils.clean_attributes(dir(__obj), remove_protected=remove_protected)
        ):
            return True
        else:
            return False

    @staticmethod
    def has_advance_method(__obj, remove_protected: bool = False):
        if "advance" in set(
            StepUtils.clean_attributes(dir(__obj), remove_protected=remove_protected)
        ):
            return True
        else:
            return False

    @staticmethod
    def remove_dunder_methods(__obj: Union[list, set]) -> list:
        return [method for method in __obj if method.endswith("__") is False]

    @staticmethod
    def remove_protected_attributes(__obj: Union[list, set]) -> list:
        return [method for method in __obj if method.startswith("_") is False]

    @staticmethod
    def clean_attributes(
        __obj: Union[list, set], remove_dunder: bool = True, remove_protected: bool = False
    ) -> Union[list, None]:
        if remove_dunder and remove_protected:
            return StepUtils.remove_protected_attributes(
                StepUtils.remove_protected_attributes(__obj)
            )
        elif remove_dunder and not remove_protected:
            return StepUtils.remove_protected_attributes(__obj)
        elif not remove_dunder and remove_protected:
            return StepUtils.remove_protected_attributes(__obj)
        else:
            return None

    @staticmethod
    def get_elements_with_step_method(
        __obj: Any, ref: str, remove_protected: bool = False, recursion_count: int = 0
    ) -> list:
        elements = list()
        max_recursion_count = 2
        if recursion_count > max_recursion_count:
            return elements

        outer_element_name = ref
        outer_element_object = __obj
        outer_element_object_class_name = __obj.__class__.__name__
        outer_element_parent_class_set = {
            _class.__name__ for _class in outer_element_object.__class__.__mro__
        }

        LOG.debug(
            f'Exploring object: "{outer_element_name}" from class '
            f'"{outer_element_object_class_name}".'
        )

        blocked_list = {
            "Model",
            "MockModel",
            "SimulationModel",
            "MockAgent",
            "Agent",
            "int",
            "int8",
            "int16",
            "int32",
            "int64",
            "uint8",
            "uint16",
            "uint32",
            "uint64",
            "float_",
            "float16",
            "float32",
            "float64",
            "complex_",
            "complex64",
            "str",
            "NoneType",
            "method",
            "float",
            "iter",
            "set",
            "list",
            "complex",
            "bool",
            "dict",
            "tuple",
        }

        intersection = outer_element_parent_class_set.intersection(blocked_list)

        if (
            StepUtils.has_step_method(
                outer_element_object, remove_protected=remove_protected
            )
            and outer_element_object_class_name not in blocked_list
            and not intersection
        ):
            elements.append(outer_element_name)
            LOG.debug(f'Found a step for object "{outer_element_name}".')

        for inner_element_name in StepUtils.clean_attributes(
            dir(outer_element_object), remove_protected=remove_protected
        ):

            inner_element_object = getattr(__obj, inner_element_name)
            inner_element_object_class_name = inner_element_object.__class__.__name__

            if (
                inner_element_object_class_name not in blocked_list
                and not inspect.isbuiltin(inner_element_object)
            ):
                inner_elements = StepUtils.get_elements_with_step_method(
                    inner_element_object,
                    inner_element_name,
                    remove_protected=remove_protected,
                    recursion_count=(recursion_count + 1)
                )
                for inner in inner_elements:
                    if inner is not None or inner != []:
                        elements.append(f"{outer_element_name}.{inner}")

        LOG.debug(f'Returning elements {elements} from object "{outer_element_name}".')
        return elements
