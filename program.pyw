# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__author__ = "Riri"
__license__ = "MIT"

import faulthandler
faulthandler.enable()

from src.application_orchestrator import ApplicationOrchestrator
from src.factories.application_factory import ApplicationFactory

class Program():
    @staticmethod
    def main():
        factory = ApplicationFactory()
        orchestrator = ApplicationOrchestrator(factory)
        orchestrator.run()

if __name__ == "__main__":
    Program.main()