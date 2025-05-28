from api.services.automoderator.recipe_text_moderator import RecipeTextModerator


class AutoModeratorService:
    """
    Service to invoke the AutoModerator.
    """

    def __init__(
        self,
        llm=None,
        recipe_text_moderator=RecipeTextModerator
    ):
        self._llm = llm
        self.recipe_text_moderator = recipe_text_moderator(llm=self._llm)

    def validate_text(self, title: str, description: str, steps: list):
        return self.recipe_text_moderator.invoke(
            title=title,
            description=description,
            steps=steps
        )
