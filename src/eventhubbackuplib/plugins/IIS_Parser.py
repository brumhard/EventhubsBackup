from pygrok import Grok
import json

# from .parser_plugin import Parser_Plugin


class IIS_Parser:
    def process(self, data_to_process) -> dict:
        pattern = "%{TIMESTAMP_ISO8601:log_timestamp} %{NOTSPACE:sitename} %{WORD:cs_method} %{URIPATH:cs_uri_stem} %{NOTSPACE:cs_uri_query} %{NUMBER:s_port} %{NOTSPACE:cs_username} %{IPORHOST:c_ip} %{NOTSPACE:cs_useragent} %{NOTSPACE:cs_cookie} %{NOTSPACE:cs_referer} %{IPORHOST:cs_host} %{NUMBER:sc_status} %{NUMBER:sc_substatus} %{NUMBER:sc_win32_status} %{NUMBER:sc_bytes} %{NUMBER:cs_bytes} %{NUMBER:time_taken}"
        grok = Grok(pattern)
        parsed_data = grok.match(data_to_process)
        dict_for_db = {
            "time": parsed_data["log_timestamp"],
            "status_code": parsed_data["sc_status"],
            "outbound_data": parsed_data["sc_bytes"],
            "inbound_data": parsed_data["cs_bytes"],
            "time_taken": parsed_data["time_taken"],
            "raw_data": json.dumps(parsed_data),
        }
        return dict_for_db

