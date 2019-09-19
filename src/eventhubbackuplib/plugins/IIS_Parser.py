from pygrok import Grok
import json
from typing import Dict, Any
import logging

# from .parser_plugin import Parser_Plugin
logger = logging.getLogger(__name__)


class IIS_Parser:
    """Plugin to parse IIS style messages

    This class implemnts the Parser_Plugin abstract class
    """

    def process(self, data_to_process: str) -> Dict[str, Any]:
        """Transfrom a string in IIS logging style

        sample input:
        2019-09-11 02:02:45 WEBSITE-LIDL-ACCOUNT-PROD-WE GET / X-ARR-LOG-ID=b7fea7b7-7913-43a9-87a6-59bcca58e4b7 443 - 51.105.161.182 - - - website-lidl-account-prod-we.lidl-account-ase-prod-we.p.azurewebsites.net 200 0 0 6180 1065 15

        Uses grok pattern to parse the string.

        Args:
            data_to_process: str containing the IIS log.
        """
        
        pattern = "%{TIMESTAMP_ISO8601:log_timestamp} %{NOTSPACE:sitename} %{WORD:cs_method} %{URIPATH:cs_uri_stem} %{NOTSPACE:cs_uri_query} %{NUMBER:s_port} %{NOTSPACE:cs_username} %{IPORHOST:c_ip} %{NOTSPACE:cs_useragent} %{NOTSPACE:cs_cookie} %{NOTSPACE:cs_referer} %{IPORHOST:cs_host} %{NUMBER:sc_status} %{NUMBER:sc_substatus} %{NUMBER:sc_win32_status} %{NUMBER:sc_bytes} %{NUMBER:cs_bytes} %{NUMBER:time_taken}"
        logger.debug(f"Parsing: {data_to_process}")
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

