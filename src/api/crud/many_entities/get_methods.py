import asyncio

from api.crud.nested.get_methods import get_nested
from api.crud.relation.get_methods import get_relationed_item
from api.crud.single_entity.get_methods import get_element_by_id
from api.crud.utils import add_attributes


async def get_all(
    element_type: str,
    element_id: int,
    related_attributes: list = [],
    nested_attributes: list = [],
) -> dict:
    """
    Get all (entity, relationships, nested) data for an element by its id and specified related and nested attributes.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_attributes (list, optional): List of related attributes to include. Defaults to [].
        nested_attributes (list, optional): List of nested attributes to include. Defaults to [].

    Returns:
        dict: Relationship item data.
    """
    element_data = await get_element_by_id(element_type, element_id)
    attributes_to_add = await asyncio.gather(*(get_relationed_item(element_type, element_id, relation_name) for relation_name in related_attributes))
    attributes_to_add += await get_nested(element_type, element_id, nested_attributes)

    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
