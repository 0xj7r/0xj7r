import os 
import logging 
import uuid
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

class Workflow:
    """
    Base class for Workflows object.
    """
    
    def __init__(self, client):
        self.client = client # This is the client object that is used to interact with the API e.g. OpenAI API
        self.id = uuid.uuid4()
    
    def step(self, input):
        """
        A single step of the workflow.
        """
        # Define step args
        raise NotImplementedError("Subclasses must implement this method")
    
    def _run(self, input):
        """
        Run the workflow.
        """
        try:
            logging.info(f"Running workflow {self.__class__.__name__}")
        except Exception as e:
            logging.error(f"Error running workflow {self.__class__.__name__}: {e}")
            return None
        raise NotImplementedError("Subclasses must implement this method")
        