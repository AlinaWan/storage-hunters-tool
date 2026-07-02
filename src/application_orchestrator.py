import atexit
import signal
from _tkinter import TclError

import cv2

from src.core.constants import Constants
from src.core.interfaces import IApplicationOrchestrator, IApplicationFactory
from src.core.native_methods import NativeMethods
from src.utils.safe_message_box import SafeMessageBox

class ApplicationOrchestrator(IApplicationOrchestrator):
    def __init__(self, factory: IApplicationFactory):
        self.factory = factory

    def run(self):
        try:
            NativeMethods.set_process_dpi_awareness_context(-4)
        except Exception:
            pass

        mutex, is_first_instance = NativeMethods.create_single_instance_mutex(f"Global\\{Constants.GUID}")
        if not is_first_instance:
            self._show_already_running()
            raise SystemExit(0)

        app = self.factory.create()
        app.mutex_handle = mutex

        atexit.register(app.current_domain_process_exit)
        signal.signal(signal.SIGINT, lambda *_,: setattr(app, 'should_exit', True))

        try:
            app.run()
        except (cv2.error, TclError) as e:
            self._handle_fatal_error(e)
            raise
        except Exception as e:
            self._handle_fatal_error(e)
            raise

    def _show_already_running(self):
        SafeMessageBox.show_message_box_sync(SafeMessageBox,
            "Another instance of Storage Hunters Tool is already running.",
            "Already Running",
            NativeMethods.MB_OK | NativeMethods.MB_ICONINFORMATION
        )

    def _handle_fatal_error(self, e):
        if isinstance(e, cv2.error):
            message = (
                "An OpenCV error occurred during runtime:\n\n"
                f"{e}\n\n"
                "The program will now exit."
            )

        elif isinstance(e, TclError):
            if "bad geometry specifier" in str(e):
                message = (
                    "Tcl raised bad geometry specifier during runtime:\n\n"
                    f"{e}\n\n"
                    "This is usually because a configuration setting is too negative, and "
                    "Tcl does not allow negative width or height in geometry strings.\n\n"
                    "The program will now exit."
                )
            else:
                message = (
                    "A Tcl error occurred during runtime:\n\n"
                    f"{e}\n\n"
                    "The program will now exit."
                )

        else:
            message = (
                "An unexpected error occurred during runtime:\n\n"
                f"{e}\n\n"
                "The program will now exit."
            )

        SafeMessageBox.show_message_box_sync(
            SafeMessageBox, message, "Fatal Error", NativeMethods.MB_OK | NativeMethods.MB_ICONERROR
        )