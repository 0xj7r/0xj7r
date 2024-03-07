import logging
from typing import Any
from image_processor import ImageExtraction

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def handler(url: str) -> Any:
    """
    This function handles the process of image extraction and summary generation.

    Args:
        url (str): The URL of the image to be processed.

    Returns:
        Any: The summary of the processed image.
    """

    try:
        image_processor = ImageExtraction()
        summary = image_processor.generate_summary(url)
        print(summary.content[0].text)
        parsed_response = image_processor._parse_response(summary)
        return parsed_response
    except Exception as e:
        logging.error(f"Error in processing image url: {e}")


if __name__ == "__main__":
    image_url = "https://pbs.twimg.com/media/GHmyH3oXcAAmAM2?format=jpg"
    response = handler(image_url)
    print(response)
