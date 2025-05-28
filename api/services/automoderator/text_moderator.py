from api.services.automoderator.base import BaseAutomoderator
from api.services.automoderator.prompts import VALIDATE_DESCRIPTION_PROMPT
from pydantic import BaseModel, Field


class TextModerator(BaseAutomoderator):
    
    PROMPT = VALIDATE_DESCRIPTION_PROMPT

    class ResponseModel(BaseModel):
        is_valid: bool = Field(
            default="Something went wrong",
            description="Indicates whether the recipe text is valid according to the moderation rules."
        )