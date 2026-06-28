from core.native_methods import NativeMethods

class ProcessLocator:

    @staticmethod
    def get_process_pid(process_name: str, require_visible: bool = False):
        pids = NativeMethods.get_all_pids()
        
        for pid in pids:
            if pid == 0:
                continue
            
            if NativeMethods.get_process_name(pid) == process_name:
                if require_visible:
                    if NativeMethods.is_process_visible(pid):
                        return pid
                    else:
                        continue
                
                return pid
                
        return None