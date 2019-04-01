"""
IMDBAgentGenerator
"""

from fake_useragent import UserAgent

class IMDBAgentGenerator():
    def __init__(self):
        self.generator = UserAgent()

    def random_agent(self):
        return self.generator.random