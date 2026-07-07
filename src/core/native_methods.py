import ctypes
import struct
from ctypes import wintypes
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

@sealed
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
    """Windows DLL platform native methods."""

    _advapi32: ReadOnly = ctypes.WinDLL("advapi32")
    _dwmapi: ReadOnly = ctypes.WinDLL("dwmapi")
    _kernel32: ReadOnly = ctypes.WinDLL("kernel32")
    _psapi: ReadOnly = ctypes.WinDLL("psapi")
    _shell32: ReadOnly = ctypes.WinDLL("shell32")
    _user32: ReadOnly = ctypes.WinDLL("user32")

    _DWMWA_WINDOW_CORNER_PREFERENCE: ReadOnly = 33
    _DWMWCP_ROUND: ReadOnly = 2

    _DPI_AWARENESS_CONTEXT_UNAWARE = ctypes.c_void_p(-1)
    _DPI_AWARENESS_CONTEXT_SYSTEM_AWARE = ctypes.c_void_p(-2)
    _DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE = ctypes.c_void_p(-3)
    _DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = ctypes.c_void_p(-4)

    _GENERIC_READ: ReadOnly = 0x80000000
    _GENERIC_WRITE: ReadOnly = 0x40000000
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

    _SW_HIDE: ReadOnly = 0x00
    _SW_SHOWNORMAL: ReadOnly = 0x01
    _SW_NORMAL: ReadOnly = 0x01
    _SW_SHOWMINIMIZED: ReadOnly = 0x02
    _SW_SHOWMAXIMIZED: ReadOnly = 0x03
    _SW_MAXIMIZE: ReadOnly = 0x03
    _SW_SHOWNOACTIVATE: ReadOnly = 0x04
    _SW_SHOW: ReadOnly = 0x05
    _SW_MINIMIZE: ReadOnly = 0x06
    _SW_SHOWMINNOACTIVE: ReadOnly = 0x07
    _SW_SHOWNA: ReadOnly = 0x08
    _SW_RESTORE: ReadOnly = 0x09
    _SW_SHOWDEFAULT: ReadOnly = 0x0A
    _SW_FORCEMINIMIZE: ReadOnly = 0x0B
    _SW_MAX: ReadOnly = 0x0B

    _GWL_WNDPROC: ReadOnly = -4
    _WM_DROPFILES: ReadOnly = 0x0233

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

    IDOK: ReadOnly = 0x00000001
    IDCANCEL: ReadOnly = 0x00000002
    IDABORT: ReadOnly = 0x00000003
    IDRETRY: ReadOnly = 0x00000004
    IDIGNORE: ReadOnly = 0x00000005
    IDYES: ReadOnly = 0x00000006
    IDNO: ReadOnly = 0x00000007

    WM_QUIT: ReadOnly = 0x0012
    WM_HOTKEY: ReadOnly = 0x0312

    _WNDPROC_FUNC = ctypes.WINFUNCTYPE(ctypes.c_int64, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

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

    _advapi32.GetUserNameW.argtypes = [wintypes.LPWSTR, wintypes.LPDWORD]
    _advapi32.GetUserNameW.restype = wintypes.BOOL

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

    _kernel32.WriteFile.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    _kernel32.WriteFile.restype = wintypes.BOOL

    _kernel32.ReadFile.argtypes = [wintypes.HANDLE, ctypes.c_char_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    _kernel32.ReadFile.restype = wintypes.BOOL

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

    _user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    _user32.ShowWindow.restype = wintypes.BOOL

    _user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    _user32.SetForegroundWindow.restype = wintypes.BOOL

    _user32.GetForegroundWindow.argtypes = []
    _user32.GetForegroundWindow.restype = wintypes.HWND

    _user32.IsIconic.argtypes = [wintypes.HWND]
    _user32.IsIconic.restype = wintypes.BOOL

    if ctypes.sizeof(ctypes.c_void_p) == 8:
        _user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]
        _user32.SetWindowLongPtrW.restype = ctypes.c_void_p
        _user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        _user32.CallWindowProcW.restype = ctypes.c_int64
    else:
        _user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
        _user32.SetWindowLongW.restype = ctypes.c_long
        _user32.CallWindowProcW.argtypes = [ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        _user32.CallWindowProcW.restype = ctypes.c_long

    _shell32.DragAcceptFiles.argtypes = [wintypes.HWND, wintypes.BOOL]
    _shell32.DragAcceptFiles.restype = None

    _shell32.DragQueryFileW.argtypes = [wintypes.HANDLE, wintypes.UINT, wintypes.LPWSTR, wintypes.UINT]
    _shell32.DragQueryFileW.restype = wintypes.UINT

    _shell32.DragFinish.argtypes = [wintypes.HANDLE]
    _shell32.DragFinish.restype = None

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

    @staticmethod
    def open_discord_pipe(pipe_index: int) -> int:
        pipe_name = f"\\\\.\\pipe\\discord-ipc-{pipe_index}"
        return NativeMethods._kernel32.CreateFileW(
            pipe_name,
            NativeMethods._GENERIC_READ | NativeMethods._GENERIC_WRITE,
            NativeMethods._FILE_SHARE_READ | NativeMethods._FILE_SHARE_WRITE,
            None,
            NativeMethods._OPEN_EXISTING,
            0,
            wintypes.HANDLE(None)
        )

    @staticmethod
    def _read_exact(handle: int, size: int) -> bytes:
        buf = bytearray()
    
        while len(buf) < size:
            chunk = ctypes.create_string_buffer(size - len(buf))
            read = wintypes.DWORD(0)

            ok = NativeMethods._kernel32.ReadFile(
                handle,
                chunk,
                size - len(buf),
                ctypes.byref(read),
                None
            )

            if not ok or read.value == 0:
                return b""

            buf += chunk.raw[:read.value]

        return bytes(buf)

    @staticmethod
    def write_pipe(handle: int, data: bytes | bytearray) -> bool:
        written = wintypes.DWORD(0)
        buffer = (ctypes.c_char * len(data)).from_buffer(data)
        
        return bool(NativeMethods._kernel32.WriteFile(
            handle,
            buffer,
            len(data),
            ctypes.byref(written),
            None
        ))

    @staticmethod
    def read_pipe(handle: int) -> bytes:
        header = NativeMethods._read_exact(handle, 8)
        if len(header) != 8:
            return b""

        opcode, length = struct.unpack("<II", header)

        payload = NativeMethods._read_exact(handle, length)
        if len(payload) != length:
            return b""

        return header + payload

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

    def get_current_username():
        # UNLEN is defined in Lmcons.h (256) + null terminator.
        size = wintypes.DWORD(257)
        buffer = ctypes.create_unicode_buffer(size.value)
        NativeMethods._advapi32.GetUserNameW(buffer, ctypes.byref(size))
        return buffer.value

    # Window management related processes
    @staticmethod
    def get_all_hwnds() -> list[int]:
        hwnds = []
        
        def callback(hwnd, lParam):
            hwnds.append(hwnd)
            return True

        enum_proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        NativeMethods._user32.EnumWindows(enum_proc(callback), 0)
        return hwnds

    @staticmethod
    def get_window_pid(hwnd: int) -> int:
        pid = wintypes.DWORD(0)
        NativeMethods._user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value

    @staticmethod
    def is_window_visible(hwnd: int) -> bool:
        return bool(NativeMethods._user32.IsWindowVisible(hwnd))

    @staticmethod
    def get_hwnd_from_pid(pid: int, require_visible: bool = False) -> int | None:
        for hwnd in NativeMethods.get_all_hwnds():
            if hwnd == 0:
                continue

            if NativeMethods.get_window_pid(hwnd) != pid:
                continue

            if require_visible and not NativeMethods.is_window_visible(hwnd):
                continue

            if NativeMethods.get_parent(hwnd):
                continue

            return hwnd
        return None

    @staticmethod
    def force_focus_window(hwnd: int) -> bool:
        if not hwnd:
            return False

        if NativeMethods._user32.IsIconic(hwnd):
            NativeMethods._user32.ShowWindow(hwnd, NativeMethods._SW_RESTORE)
        else:
            NativeMethods._user32.ShowWindow(hwnd, NativeMethods._SW_SHOW)

        return bool(NativeMethods._user32.SetForegroundWindow(hwnd))

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

    @staticmethod
    def register_drag_drop(hwnd: int, callback) -> ctypes.c_void_p:
        NativeMethods._shell32.DragAcceptFiles(hwnd, True)

        proc_container = [None]

        def wnd_proc(hWnd, uMsg, wParam, lParam):
            if uMsg == NativeMethods._WM_DROPFILES:
                hDrop = wintypes.HANDLE(wParam)
                count = NativeMethods._shell32.DragQueryFileW(hDrop, 0xFFFFFFFF, None, 0)
                if count > 0:
                    length = NativeMethods._shell32.DragQueryFileW(hDrop, 0, None, 0)
                    buf = ctypes.create_unicode_buffer(length + 1)
                    NativeMethods._shell32.DragQueryFileW(hDrop, 0, buf, length + 1)
                    
                    NativeMethods._shell32.DragFinish(hDrop)
                    callback(buf.value)
                return 0

            old_handler = proc_container[0]
            if old_handler is not None:
                if ctypes.sizeof(ctypes.c_void_p) == 8:
                    return NativeMethods._user32.CallWindowProcW(old_handler, hWnd, uMsg, wParam, lParam)
                return NativeMethods._user32.CallWindowProcW(old_handler, hWnd, uMsg, wParam, lParam)
            return 0

        NativeMethods._active_dnd_proc = NativeMethods._WNDPROC_FUNC(wnd_proc)
        
        if ctypes.sizeof(ctypes.c_void_p) == 8:
            old_proc = NativeMethods._user32.SetWindowLongPtrW(hwnd, NativeMethods._GWL_WNDPROC, ctypes.cast(NativeMethods._active_dnd_proc, ctypes.c_void_p))
        else:
            old_proc = NativeMethods._user32.SetWindowLongW(hwnd, NativeMethods._GWL_WNDPROC, ctypes.cast(NativeMethods._active_dnd_proc, ctypes.c_long))
            
        proc_container[0] = old_proc
        return old_proc