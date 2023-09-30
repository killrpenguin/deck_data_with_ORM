import requests


class MasterProxyList:
    def __init__(self):
        self.proxy_link = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        self.get_list()


    def get_list(self):
        with requests.get(self.proxy_link) as MasterProxyList:
            with open("MasterProxyList", "x") as file:
                proxies = MasterProxyList.text.strip().split('\n')
                proxies = [file.write(f"http://{item}\n") for item in proxies]
                return None


class MasterUserAgents:
    def __init__(self):
        self.UA_link = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"
        self.get_useragents()

    def get_useragents(self):
        with requests.get(self.UA_link) as Master_UserAgents_List:
            with open("Master_User_Agents", "x") as file:
                UA_list = Master_UserAgents_List.text.strip().split('\n')
                UA_list = [file.write(f"{item}\n") for item in UA_list]
                return None
