import importlib
import inspect
from typing import final as sealed, Any

@sealed
class ReflectionUtil:
    @staticmethod
    def instantiate_class_from_fully_qualified_name(fully_qualified_name: str, *args, **kwargs) -> Any:
        try:
            module_path, class_name = fully_qualified_name.rsplit(".", 1)
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            if not inspect.isclass(cls):
                raise TypeError(f"{fully_qualified_name} is not a class.")
            return cls(*args, **kwargs)
        except (ValueError, AttributeError, ModuleNotFoundError) as e:
            raise ImportError(f"Failed to dynamically load target configuration path '{fully_qualified_name}'.") from e