from langchain.prompts import StringPromptTemplate
from typing import List

class CustomPromptTemplate(StringPromptTemplate):
    template: str  # Define as class attribute
    input_variables: List[str]  # Define as class attribute

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)
