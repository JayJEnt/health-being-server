from api.crud.relation.delete_methods import delete_relationships
from api.crud.single_entity.delete_methods import delete_element_by_id


async def delete_all(
    element_type: str,
    element_id: int,
    related_attributes: list = [],
) -> dict:
    """
    Delete all (entity, relationships) data for an element by its id and specified related attributes, that are attached.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_attributes (list, optional): List of related attributes to include. Defaults to [].

    Returns:
        dict: Relationship item data.
    """
    await delete_relationships(element_type, element_id, related_attributes)

    element = await delete_element_by_id(element_type, element_id)

    return element
