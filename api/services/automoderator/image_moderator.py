from api.services.automoderator.base import BaseAutomoderator
from api.services.automoderator.prompts import VALIDATE_IMAGE_PROMPT
from pydantic import BaseModel, Field


class ImageModerator(BaseAutomoderator):
    
    PROMPT = VALIDATE_IMAGE_PROMPT

    class ResponseModel(BaseModel):
        is_valid: bool = Field(
            default="Something went wrong",
            description="Indicates whether the recipe image is valid according to the moderation rules."
        )