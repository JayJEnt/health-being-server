from api.crud.utils import pop_attributes, add_attributes
from api.crud.single_entity.put_methods import update_element_by_id
from api.crud.nested.put_methods import update_nested
from api.crud.relation.put_methods import update_relationships


async def update_all(
    element_type: str,
    element_id: int,
    element_data: dict,
    related_attributes: list = [],
    nested_attributes: list = [],
) -> dict:
    """
    Update all (entity, relationships, nested) data for an element by its id and specified related and nested attributes, which are required.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_attributes (list, optional): List of related attributes to include. Defaults to [].
        nested_attributes (list, optional): List of nested attributes to include. Defaults to [].

    Returns:
        dict: Relationship item data.
    """
    element_data, related_elements_list = pop_attributes(
        element_data, related_attributes
    )
    element_data, nested_data = pop_attributes(element_data, nested_attributes)

    element_data = await update_element_by_id(element_type, element_id, element_data)
    attributes_to_add = await update_relationships(
        element_type, element_id, related_elements_list
    )
    attributes_to_add += await update_nested(element_type, element_id, nested_data)

    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
