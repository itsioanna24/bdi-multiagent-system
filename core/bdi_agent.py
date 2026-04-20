from abc import ABC, abstractmethod
from core.utils import log, handle_error # Import logging and error handling

class BDIAgent:
# Base BDI agent.

    def __init__(self, name, env=None):
        # Store agent name for identification in logs
        self.name = name

        # Store reference to environment
        self.env = env

        # Initialise beliefs (what agent knows)
        self.beliefs = None
        
        # Initialise intention (what agent plans to do)
        self.intention = None


    @abstractmethod
    def perceive(self, env):
        # Read current state of environment
        # WHY: Updates beliefs based on latest shared data
        log(f"[{self.name}] Perceiving environment...")
        self.beliefs = self.env.data


    @abstractmethod
    def deliberate(self):
        # Placeholder method for decision-making
        # WHY: Each specialised agent defines its own reasoning logic
        pass


    @abstractmethod
    def act(self, env):
        # Placeholder method for action execution
        pass


    def run(self, env):
        try:
            # Start of BDI cycle
            log(f"\n[{self.name}] --- BDI Cycle Start ---")

            # Step 1: Perceive environment
            self.perceive(env)

            # Step 2: Decide what to do
            self.deliberate()

            # Step 3: Execute action
            self.act(env)

            # End of BDI cycle
            log(f"[{self.name}] --- BDI Cycle End ---\n")

        except Exception as e:
            # Catch any runtime errors
            # WHY: Ensures system continues even if one agent fails
            handle_error(self.name, e)
