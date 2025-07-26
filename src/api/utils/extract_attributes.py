from logger import logger

def extract_attributes(pydantic_model, attributes):
    """Function for seperating attributes from pydantic_model
    args:   pydantic_model [json]
            attributes [list[str]] (attributes selected for seperation)
    return: pydantic_model, extracted_attributes
    """
    pm_json = pydantic_model.model_dump()
    extracted_attributes = [] 

    for attribute in attributes:
        extracted_attribut = pm_json.get(f"{attribute}", "")
        logger.debug(f"extracted_attribut: {extracted_attribut}")
        extracted_attributes.append(extracted_attribut)

        pydantic_model = {key : value for key, value in pm_json.items() if key != f"{attribute}"}
        logger.debug(f"pydantic_model after extraction of attributes: {pydantic_model}")

    return pydantic_model, extracted_attributes