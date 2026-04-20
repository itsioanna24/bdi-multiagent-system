from core.environment import Environment
from agents.search_agent import SearchAgent
from agents.extraction_agent import ExtractionAgent
from agents.processing_agent import ProcessingAgent
from agents.storage_agent import StorageAgent
from core.utils import log


def main():
    # Log start of system execution
    log("System execution started.\n")

    # Create shared environment instance
    env = Environment()

    # Ask user for query
    query = input("Enter a search term: ").strip()

    # Optional: default if empty
    if not query:
        query = "machine learning"
        print("No input provided. Using default query: machine learning")

    # Initialise agents in execution order
    agents = [
        SearchAgent(query),
        ExtractionAgent(),
        ProcessingAgent(query),
        StorageAgent()
    ]

    # Execute each agent sequentially
    for agent in agents:
        agent.run(env)

    # Log completion of system execution
    log("System execution completed.")
    

# Run main function when script is executed
if __name__ == "__main__":
    main()