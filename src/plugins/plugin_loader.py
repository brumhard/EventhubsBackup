import importlib


class Plugin_Loader:
    @staticmethod
    def load(path, class_name):
        spec = importlib.util.spec_from_file_location("plugin", path)
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
