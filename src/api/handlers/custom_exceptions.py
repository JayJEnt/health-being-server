class MissingVariables(Exception):
    def __init__(self):
        super().__init__("Missing required environment variables")
