import importlib
from pathlib import Path
from typing import Optional
from .parser_plugin import Parser_Plugin
import logging

logger = logging.getLogger(__name__)


class Plugin_Loader:
    """Load plugins dynamically by name"""

    @staticmethod
    def load(class_name: str, path: Optional[str] = None) -> Parser_Plugin:
        """Static method to load parser plugins.

        Looks for the module file (class_name.py) in the given directory,
        checks whether it contains the needed process method and return
        an instance of the class to be used.

        Args:
            class_name: Name of the Plugin parser class that should be 
                equivalent to the file name
            path: Absolute path to the file, if none the current directory
                will be used to find the right file
        """
        if path == None:
            current_path = Path(__file__).parent
            path = Path(current_path).joinpath(f"{class_name}.py")
            path = str(path)

        logger.debug(f"Trying to load plugin class {class_name} from {path}")
        spec = importlib.util.spec_from_file_location("plugin", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_ = getattr(module, class_name)
        instance = class_()

        logger.debug(f"Successfully loaded class {class_name}")

        method = getattr(class_, "process", None)
        if not callable(method):
            raise Exception(
                f"Class {class_name} doesn't have process method which is required for plugins"
            )
        return instance

