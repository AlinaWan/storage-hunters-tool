import importlib
import inspect
from typing import final as sealed, Any

@sealed
class ReflectionUtil:
    @staticmethod
    def instantiate_class_from_fqn(fqn: str, *args, **kwargs) -> Any:
        try:
            module_path, class_name = fqn.rsplit(".", 1)
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            if not inspect.isclass(cls):
                raise TypeError(f"{fqn} is not a class.")
            return cls(*args, **kwargs)
        except (ValueError, AttributeError, ModuleNotFoundError) as e:
            raise ImportError(f"Failed to dynamically load target configuration path '{fqn}'.") from e