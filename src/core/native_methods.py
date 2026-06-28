import ctypes
from ctypes import wintypes
from pathlib import Path
from typing import Final as ReadOnly, final as sealed

if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

@sealed
class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", ULONG_PTR),
        ("InternalHigh", ULONG_PTR),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", wintypes.HANDLE),
    ]

@sealed
class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG),
    ]

@sealed
class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", wintypes.DWORD),
    ]

@sealed
class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1),
    ]

@sealed
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

@sealed
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

@sealed
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT),
    ]

@sealed
class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("un", INPUT_UNION),
    ]

@sealed
class NativeMethods:

    _advapi32: ReadOnly = ctypes.WinDLL("advapi32")
    _dwmapi: ReadOnly = ctypes.WinDLL("dwmapi")
    _kernel32: ReadOnly = ctypes.WinDLL("kernel32")
    _psapi: ReadOnly = ctypes.WinDLL("psapi")
    _user32: ReadOnly = ctypes.WinDLL("user32")

    # Local DLLs
    _vision_lib: ReadOnly = ctypes.WinDLL(Path(__file__).resolve().parent.parent / "native" / "core_vision.dll")

    _DWMWA_WINDOW_CORNER_PREFERENCE: ReadOnly = 33
    _DWMWCP_ROUND: ReadOnly = 2

    _DPI_AWARENESS_CONTEXT_UNAWARE = ctypes.c_void_p(-1)
    _DPI_AWARENESS_CONTEXT_SYSTEM_AWARE = ctypes.c_void_p(-2)
    _DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE = ctypes.c_void_p(-3)
    _DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = ctypes.c_void_p(-4)

    _FILE_LIST_DIRECTORY: ReadOnly = 0x0001
    _FILE_SHARE_READ: ReadOnly = 0x00000001
    _FILE_SHARE_WRITE: ReadOnly = 0x00000002
    _OPEN_EXISTING: ReadOnly = 3
    _FILE_FLAG_BACKUP_SEMANTICS: ReadOnly = 0x02000000
    _FILE_NOTIFY_CHANGE_FILE_NAME: ReadOnly = 0x00000001
    _FILE_NOTIFY_CHANGE_SIZE: ReadOnly = 0x00000008
    _FILE_NOTIFY_CHANGE_LAST_WRITE: ReadOnly = 0x00000010

    _MOUSEEVENTF_MOVE: ReadOnly = 0x0001
    _MOUSEEVENTF_ABSOLUTE: ReadOnly = 0x8000

    _MOUSEEVENTF_LEFTDOWN: ReadOnly = 0x0002
    _MOUSEEVENTF_LEFTUP: ReadOnly = 0x0004
    _MOUSEEVENTF_RIGHTDOWN: ReadOnly = 0x0008
    _MOUSEEVENTF_RIGHTUP: ReadOnly = 0x0010
    _MOUSEEVENTF_MIDDLEDOWN: ReadOnly = 0x0020
    _MOUSEEVENTF_MIDDLEUP: ReadOnly = 0x0040
    _INPUT_MOUSE: ReadOnly = 0

    _KEYEVENTF_SCANCODE: ReadOnly = 0x0008
    _KEYEVENTF_KEYUP: ReadOnly = 0x0002
    _INPUT_KEYBOARD: ReadOnly = 1

    _TOKEN_ADJUST_PRIVILEGES: ReadOnly = 0x20
    _TOKEN_QUERY: ReadOnly = 0x8
    _SE_PRIVILEGE_ENABLED: ReadOnly = 0x2

    _PROCESS_QUERY_INFORMATION: ReadOnly = 0x0400
    _PROCESS_VM_READ: ReadOnly = 0x0010
    _SYNCHRONIZE: ReadOnly = 0x00100000

    _FILE_FLAG_OVERLAPPED: ReadOnly = 0x40000000
    _WAIT_OBJECT_0: ReadOnly = 0x00000000
    _INFINITE: ReadOnly = 0xFFFFFFFF

    INT = ctypes.c_int
    UBYTE = ctypes.c_ubyte

    ERROR_ALREADY_EXISTS: ReadOnly = 183

    INVALID_HANDLE_VALUE: ReadOnly = wintypes.HANDLE(-1).value
    
    MB_ICONERROR: ReadOnly = 0x10
    MB_ICONWARNING: ReadOnly = 0x30
    MB_ICONINFORMATION: ReadOnly = 0x40
    MB_ICONQUESTION: ReadOnly = 0x20

    MB_OK: ReadOnly = 0x00000000
    MB_OKCANCEL: ReadOnly = 0x00000001
    MB_YESNO: ReadOnly = 0x00000004
    MB_YESNOCANCEL: ReadOnly = 0x00000003
    MB_ABORTRETRYIGNORE: ReadOnly = 0x00000002
    MB_RETRYCANCEL: ReadOnly = 0x00000005
    MB_CANCELTRYCONTINUE: ReadOnly = 0x00000006
    MB_HELP: ReadOnly = 0x00004000

    WM_QUIT: ReadOnly = 0x0012
    WM_HOTKEY: ReadOnly = 0x0312

    _advapi32.InitiateSystemShutdownExW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR, wintypes.DWORD, wintypes.BOOL, wintypes.BOOL, wintypes.DWORD]
    _advapi32.InitiateSystemShutdownExW.restype = wintypes.BOOL

    _advapi32.AbortSystemShutdownW.argtypes = [wintypes.LPWSTR]
    _advapi32.AbortSystemShutdownW.restype = wintypes.BOOL

    _advapi32.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    _advapi32.OpenProcessToken.restype = wintypes.BOOL

    _advapi32.LookupPrivilegeValueW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR, ctypes.POINTER(LUID)]
    _advapi32.LookupPrivilegeValueW.restype = wintypes.BOOL

    _advapi32.AdjustTokenPrivileges.argtypes = [wintypes.HANDLE, wintypes.BOOL, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p, ctypes.c_void_p]
    _advapi32.AdjustTokenPrivileges.restype = wintypes.BOOL

    _dwmapi.DwmSetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
    _dwmapi.DwmSetWindowAttribute.restype = ctypes.HRESULT

    _kernel32.CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
    _kernel32.CreateMutexW.restype = wintypes.HANDLE

    _kernel32.ReleaseMutex.argtypes = [wintypes.HANDLE]
    _kernel32.ReleaseMutex.restype = wintypes.BOOL

    _kernel32.GetLastError.argtypes = []
    _kernel32.GetLastError.restype = wintypes.DWORD

    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL

    _kernel32.CreateEventW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.BOOL, wintypes.LPCWSTR]
    _kernel32.CreateEventW.restype = wintypes.HANDLE

    _kernel32.SetEvent.argtypes = [wintypes.HANDLE]
    _kernel32.SetEvent.restype = wintypes.BOOL

    _kernel32.ResetEvent.argtypes = [wintypes.HANDLE]
    _kernel32.ResetEvent.restype = wintypes.BOOL

    _kernel32.WaitForMultipleObjects.argtypes = [wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE), wintypes.BOOL, wintypes.DWORD]
    _kernel32.WaitForMultipleObjects.restype = wintypes.DWORD

    _kernel32.CancelIo.argtypes = [wintypes.HANDLE]
    _kernel32.CancelIo.restype = wintypes.BOOL

    _kernel32.GetOverlappedResult.argtypes = [wintypes.HANDLE, ctypes.POINTER(OVERLAPPED), ctypes.POINTER(wintypes.DWORD), wintypes.BOOL]
    _kernel32.GetOverlappedResult.restype = wintypes.BOOL

    _kernel32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    _kernel32.CreateFileW.restype = wintypes.HANDLE

    _kernel32.ReadDirectoryChangesW.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD, wintypes.BOOL, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(OVERLAPPED), wintypes.LPVOID]
    _kernel32.ReadDirectoryChangesW.restype = wintypes.BOOL

    _kernel32.GetWindowsDirectoryW.argtypes = [wintypes.LPWSTR, wintypes.UINT]
    _kernel32.GetWindowsDirectoryW.restype = wintypes.UINT

    _kernel32.GetCurrentProcess.argtypes = []
    _kernel32.GetCurrentProcess.restype = wintypes.HANDLE

    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE

    _psapi.EnumProcesses.argtypes = [ctypes.POINTER(wintypes.DWORD), wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    _psapi.EnumProcesses.restype = wintypes.BOOL

    _user32.EnumWindows.argtypes = [ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
    _user32.EnumWindows.restype = wintypes.BOOL

    _user32.IsWindowVisible.argtypes = [wintypes.HWND]
    _user32.IsWindowVisible.restype = wintypes.BOOL

    _user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    _user32.GetWindowThreadProcessId.restype = wintypes.DWORD

    _user32.MapVirtualKeyW.argtypes = [wintypes.UINT, wintypes.UINT]
    _user32.MapVirtualKeyW.restype = wintypes.UINT

    _user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
    _user32.SendInput.restype = wintypes.UINT

    _psapi.GetModuleBaseNameW.argtypes = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
    _psapi.GetModuleBaseNameW.restype = wintypes.DWORD

    _user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
    _user32.RegisterHotKey.restype = wintypes.BOOL

    _user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
    _user32.UnregisterHotKey.restype = wintypes.BOOL

    _user32.PostThreadMessageW.argtypes = [wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    _user32.PostThreadMessageW.restype = wintypes.BOOL

    _user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
    _user32.GetMessageW.restype = wintypes.BOOL

    _user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
    _user32.TranslateMessage.restype = wintypes.BOOL

    _user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
    _user32.DispatchMessageW.restype = wintypes.LPARAM

    _user32.GetParent.argtypes = [wintypes.HWND]
    _user32.GetParent.restype = wintypes.HWND

    _user32.FindWindowW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
    _user32.FindWindowW.restype = wintypes.HWND

    _user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    _user32.GetWindowRect.restype = wintypes.BOOL

    _user32.GetSystemMetrics.argtypes = [ctypes.c_int]
    _user32.GetSystemMetrics.restype = ctypes.c_int

    _user32.MessageBoxW.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
    _user32.MessageBoxW.restype = ctypes.c_int

    _user32.SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
    _user32.SetProcessDpiAwarenessContext.restype = wintypes.BOOL

    # Local argtypes/restype
    _vision_lib.check_pixel_columns.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # pixels
        ctypes.c_int,                   # height
        ctypes.c_int,                   # stride
        ctypes.POINTER(ctypes.c_int),   # x_offsets
        ctypes.POINTER(ctypes.c_ubyte), # target_bgrs
        ctypes.c_int,                   # count
        ctypes.c_int                    # tolerance
    ]
    _vision_lib.check_pixel_columns.restype = ctypes.c_int

    # Memory management related methods
    @staticmethod
    def create_buffer(size=1024):
        return ctypes.create_string_buffer(size)

    @staticmethod
    def byref(obj):
        return ctypes.byref(obj)

    @staticmethod
    def cast_to_ubyte_ptr(obj):
        return (ctypes.c_ubyte * len(obj)).from_buffer(obj) # take a raw python buffer

    @staticmethod
    def create_int_array(values):
        return (ctypes.c_int * len(values))(*values)

    @staticmethod
    def create_ubyte_array(values):
        return (ctypes.c_ubyte * len(values))(*values)

    # Mutex related methods
    @staticmethod
    def create_mutex(name: str, initial_owner: bool = True):
        return NativeMethods._kernel32.CreateMutexW(None, initial_owner, name)

    @staticmethod
    def release_mutex(handle):
        return NativeMethods._kernel32.ReleaseMutex(handle)

    @staticmethod
    def get_last_error():
        return NativeMethods._kernel32.GetLastError()

    @staticmethod
    def create_single_instance_mutex(name: str):
        handle = NativeMethods.create_mutex(name, True)

        if not handle:
            return None, False

        already_exists = (NativeMethods.get_last_error() == NativeMethods.ERROR_ALREADY_EXISTS)
        return handle, not already_exists

    # Overlapped IO related methods
    @staticmethod
    def create_overlapped(event):
        ov = OVERLAPPED()
        ov.hEvent = event
        return ov

    @staticmethod
    def create_event(manual_reset=True, initial_state=False):
        return NativeMethods._kernel32.CreateEventW(None, manual_reset, initial_state, None)

    @staticmethod
    def set_event(hEvent):
        return NativeMethods._kernel32.SetEvent(hEvent)

    @staticmethod
    def reset_event(hEvent):
        return NativeMethods._kernel32.ResetEvent(hEvent)

    @staticmethod
    def wait_for_multiple_objects(handles, wait_all=False, timeout=0xFFFFFFFF):
        handle_array = (wintypes.HANDLE * len(handles))(*handles)
        return NativeMethods._kernel32.WaitForMultipleObjects(len(handles), handle_array, wait_all, timeout)

    @staticmethod
    def cancel_io(handle):
        return NativeMethods._kernel32.CancelIo(handle)

    @staticmethod
    def get_overlapped_result(handle, overlapped, bytes_returned, wait):
        return NativeMethods._kernel32.GetOverlappedResult(
            handle,
            ctypes.byref(overlapped),
            bytes_returned,
            wait
        )

    # UI & window related methods
    @staticmethod
    def message_box(text, title, flags=MB_OK):
        return NativeMethods._user32.MessageBoxW(
            None,
            text,
            title,
            flags
        )

    @staticmethod
    def get_parent(hwnd):
        return NativeMethods._user32.GetParent(hwnd)

    @staticmethod
    def apply_rounded_corners(hwnd):
        pref = ctypes.c_int(NativeMethods._DWMWCP_ROUND)

        NativeMethods._dwmapi.DwmSetWindowAttribute(
            hwnd,
            NativeMethods._DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(pref),
            ctypes.sizeof(pref)
        )

    @staticmethod
    def set_process_dpi_awareness_context(context=-4):
        ctx_map = {
            -1: NativeMethods._DPI_AWARENESS_CONTEXT_UNAWARE,
            -2: NativeMethods._DPI_AWARENESS_CONTEXT_SYSTEM_AWARE,
            -3: NativeMethods._DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE,
            -4: NativeMethods._DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2,
        }

        return NativeMethods._user32.SetProcessDpiAwarenessContext(
            ctx_map.get(context, NativeMethods._DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
        )

    @staticmethod
    def find_window(class_name: str | None, window_name: str | None) -> int:
        return NativeMethods._user32.FindWindowW(class_name, window_name)

    @staticmethod
    def get_window_rect(hwnd: int) -> tuple[int, int, int, int]:
        rect = wintypes.RECT()
        if NativeMethods._user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return (rect.left, rect.top, rect.right, rect.bottom)
        return (0, 0, 0, 0)

    # Directory monitoring related methods
    @staticmethod
    def get_filename_from_notify_buffer(buffer):
        # Offset 12 starts the filename in the struct FILE_NOTIFY_INFORMATION
        file_name_len = int.from_bytes(buffer[8:12], "little")
        return buffer[12:12+file_name_len].decode("utf-16")

    @staticmethod
    def open_directory_handle(path):
        return NativeMethods._kernel32.CreateFileW(
            path,
            NativeMethods._FILE_LIST_DIRECTORY,
            NativeMethods._FILE_SHARE_READ | NativeMethods._FILE_SHARE_WRITE,
            None,
            NativeMethods._OPEN_EXISTING,
            NativeMethods._FILE_FLAG_BACKUP_SEMANTICS | NativeMethods._FILE_FLAG_OVERLAPPED,
            wintypes.HANDLE(None)
        )

    @staticmethod
    def read_directory_changes(handle, buffer, overlapped_ptr):
        return NativeMethods._kernel32.ReadDirectoryChangesW(
            handle,
            buffer,
            ctypes.sizeof(buffer),
            False,
            NativeMethods._FILE_NOTIFY_CHANGE_FILE_NAME | 
            NativeMethods._FILE_NOTIFY_CHANGE_SIZE | 
            NativeMethods._FILE_NOTIFY_CHANGE_LAST_WRITE,
            None,
            overlapped_ptr,
            None
        )

    @staticmethod
    def close_handle(handle):
        NativeMethods._kernel32.CloseHandle(handle)

    @staticmethod
    def get_windows_directory() -> str:
        # MAX_PATH is 260
        buffer = ctypes.create_unicode_buffer(260)
        size = NativeMethods._kernel32.GetWindowsDirectoryW(buffer, 260)
        if size == 0:
            return ""
        return buffer.value

    # Process management related methods
    @staticmethod
    def get_all_pids():
        pids = (wintypes.DWORD * 1024)()
        cb = ctypes.sizeof(pids)
        bytes_returned = wintypes.DWORD()
        
        if NativeMethods._psapi.EnumProcesses(pids, cb, ctypes.byref(bytes_returned)):
            count = bytes_returned.value // ctypes.sizeof(wintypes.DWORD)
            return [pids[i] for i in range(count)]
        return []

    @staticmethod
    def is_process_visible(pid: int) -> bool:
        found_visible = [False]
    
        def callback(hwnd, lParam):
            if NativeMethods._user32.IsWindowVisible(hwnd):
                window_pid = wintypes.DWORD()
                NativeMethods._user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
                if window_pid.value == pid:
                    found_visible[0] = True
                    return False
            return True

        enum_proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        NativeMethods._user32.EnumWindows(enum_proc(callback), 0)
        return found_visible[0]

    @staticmethod
    def get_process_name(pid: int) -> str:
        handle = NativeMethods._kernel32.OpenProcess(
            NativeMethods._PROCESS_QUERY_INFORMATION | NativeMethods._PROCESS_VM_READ, 
            False, 
            pid
        )
        if not handle:
            return ""

        name_buffer = ctypes.create_unicode_buffer(260)
        success = NativeMethods._psapi.GetModuleBaseNameW(handle, None, name_buffer, 260)
        NativeMethods._kernel32.CloseHandle(handle)
        
        return name_buffer.value if success else ""

    @staticmethod
    def open_process(pid):
        return NativeMethods._kernel32.OpenProcess(
            NativeMethods._SYNCHRONIZE,
            False,
            pid
        )

    @staticmethod
    def wait_for_single_object(handle, timeout=_INFINITE):
        return NativeMethods._kernel32.WaitForSingleObject(handle, timeout)

    @staticmethod
    def enable_shutdown_privilege():
        token = wintypes.HANDLE()

        # Open current process token
        if not NativeMethods._advapi32.OpenProcessToken(
            NativeMethods._kernel32.GetCurrentProcess(),
            NativeMethods._TOKEN_ADJUST_PRIVILEGES | NativeMethods._TOKEN_QUERY,
            ctypes.byref(token)
        ):
            return False

        luid = LUID()

        # Lookup shutdown privilege
        if not NativeMethods._advapi32.LookupPrivilegeValueW(
            None,
            "SeShutdownPrivilege",
            ctypes.byref(luid)
        ):
            return False

        tp = TOKEN_PRIVILEGES()
        tp.PrivilegeCount = 1
        tp.Privileges[0].Luid = luid
        tp.Privileges[0].Attributes = NativeMethods._SE_PRIVILEGE_ENABLED

        # Enable privilege
        if not NativeMethods._advapi32.AdjustTokenPrivileges(
            token,
            False,
            ctypes.byref(tp),
            0,
            None,
            None
        ):
            return False

        return True

    @staticmethod
    def initiate_system_shutdown(timeout_sec=15, message="Shutting down."):
        return NativeMethods._advapi32.InitiateSystemShutdownExW(
            None,
            message,
            timeout_sec,
            True,   # force close apps
            False,  # shutdown (not reboot)
            0
        )

    @staticmethod
    def abort_system_shutdown():
        return NativeMethods._advapi32.AbortSystemShutdownW(None)

    # Hotkey related methods
    @staticmethod
    def create_msg():
        return wintypes.MSG()

    @staticmethod
    def register_hotkey(hwnd, id, modifiers, key):
        return NativeMethods._user32.RegisterHotKey(hwnd, id, modifiers, key)

    @staticmethod
    def unregister_hotkey(hwnd, id):
        return NativeMethods._user32.UnregisterHotKey(hwnd, id)

    @staticmethod
    def get_message(msg):
        return NativeMethods._user32.GetMessageW(ctypes.byref(msg), None, 0, 0)

    @staticmethod
    def translate_message(msg):
        NativeMethods._user32.TranslateMessage(ctypes.byref(msg))

    @staticmethod
    def dispatch_message(msg):
        NativeMethods._user32.DispatchMessageW(ctypes.byref(msg))

    @staticmethod
    def post_thread_message(thread_id, msg_type, wparam=0, lparam=0):
        return NativeMethods._user32.PostThreadMessageW(thread_id, msg_type, wparam, lparam)

    # Screen metrics related methods
    @staticmethod
    def get_system_metrics(index):
        return NativeMethods._user32.GetSystemMetrics(index)

    @staticmethod
    def get_screen_width():
        return NativeMethods.get_system_metrics(0)

    @staticmethod
    def get_screen_height():
        return NativeMethods.get_system_metrics(1)

    # Input related methods
    @staticmethod
    def move_mouse(x: int, y: int, relative: bool = False):
        inp = INPUT()
        inp.type = NativeMethods._INPUT_MOUSE
    
        if relative:
            inp.un.mi = MOUSEINPUT(x, y, 0, NativeMethods._MOUSEEVENTF_MOVE, 0, 0)
        else:
            w = NativeMethods._user32.GetSystemMetrics(0) # SM_CXSCREEN
            h = NativeMethods._user32.GetSystemMetrics(1) # SM_CYSCREEN
        
            # (Coord * 65536) / Width
            nx = int((x * 65536) / w)
            ny = int((y * 65536) / h)
        
            flags = NativeMethods._MOUSEEVENTF_MOVE | NativeMethods._MOUSEEVENTF_ABSOLUTE
            inp.un.mi = MOUSEINPUT(nx, ny, 0, flags, 0, 0)

        NativeMethods._user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(INPUT))

    @staticmethod
    def send_mouse_click(button: str, down: bool):
        flags = 0
        if button == 'left':
            flags = NativeMethods._MOUSEEVENTF_LEFTDOWN if down else NativeMethods._MOUSEEVENTF_LEFTUP
        elif button == 'right':
            flags = NativeMethods._MOUSEEVENTF_RIGHTDOWN if down else NativeMethods._MOUSEEVENTF_RIGHTUP
        elif button == 'middle':
            flags = NativeMethods._MOUSEEVENTF_MIDDLEDOWN if down else NativeMethods._MOUSEEVENTF_MIDDLEUP

        inp = INPUT()
        inp.type = NativeMethods._INPUT_MOUSE
        # dx, dy are 0 because we are clicking at the current cursor position
        inp.un.mi = MOUSEINPUT(0, 0, 0, flags, 0, 0)
    
        NativeMethods._user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(INPUT))

    @staticmethod
    def send_key(vk_code: int, down: bool):
        # Convert Virtual Key to Hardware Scan Code
        scan_code = NativeMethods._user32.MapVirtualKeyW(vk_code, 0)
    
        flags = NativeMethods._KEYEVENTF_SCANCODE
        if not down:
            flags |= NativeMethods._KEYEVENTF_KEYUP
        
        inp = INPUT()
        inp.type = NativeMethods._INPUT_KEYBOARD
        # We set wVk to 0 when using SCANCODE flag for game compatibility
        inp.un.ki = KEYBDINPUT(0, scan_code, flags, 0, 0)
    
        NativeMethods._user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(INPUT))

    # Local methods
    @staticmethod
    def pixel_scan(pixel_ptr, height, stride, x_offsets_ptr, target_bgrs_ptr, count, tolerance):
        return NativeMethods._vision_lib.check_pixel_columns(
            pixel_ptr,
            height,
            stride,
            x_offsets_ptr,
            target_bgrs_ptr,
            count,
            tolerance
        )