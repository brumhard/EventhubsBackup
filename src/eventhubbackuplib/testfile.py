from .plugins.plugin_loader import Plugin_Loader

parser_path = "C:\\Users\\brumhardadm\\Desktop\\tmp\\EventHubsBackup\\src\\plugins\\iis.py"
class_name = "IIS_Parser"


class_ = Plugin_Loader.load(class_name=class_name)

text_to_process = ""
data = class_.process(text_to_process)
print(data)


