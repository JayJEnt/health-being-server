from langchain_core.output_parsers import JsonOutputParser


class BaseAutomoderator:
    """Base class for automoderators."""

    def __init__(self, llm):
        self._llm = llm
        self._prompt = self.PROMPT
        self._output_parser = self._get_output_parser()
        self._chain = self._prompt | self._llm  #| self._output_parser
        
    def _get_output_parser(self):
        return JsonOutputParser(pydantic_object=self.ResponseModel)

    def invoke(self, title: str, description: str, steps: list) -> str:
        return self._chain.invoke({"title": title, "description": description, "steps": steps})
    
    def invoke_img(self, title: str, description: str, steps: list, image_description: str) -> str:
        return self._chain.invoke({"title": title, "description": description, "steps": steps, "image_description": image_description})