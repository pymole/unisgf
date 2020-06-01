from __future__ import annotations
from unisgf.property import Property
from unisgf.exceptions import NodeAlreadyHasAProperty
from typing import Iterable, Optional


# TODO __iadd__
class Node:
    def __init__(self, parent):
        self.parent = parent

        self.__properties = {}
        self.children = []

    def __contains__(self, property_identifier: str):
        return self.has_property(property_identifier)

    def __getitem__(self, property_identifier: str):
        return self.__properties[property_identifier]

    def __setitem__(self, property_identifier: str, values: Iterable):
        self.create_property(property_identifier, values)

    def create_property(self, property_identifier: str, values: Optional[Iterable] = None) -> Property:
        if self.has_property(property_identifier):
            raise KeyError(f"Property with identifier '{property_identifier}' already exists.")

        property = Property(property_identifier, values)
        self.__properties[property_identifier] = property
        return property

    def create_child(self) -> Node:
        child = Node(self)
        self.children.append(child)
        return child

    def has_property(self, property_identifier: str):
        return property_identifier in self.__properties

    @property
    def properties(self):
        return self.__properties.values()


class RootNode(Node):
    def __init__(self):
        super().__init__(None)
