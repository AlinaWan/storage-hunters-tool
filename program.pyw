# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__author__ = "Riri"
__license__ = "MIT"

import faulthandler
faulthandler.enable()

from src.application_orchestrator import ApplicationOrchestrator

class Program():
    @staticmethod
    def main():
        orchestrator = ApplicationOrchestrator()
        orchestrator.run()

if __name__ == "__main__":
    Program.main()