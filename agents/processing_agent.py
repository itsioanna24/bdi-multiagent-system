from core.bdi_agent import BDIAgent
from core.utils import log, handle_error
from core.scoring import compute_score

class ProcessingAgent(BDIAgent):
    """
    Agent responsible for evaluating and filtering extracted data
    using a score-based adaptive filtering approach.
    """

    def __init__(self, keyword):
        # Initialise base BDI agent with name
        super().__init__("ProcessingAgent")

        # Store keyword used for filtering
        self.keyword = keyword.lower()

        # Initialise list to store filtered results
        self.filtered = []

        # Define intention (BDI concept)
        self.intention = None


    def perceive(self, env):
        # Retrieve extracted data from environment
        self.data = env.get("extracted_data")

        log("[ProcessingAgent] Retrieved extracted data from environment")


    def deliberate(self):
        # Define goal of agent
        self.intention = "evaluate_and_filter"

        log(f"[ProcessingAgent] Intention set: {self.intention}")


    def act(self, env):
        try:
            # Check if data exists
            if not self.data:
                log("[ProcessingAgent] No data available. Waiting...")
                env.update("processed_data", None)
                return

            # Initial strict threshold
            threshold = 2

            # Maximum number of adaptation cycles
            max_cycles = 3

            cycle = 0
            quality_ok = False

            while not quality_ok and cycle < max_cycles:
                log(f"[ProcessingAgent] Processing attempt {cycle + 1}")
                log(f"[ProcessingAgent] Current threshold: {threshold}")

                try:
                    # Apply score-based filtering
                    scored_results = []

                    for item in self.data:
                        score = compute_score(item, self.keyword)    
                        scored_results.append((item, score))

                    # Sort results by score (highest first)
                    scored_results.sort(key=lambda x: x[1], reverse=True)

                    # Log score for transparency
                    for item, score in scored_results:
                        log(f"[ProcessingAgent] Score: {score} | Title: {item.get('title')}")

                    # Extract only items
                    self.filtered = [item for item, score in scored_results if score >= threshold]

                except Exception as e:
                    log(f"[ProcessingAgent] Error during scoring: {str(e)}")
                    self.filtered = []

                # Evaluate quality
                if len(self.filtered) > 0:
                    log("[ProcessingAgent] Quality acceptable")
                    quality_ok = True
                else:
                    # Adaptive behaviour: relax threshold
                    threshold -= 1
                    log(f"[ProcessingAgent] No results → lowering threshold to {threshold}")

                cycle += 1

            # If still no results → fallback
            if not self.filtered:
                log("[ProcessingAgent] No results after adaptation")

                # Best-effort result
                self.filtered = self.data[:1]

                log("[ProcessingAgent] Using fallback result")

            # Store results
            env.update("processed_data", self.filtered)

            log("[ProcessingAgent] Processed data stored in environment")

        except Exception as e:
            handle_error("ProcessingAgent", e)
            env.update("processed_data", None)