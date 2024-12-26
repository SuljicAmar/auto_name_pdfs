from ollama import generate
from pydantic import BaseModel
from typing import List, Optional


class ModelResponse(BaseModel):
    title: str
    authors: Optional[List[str]]


class ModelWrapper:
    def __init__(self):
        self.model = "gemma2:2b"
        self.options = {"temperature": 0.7, "num_ctx": 15000}
        self.format = ModelResponse.model_json_schema()
        self.system_prompt = """I have books and research papers saved as untitled PDFs. I will provide a snippet of content
    from the PDF and it is your job to extract the title of the book and/or research paper alongside its authors. 
    The content is provided below: \n"""

    def run(self, content):
        return generate(
            model=self.model,
            system=self.system_prompt,
            prompt=content,
            options=self.options,
            format=self.format,
        ).response
