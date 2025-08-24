from api.crud.utils import pop_attributes, add_attributes
from api.crud.single_entity.put_methods import update_element_by_id
from api.crud.nested.put_methods import update_nested
from api.crud.relation.put_methods import update_relationships


# TODO: FIX DOCS
async def update_all(
    element_type: str,
    element_id: int,
    element_data: dict,
    related_attributes: list = [],
    nested_attributes: list = [],
) -> dict:
    """Update a record in all picked relations and main table."""
    element_data, related_elements_list = pop_attributes(element_data, related_attributes)
    element_data, nested_data = pop_attributes(element_data, nested_attributes)
    
    element_data = await update_element_by_id(element_type, element_id, element_data)
    attributes_to_add = await update_relationships(element_type, element_id, related_elements_list)
    attributes_to_add += await update_nested(element_type, element_id, nested_data)

    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
