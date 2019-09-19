import importlib
from pathlib import Path


class Plugin_Loader:
    @staticmethod
    def load(class_name, path = None):
        if path == None:
            current_path = Path(__file__).parent
            abs_file_path = Path(current_path).joinpath(f"{class_name}.py")
        spec = importlib.util.spec_from_file_location("plugin", str(abs_file_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_ = getattr(module, class_name)
        instance = class_()

        method = getattr(class_, "process", None)
        if not callable(method):
            raise Exception(
                f"Class {class_name} doesn't have process method which is required for plugins"
            )
        return instance





# return method
