# Utility module for shared helper functions

def log(message):
    # Print log message to console
    # WHY: Centralised logging ensures consistent output format across agents
    print(f"[LOG] {message}")


def handle_error(context, error):
    # Generic error handler for all agents
    # WHY: Prevents system crash and provides clear debugging information
    print(f"[ERROR] in {context}: {str(error)}")
