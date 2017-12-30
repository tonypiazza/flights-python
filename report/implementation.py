"""
    Proxy for switching between report implementations
"""

from enum import Enum
from functools import partial


class ImplementationSelector(object):
    """Wraps multiple report implementations and makes it easy to switch
       between them
    """

    current_impl = None
    __impls = {}
    report_group_subtitle = ""
    implementation_group_title = "Implementation"

    def __init__(self, *args):
        # if not isinstance(impls, tuple):
        #     raise ValueError('impls argument is wrong type:' + type(impls))
        for impl_enum, impl_value in args:
            if not isinstance(impl_enum, ImplementationType):
                raise ValueError("Invalid enum type:" + impl_enum)
            if self.current_impl is None:
                self.current_impl = impl_enum
                self.__set_implementation_group_title(impl_enum.name)
                self.__set_report_group_subtitle(impl_enum.name)
            self.__impls[impl_enum] = impl_value

    def __call__(self, *args, **kwargs):
        return self.__impls[self.current_impl]

    def use_impl(self, impl_enum):
        if impl_enum in self.__impls:
            self.current_impl = impl_enum
            self.__set_implementation_group_title(impl_enum.name)
            self.__set_report_group_subtitle(impl_enum.name)
        else:
            raise ValueError("Unknown enum: " + impl_enum)

    def get_implementation_group_title(self):
        return self.implementation_group_title

    def get_report_group_subtitle(self):
        return self.report_group_subtitle

    def __set_implementation_group_title(self, impl_name):
        self.implementation_group_title = \
            "Implementation (currently using {})".format(impl_name)

    def __set_report_group_subtitle(self, impl_name):
        self.report_group_subtitle = \
            "(using {} implementation)".format(impl_name)

    def get_implementation_menu_items(self):
        result = []
        for impl_enum, impl_value in self.__impls.items():
            result.append((impl_enum.name, partial(self.use_impl, impl_enum)))
        return result


class ImplementationType(Enum):
    """Enum that represents each possible type of implementation of reports"""
    Pandas = 1
    RxPY = 2
