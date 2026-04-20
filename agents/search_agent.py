import requests, time
from core.bdi_agent import BDIAgent
from core.utils import log, handle_error

class SearchAgent(BDIAgent):
    """
    Retrieves academic data from ArXiv API.
    """

    def __init__(self, query):
        # Initialise base BDI agent with name
        super().__init__("SearchAgent")

        # Store the search query provided by the user/system
        self.query = query

        # Initialise variable to store API results
        self.results = None

        # Define intention (BDI concept)
        self.intention = None


    def perceive(self, env):
        # Log preparation step before making API request
        log("[SearchAgent] Preparing API request...")


    def deliberate(self):
        # Define intention based on goal
        self.intention = "retrieve_data"
        log(f"[SearchAgent] Intention set: {self.intention}")

        # Construct the ArXiv API URL using the query
        self.url = f"http://export.arxiv.org/api/query?search_query=all:{self.query}&start=0&max_results=5"
       


    def act(self, env):
        try:
            time.sleep(3)
            # Send HTTP GET request with timeout
            # WHY: Prevents system from hanging if API is slow/unresponsive
            response = requests.get(self.url, timeout=10)

            # Check if the response status is successful
            if response.status_code == 200:
                log("[SearchAgent] API response received successfully")

                # Check if response content is not empty
                if response.text:
                    # Store raw XML response
                    self.results = response.text

                    # Log successful retrieval with size info
                    log(f"[SearchAgent] Retrieved data")
                else:
                    # Handle empty response case
                    log("[SearchAgent] Warning: Empty response received")
                    self.results = None

            else:
                # Handle non-success HTTP status codes
                log(f"[SearchAgent] API returned status code: {response.status_code}")
                self.results = None

        except requests.exceptions.Timeout:
            # Handle timeout errors specifically
            log("[SearchAgent] Request timed out")
            self.results = None

        except requests.exceptions.ConnectionError:
            # Handle network connection issues
            log("[SearchAgent] Connection error occurred")
            self.results = None

        except Exception as e:
            # Handle any unexpected errors
            handle_error("SearchAgent", e)
            self.results = None
    
        # Store retrieved data into shared environment
        # Enables other agents to access and process this data
        env.update("raw_data", self.results)

        # Log storage step for traceability
        log("[SearchAgent] Raw data stored in environment")