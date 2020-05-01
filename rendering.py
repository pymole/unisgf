from collection import Collection


class Renderer:
    # TODO add typing for path-like objects
    def render_file(self, path: str, collection: Collection):
        rendered_string = self.render_string(collection)

        with open(path, 'w') as f:
            f.write(rendered_string)

    def render_string(self, collection: Collection) -> str:
        if not isinstance(collection, Collection):
            raise TypeError("Pass <Collection> instead of " + str(type(collection)))

        rendered_string = ''

        for game_tree in collection:
            rendered_string += '('

            to_check = [game_tree.get_root()]

            while to_check:
                cur_node = to_check.pop()

                # open group if parent has multiple children
                if cur_node.parent is not None and len(cur_node.parent.children) > 1:
                    rendered_string += '('

                rendered_node = ';'
                for property in cur_node.properties:
                    if not property.values:
                        raise ValueError(f'Property {property.identifier} must have a value')

                    rendered_values = '[' + ']['.join(value.render() for value in property.values) + ']'

                    rendered_property = property.identifier + rendered_values
                    rendered_node += rendered_property

                rendered_string += rendered_node

                # exit group if it is the last node has no children
                if len(cur_node.children) == 0:
                    rendered_string += ')'

                to_check += reversed(cur_node.children)

            rendered_string += ')'

        return rendered_string