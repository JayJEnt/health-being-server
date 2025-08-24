from api.crud.single_entity.post_methods import create_element
from api.crud.relation.post_methods import create_relationships
from api.crud.nested.post_methods import create_nested
from api.crud.utils import pop_attributes, add_attributes


# TODO: FIX DOCS
async def create_all(
    element_type: str,
    element_data: dict,
    related_attributes: list = [],
    nested_attributes: list = [],
) -> dict:
    """Creates a record in all picked relations and main table."""
    element_data, related_data = pop_attributes(element_data, related_attributes)
    element_data, nested_data = pop_attributes(element_data, nested_attributes)

    element_data = await create_element(element_type, element_data)
    attributes_to_add = await create_relationships(element_type, element_data["id"], related_data)
    attributes_to_add += await create_nested(element_type, element_data["id"], nested_data)
    
    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
