from api.crud.nested.delete_methods import delete_nested
from api.crud.relation.delete_methods import delete_relationships
from api.crud.single_entity.delete_methods import delete_element_by_id


# TODO: FIX DOCS
async def delete_all(
    element_type: str,
    element_id: int,
    related_attributes: list = [],
    nested_attributes: list = [],
):
    """Function deletes a record in element table, relationship/join tables and nested tables"""
    await delete_relationships(element_type, element_id, related_attributes)
    await delete_nested(element_type, element_id, nested_attributes)

    element = await delete_element_by_id(element_type, element_id)

    return element
