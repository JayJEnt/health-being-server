from api.services.automoderator.text_moderator import TextModerator
from api.services.automoderator.image_moderator import ImageModerator
from transform_image import convert_to_base64
from PIL import Image


class AutoModeratorService:
    """
    Service to invoke the AutoModerator.
    """

    def __init__(
        self,
        llm=None,
        text_moderator=TextModerator,
        image_moderator=ImageModerator,
    ):
        self._llm = llm
        self.text_moderator = text_moderator(llm=self._llm)
        self.image_moderator = image_moderator(llm=self._llm)

    def validate_text(self, title: str, description: str, steps: list):
        return self.text_moderator.invoke(
            title=title,
            description=description,
            steps=steps
        )
        
    def _attach_image(self, image_path: str):
        pil_image = Image.open(image_path)
        image_b64 = convert_to_base64(pil_image)
        return image_b64
        
    def validate_image(self, image_path: str, title: str, description: str, steps: list):
        image_b64 = self._attach_image(image_path)
        
        image_description = self._llm.invoke("Descripe the image detailed. Focus on correct guessing dish/food name", images=[image_b64], model_kwargs={"temperature": 0})
        print("Image description:", image_description)
        
        return self.image_moderator.invoke_img(
            title=title,
            description=description,
            steps=steps,
            image_description=image_description
        )