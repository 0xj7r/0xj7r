import anthropic
import logging
import requests
import base64
import httpx

from typing import Optional, Any
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
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class ImageExtraction(AssetExtraction):
    """
    Class to generate summaries of images using OpenAI's GPT-4 Vision model.
    """

    def __init__(self):
        """
        Initialize the ImageSummaryGenerator with an OpenAI client and a requests session.
        """
        super().__init__()
        self.client = anthropic.Anthropic()
        self.llm = "claude-3-sonnet-20240229"
        self.pydantic_parser = PydanticOutputParser(pydantic_object=ImageProperties)

    def _url_to_base64(self, image_url: str) -> Optional[Any]:
        """Fetch an image from a URL and convert it to a base64 string.

        Args:
            image_url (str): URL of the image to fetch.

        Returns:
            Optional[Any]: Base64 string of the image or None on error.
        """
        try:
            img_base64_string = base64.b64encode(httpx.get(image_url).content).decode(
                "utf-8"
            )
            return img_base64_string
        except Exception as e:
            logging.error("An error occurred:", e)
            return None

    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def generate_summary(self, url: str) -> Optional[str]:
        """
        Generate a summary of the image at the given URL.

        Args:
            url (str): URL of the image to summarize.
        Returns:
            Optional[str]: Summary of the image or None on error.
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
            img_base64 = self._url_to_base64(url)
            response = self.client.messages.create(
                model=self.llm,
                system=prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": img_base64,
                                },
                            },
                            {"type": "text", "text": "What is in this image?"},
                        ],
                    }
                ],
                max_tokens=4000,
                temperature=0,
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
