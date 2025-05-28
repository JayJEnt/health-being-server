from api.services.automoderator.base import BaseAutomoderator
from api.services.automoderator.prompts import GENERATE_DESCRIPTION_PROMPT
from pydantic import BaseModel, Field


class RecipeTextModerator(BaseAutomoderator):
    """Automoderator for recipe text."""
    
    PROMPT = GENERATE_DESCRIPTION_PROMPT

    class ResponseModel(BaseModel):
        """Response model for recipe text moderation."""
        is_valid: bool = Field(
            default=False,
            description="Indicates whether the recipe text is valid according to the moderation rules."
        )