from api.crud.single_entity.post_methods import create_element
from api.crud.relation.post_methods import create_relationships
from api.crud.nested.post_methods import create_nested
from api.crud.utils import pop_attributes, add_attributes


async def create_all(
    element_type: str,
    element_data: dict,
    related_attributes: list = [],
    nested_attributes: list = [],
) -> dict:
    """
    Create all (entity, relationships, nested) data for an element by its id and specified related and nested attributes, which are required.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_attributes (list, optional): List of related attributes to include. Defaults to [].
        nested_attributes (list, optional): List of nested attributes to include. Defaults to [].

    Returns:
        dict: Relationship item data.
    """
    element_data, related_data = pop_attributes(element_data, related_attributes)
    element_data, nested_data = pop_attributes(element_data, nested_attributes)

    element_data = await create_element(element_type, element_data)
    attributes_to_add = await create_relationships(
        element_type, element_data["id"], related_data
    )
    attributes_to_add += await create_nested(
        element_type, element_data["id"], nested_data
    )

    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
