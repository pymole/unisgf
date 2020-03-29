from __future__ import annotations
from exceptions import NodeAlreadyHasAProperty
from property import Property
from typing import Iterable, Optional


class Node:
    def __init__(self, parent):
        self.parent = parent

        self.properties = []
        self.children = []

    def add_property(self, property: Property):
        if self.has_property(property.identifier):
            raise NodeAlreadyHasAProperty(property)

        self.properties.append(property)

    def create_property(self, property_identifier: str, values: Optional[Iterable] = None) -> Property:
        property = Property(property_identifier, values)
        self.add_property(property)
        return property

    def create_child(self) -> Node:
        child = Node(self)
        self.children.append(child)

        return child

    def has_property(self, property_identifier: str):
        for property in self.properties:
            if property.identifier == property_identifier:
                return True

        return False


class RootNode(Node):
    def __init__(self):
        super().__init__(None)
