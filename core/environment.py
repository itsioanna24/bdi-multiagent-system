# Shared blackboard environment

class Environment:
# Shared blackboard environment
    def __init__(self):
        # Initialise an empty dictionary to store shared data
        self.data = {}


    def update(self, key, value):
        # Store value in environment using key
        self.data[key] = value


    def get(self, key):
        # Retrieve a value from the environment using a key
        return self.data.get(key, None)