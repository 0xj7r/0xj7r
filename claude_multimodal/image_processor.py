import logging
from typing import Optional
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from models.image_properties import ImageProperties
from services.extractor import AssetExtraction
from tenacity import retry, stop_after_attempt, wait_random_exponential
from utils.prompts import image_summary_assistant_prompt
from pydantic.error_wrappers import ValidationError
from requests.exceptions import HTTPError


class ImageExtraction(AssetExtraction):
    """
    Class to generate summaries of images using OpenAI's GPT-4 Vision model.
    """

    def __init__(self):
        """
        Initialize the ImageSummaryGenerator with an OpenAI client and a requests session.
        """
        super().__init__()
        self.pydantic_parser = PydanticOutputParser(pydantic_object=ImageProperties)

    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def generate_summary(self, url: str) -> Optional[str]:
        """
        Process a single image URL and return its summary. This method is rate-limited.

        :param url: Image URL to process.
        :return: Summary of the image or None on error.
        """

        # Initialise pydantic output parser
        prompt = PromptTemplate.from_template(
            template=image_summary_assistant_prompt
            + """
              \n{format_instructions}\n
              """
            + "Please output your response in the demanded JSON format.",
        ).format(format_instructions=self.pydantic_parser.get_format_instructions())
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What is in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {"url": url, "detail": "high"},
                            },
                        ],
                    },
                ],
                temperature=0,
                max_tokens=4000,
            )
            return response
        except OutputParserException as e:
            logger.warning(f"JSON output could not be parsed: {e}", exc_info=True)
            return None
        except (HTTPError, ValidationError) as e:
            logger.error(f"Error in processing image {url}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return None