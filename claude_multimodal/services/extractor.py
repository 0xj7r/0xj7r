import logging
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()



class AssetExtraction:
    """
    Base class to generate summaries of assets using OpenAI's GPT-4 Vision model.

    :attribute client (OpenAI): An instance of the OpenAI client.
    :attribute session (requests.Session): A session object for making HTTP requests.
    """

    def __init__(self):
        """
        Initialize the ImageSummaryGenerator with an OpenAI client and a requests session.
        """
        self.client = OpenAI()
        self.session = requests.Session()

    def generate_summary(self):
        """Placeholder method implemented in sub-classes."""
        raise NotImplementedError(
            f"generate_summary method not implemented in {self.__class__.__name__}. "
            f"Subclasses of AssetExtraction must implement generate_summary method."
        )

    def _parse_response(self, response: Dict) -> Dict:
        """Parses model output response to conform to Pydantic class."""
        return self.pydantic_parser.parse(response.choices[0].message.content)

    def _return_tokens(self, response: Dict) -> Dict:
        """Estimates inference cost assuming gpt-4 (4K context)."""
        i_tokens = response.usage.prompt_tokens
        o_tokens = response.usage.completion_tokens

        i_cost = (i_tokens / 1000) * 0.001
        o_cost = (o_tokens / 1000) * 0.003

        # TODO: add image scaling token costs
        return {
            "prompt_tokens": i_tokens,
            "completion_tokens": o_tokens,
            "estimated_io_cost": f"${round(i_cost + o_cost, 5)}",
        }

    def _run(self, url: str) -> Dict:
        """Executes main text extraction methods."""
        logger.info(f"Processing asset {url}")
        response = self.generate_summary(url)
        if response is not None:
            try:
                json_output = dict(self._parse_response(response))
                return json_output
            except Exception as e:
                logger.error(
                    f"Error processing response for asset {url}: {e}", exc_info=True
                )
        else:
            logger.error(f"Failed to generate summary for asset {url}")
        return {}