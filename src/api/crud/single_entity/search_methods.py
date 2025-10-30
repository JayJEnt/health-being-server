from logger import logger
from database.supabase_connection import supabase_connection
from api.handlers.http_exceptions import ResourceNotFound
from api.crud.utils import restrict_data, get_main_config
from api.filters.base_filter import filter_followed_authors, filter_ingredients


async def search_elements(
    element_type: str,
    phrase: str,
    filters: dict = {},
    requesting_user_id: int = None,
    restrict: bool = False,
) -> list:
    """
    Search a record in element table by given phrase.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        phrase (str): The searching phrase.
        filters (dict): Filters which are used while searching phrase.
        restrict (bool): The optional argument, that allows to drop some of the attributes.

    Returns:
        dict: List of found element item responses data from database.
    """
    config = get_main_config(element_type)
    found_elements = []

    for search_column in config.get("search_columns", []):
        actual_founds = []
        try:
            actual_founds = supabase_connection.find_ilike(
                config.get("table"), search_column, phrase
            )
        except ResourceNotFound:
            logger.info(
                f"{element_type} with phrase={phrase} not found in column={search_column}"
            )

        if actual_founds:
            for actual_found in actual_founds:
                duplicated = False
                for found_element in found_elements:
                    if found_element.get("id") == actual_found.get("id"):
                        duplicated = True
                        break
                if not duplicated:
                    found_elements.append(actual_found)

    if not found_elements:
        raise ResourceNotFound

    if filters and requesting_user_id:
        found_elements = await filter_out_recipes(
            found_elements, filters, requesting_user_id
        )

    if restrict:
        found_elements = restrict_data(element_type, found_elements)

    return found_elements


async def filter_out_recipes(
    recipes: list[dict], filters: dict, requesting_user_id: int
) -> list[dict]:
    if filters.get("allergies_off"):
        recipes = await filter_ingredients(recipes, requesting_user_id)
    if filters.get("liked_and_favourite_ingredients"):
        pass
    if filters.get("only_favourite_ingredients"):
        pass
    if filters.get("only_favourite_diets"):
        pass
    if filters.get("only_followed_authors"):
        recipes = await filter_followed_authors(recipes, requesting_user_id)
    if filters.get("only_owned_ingredients"):
        pass

    return recipes
