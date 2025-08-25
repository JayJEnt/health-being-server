from api.crud.many_entities.delete_methods import delete_all
from api.crud.many_entities.get_methods import get_all
from api.crud.many_entities.post_methods import create_all
from api.crud.many_entities.put_methods import update_all

from api.crud.relation.delete_methods import delete_relationship, delete_relationships
from api.crud.relation.get_methods import get_relationships, get_relationship
from api.crud.relation.post_methods import create_relationship

from api.crud.single_entity.delete_methods import delete_element_by_id
from api.crud.single_entity.get_methods import get_elements, get_element_by_id, get_element_by_name
from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.put_methods import update_element_by_id
from api.crud.single_entity.search_methods import search_elements


# TODO: FIX DOCS
class CrudOperations():
    def __init__(self, element_type: str):
        self.element_type = element_type

    """Entities with all relationed entities"""
    def get_all(
        self,
        element_id: int,
        related_attributes: list = [],
        nested_attributes: list = [],
    ) -> dict:
        return get_all(self.element_type, element_id, related_attributes, nested_attributes)
    
    def post_all(
        self,
        element_data: dict,
        related_attributes: list = [],
        nested_attributes: list = [],
    ) -> dict:
        return create_all(self.element_type, element_data, related_attributes, nested_attributes)
    
    def put_all(
        self,
        element_id: int,
        element_data: dict,
        related_attributes: list = [],
        nested_attributes: list = [],
    ) -> dict:
        return update_all(self.element_type, element_id, element_data, related_attributes, nested_attributes)
    
    def delete_all(
        self,
        element_id: int,
        related_attributes: list = [],
        nested_attributes: list = [],
    ) -> dict:
        return delete_all(self.element_type, element_id, related_attributes, nested_attributes)

    """Relations"""
    def get_relationship(
        self,
        element_id: int,
        relation_name: str,
        relation_id: int
    ) -> dict:
        return get_relationship(self.element_type, element_id, relation_name, relation_id)
        
    def get_relationships(
        self,
        relation_name: str,
        relation_id: int,
    ) -> list:
        return get_relationships(self.element_type, relation_name, relation_id)

    def post_relationship(
        self,
        element_id: int,
        relation_name: str,
        related_data: dict
    ) -> dict:
        return create_relationship(self.element_type, element_id, relation_name, related_data)
        
    def delete_relationship(
        self,
        element_id: int,
        relation_name: str,
        relation_id: int
    ) -> dict:
        return delete_relationship(self.element_type, element_id, relation_name, relation_id)
    
    def delete_relationships(
        self,
        element_id: int,
        relation_name: str,
    ) -> dict:
        return delete_relationships(self.element_type, element_id, relation_name)

    """Just entity"""

    def get(
        self,
        restrict: bool=False
    ) -> list:
        return get_elements(self.element_type, restrict)
    
    def get_by_name(
        self,
        element_name: str,
        alternative_name: bool=False
    ) -> dict:
        return get_element_by_name(self.element_type, element_name, alternative_name)
    
    def get_by_id(
        self,
        element_id: int,
    ) -> dict:
        return get_element_by_id(self.element_type, element_id)
    
    def post(
        self,
        element_data: dict
    ) -> dict:
        return create_element(self.element_type, element_data)
    
    def put(
        self,
        element_id: int,
        element_data: dict,
    ) -> dict:
        return update_element_by_id(self.element_type, element_id, element_data)
    
    def delete(
        self,
        element_id: int,
    ) -> dict:
        return delete_element_by_id(self.element_type, element_id)
    
    def search(
        self,
        phrase: str,
        restrict: bool=False,
    ) -> list:
        return search_elements(self.element_type, phrase, restrict)