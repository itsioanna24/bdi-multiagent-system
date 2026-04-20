import json
from core.bdi_agent import BDIAgent
from core.utils import log, handle_error

class StorageAgent(BDIAgent):
    """
    Stores processed data into JSON.
    WHY: Ensures traceable and reusable output.
    """
    def __init__(self, output_file="results.json"):
        # Initialise base BDI agent with name
        super().__init__("StorageAgent")

        # Define output file name
        self.output_file = output_file

        # Define intention (BDI concept)
        self.intention = None

    def perceive(self, env):
        # Retrieve processed data from environment
        self.data = env.get("processed_data")

        log("[StorageAgent] Retrieved processed data from environment")


    def deliberate(self):
        # Define goal of agent
        self.intention = "store_results"

        log(f"[StorageAgent] Intention set: {self.intention}")


    def act(self, env):
        try:
            # Check if there is data to store
            if not self.data:
                log("[StorageAgent] No data available to store")
                return

            # Attempt to write data to JSON file
            try:
                with open(self.output_file, "w", encoding="utf-8") as file:
                    # Convert Python data into JSON format
                    # indent improves readability for inspection
                    json.dump(self.data, file, indent=2)

                # Log success with number of records
                log(f"[StorageAgent] Successfully stored {len(self.data)} records in '{self.output_file}'")

            except IOError as e:
                # Handle file writing issues (permissions, disk issues, etc.)
                log(f"[StorageAgent] File writing error: {str(e)}")

        except Exception as e:
            # Catch unexpected errors to prevent system crash
            handle_error("StorageAgent", e)
