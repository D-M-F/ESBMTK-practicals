import ctypes
import os
from ctypes import wintypes as w

# Inherited by diagnostic child processes; do not show Windows crash dialogs.
ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
class ExceptionRecord(ctypes.Structure):
    _fields_ = [('code', w.DWORD), ('flags', w.DWORD), ('record', ctypes.c_void_p),
                ('address', ctypes.c_void_p), ('count', w.DWORD),
                ('info', ctypes.c_size_t * 15)]
class ExceptionPointers(ctypes.Structure):
    _fields_ = [('record', ctypes.POINTER(ExceptionRecord)), ('context', ctypes.c_void_p)]
class ProcName(ctypes.Union):
    _fields_ = [('name', ctypes.c_char_p), ('ordinal', w.DWORD)]
class Proc(ctypes.Structure):
    _fields_ = [('by_name', w.BOOL), ('value', ProcName)]
class DelayLoadInfo(ctypes.Structure):
    _fields_ = [('size', w.DWORD), ('descriptor', ctypes.c_void_p),
                ('function', ctypes.c_void_p), ('dll', ctypes.c_char_p),
                ('proc', Proc), ('module', ctypes.c_void_p),
                ('resolved_function', ctypes.c_void_p), ('last_error', w.DWORD)]
@ctypes.WINFUNCTYPE(w.LONG, ctypes.POINTER(ExceptionPointers))
def handler(pointer):
    record = pointer.contents.record.contents
    if record.code in (0xC06D007E, 0xC06D007F) and record.count:
        info = ctypes.cast(record.info[0], ctypes.POINTER(DelayLoadInfo)).contents
        filename = ctypes.create_unicode_buffer(32768)
        ctypes.windll.kernel32.GetModuleFileNameW(ctypes.c_void_p(info.module), filename, len(filename))
        text = f'DELAY_LOAD_FAILURE code={record.code:#x} dll={info.dll!r} proc={info.proc.value.name if info.proc.by_name else info.proc.value.ordinal!r} module={filename.value!r} error={info.last_error}\n'
        os.write(2, text.encode('utf-8', errors='replace'))
        modules = (ctypes.c_void_p * 2048)()
        needed = w.DWORD()
        process = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.psapi.EnumProcessModules(ctypes.c_void_p(process), modules, ctypes.sizeof(modules), ctypes.byref(needed))
        for module in modules[:needed.value // ctypes.sizeof(ctypes.c_void_p)]:
            name = ctypes.create_unicode_buffer(32768)
            ctypes.windll.kernel32.GetModuleFileNameW(ctypes.c_void_p(module), name, len(name))
            if any(part in name.value.lower() for part in ('omp', 'mkl', 'blas')):
                os.write(2, ('LOADED: ' + name.value + '\n').encode('utf-8', errors='replace'))
    return 0
ctypes.windll.kernel32.AddVectoredExceptionHandler.argtypes = [w.ULONG, ctypes.c_void_p]
ctypes.windll.kernel32.AddVectoredExceptionHandler.restype = ctypes.c_void_p
_handle = ctypes.windll.kernel32.AddVectoredExceptionHandler(1, handler)
