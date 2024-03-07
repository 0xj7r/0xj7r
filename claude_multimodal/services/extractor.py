import logging
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

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
        self.session = requests.Session()

    def generate_summary(self):
        """Placeholder method implemented in sub-classes."""
        raise NotImplementedError(
            f"generate_summary method not implemented in {self.__class__.__name__}. "
            f"Subclasses of AssetExtraction must implement generate_summary method."
        )

    def _parse_response(self, response: Dict) -> Dict:
        """Parses model output response to conform to Pydantic class."""
        return self.pydantic_parser.parse(response.content[0])   

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