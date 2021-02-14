import requests
import os

class NSPV:
    def __init__(self, node_addr=None, rpc_port=None, req_method=None, rpc_username=None, rpc_password=None):
        self.node_addr = node_addr or '127.0.0.1'
        self.rpc_port = rpc_port or 7771
        self.req_method = req_method or 'POST'
        self.rpc_username = rpc_username or ''
        self.rpc_password = rpc_password or ''
        self.req_auth = {
            'user': self.rpc_username,
            'pass': self.rpc_password
        }
        self.req_url = f'http://{self.node_addr}:{self.rpc_port}/'
        self.req_headers = {
            'content-type': 'text/plain;'
        }
        self.jsonrpc_ver = '2.0'
        self.rpc_req_id = 'curltest'


    def get_request_metadata(self):
        metadata = f'"jsonrpc": "{self.jsonrpc_ver}", "id": "{self.rpc_req_id}"'
        return metadata

    # communicates with daemon RPC
    def rpc_request(self, data_string=''):
        try:
            response = requests.post(self.req_url,
                                     headers=self.req_headers,
                                     data=data_string,
                                     auth=(self.rpc_username,
                                           self.rpc_password)
                                     )
            if response.ok:
                return response.json()
            else:
                return f"Failed with status code {response.status_code}! Message: {response.text}"
        except:
            return f"Error, nSPV is not running!"

    # Used to build parameter strings for RPC
    def build_data(self, method, params=None):
        clean_params = params or ""
        metadata = self.get_request_metadata()
        if isinstance(clean_params, list):
            data = f'{{{metadata}, "method":"{method}", "params":{clean_params}}}'
        else:
            data = f'{{{metadata}, "method":"{method}", "params":[{clean_params}]}}'
        return data

    def help(self):
        data = self.build_data("help")
        rpc_response = self.rpc_request(data)
        return rpc_response

    def login(self, wif: str):
        clean_wif = f'"{wif}"'
        data = self.build_data("login", clean_wif)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def logout(self):
        data = self.build_data("logout")
        rpc_response = self.rpc_request(data)
        return rpc_response

    def get_info(self, height: int=None):
        data = self.build_data("getinfo", height)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def add_node(self, ipAddress: str):
        clean_param = f'"{ipAddress}"'
        data = self.build_data("addnode", clean_param)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def set_language(self, language: str):
        clean_param = f'"{language}"'
        data = self.build_data("language", clean_param)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def broadcast_hex(self, hex: str):
        clean_hex = f'"{hex}"'
        data = self.build_data("broadcast", clean_hex)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def get_new_address(self, language: str=None):
        use_language = language or "english"
        cleaned_language = f'"{str.lower(use_language)}"'
        data = self.build_data("getnewaddress", cleaned_language)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def get_peer_info(self):
        data = self.build_data("getpeerinfo")
        rpc_response = self.rpc_request(data)
        return rpc_response

    def notarizations(self, height: int):
        clean_height = int(height)
        data = self.build_data("notarizations", clean_height)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def headers_proof(self, previousHeight: int, nextHeight: int):
        clean_previous_height = int(previousHeight)
        clean_next_height = int(nextHeight)
        clean_heights = [clean_previous_height, clean_next_height]
        data = self.build_data("hdrsproof", clean_heights)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def list_unspent(self, address: str=None, isCC: int=None, skipcount: int=None, filter: int=None):
        try:
            clean_address = str(address) or ""
            clean_isCC = int(isCC) or ""
            clean_skipcount = str(skipcount) or ""
            clean_filter = str(filter) or ""
            clean_params = [clean_address, clean_isCC, clean_skipcount, clean_filter]
            data = self.build_data("listunspent", clean_params)
            rpc_response = self.rpc_request(data)
            return rpc_response
        except:
            return "Error! Requirements: Address=str, isCC=int, skipcount=int, filter=int"

    def get_transaction(self, txid: str, vout: int, height: int):
        try:
            clean_txid = str(txid) or ""
            clean_vout = int(vout) or ""
            clean_height = int(height) or ""
            clean_params = [clean_txid, clean_vout, clean_height, ]
            data = self.build_data("gettransaction", clean_params)
            rpc_response = self.rpc_request(data)
            return rpc_response
        except:
            return "Error! Requirements: txid=str, vout=int, height=int"

    def list_transactions(self, address: str=None, isCC: int=None, skipcount: int=None, filter: int=None):
        try:
            clean_address = str(address) or ""
            clean_isCC = int(isCC) or ""
            clean_skipcount = str(skipcount) or ""
            clean_filter = str(filter) or ""
            clean_params = [clean_address, clean_isCC, clean_skipcount, clean_filter]
            data = self.build_data("listtransactions", clean_params)
            rpc_response = self.rpc_request(data)
            return rpc_response
        except:
            return "Error! Requirements: Address=str, isCC=int, skipcount=int, filter=int"

    def mempool(self, address: str=None, isCC: int=None, memfunc: int=None, txid: str=None, vout: int=None, evalcode: int=None, ccfunc: int=None):
        try:
            clean_address = str(address) or ""
            clean_isCC = int(isCC) or ""
            clean_memfunc = int(memfunc) or ""
            clean_txid = str(txid) or ""
            clean_vout = int(vout) or ""
            clean_evalcode = int(evalcode) or ""
            clean_ccfunc = int(ccfunc) or ""
            clean_params = [clean_address, clean_isCC, clean_memfunc, clean_txid, clean_vout, clean_evalcode, clean_ccfunc]
            data = self.build_data("mempool", clean_params)
            rpc_response = self.rpc_request(data)
            return rpc_response
        except:
            return "Error! Requirements: Address=str, isCC=int, memfunc=int, txid=str, vout=int, evalcode=int, ccfunc=int"

    def spend(self, address: str, amount:float):
        clean_params = [address, amount]
        data = self.build_data("spend", clean_params)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def spent_info(self, txid: str, vout: int):
        clean_params = [txid, vout]
        data = self.build_data("spentinfo", clean_params)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def tx_proof(self, txid: str, vout: int, height: int=None):
        clean_params = [txid, vout, height or ""]
        data = self.build_data("spentinfo", clean_params)
        rpc_response = self.rpc_request(data)
        return rpc_response

    def stop(self):
        data = self.build_data("stop")
        rpc_response = self.rpc_request(data)
        return rpc_response

    def build_coins_conf(self, source: str, coin: str, asset: str, fname: str, rpcport: int, mm2: int, p2p: int, magic: str, nspv: str):
        coins = {
                  "coin": f"{coin}",
                  "asset": f"{asset}",
                  "fname": f"{fname}",
                  "rpcport": rpcport,
                  "mm2": mm2,
                  "p2p": p2p,
                  "magic": f"{magic}",
                  "nSPV": f"{nspv}"
                }
        return coins

    def find_nspv_file(self):
        nspv_name = "nspv"
        path = "/home"
        for root, dirs, files in os.walk(path):
            if nspv_name in files:
                return os.path.join(root, nspv_name)

    def get_docs_link(self):
        data = "https://docs.komodoplatform.com/basic-docs/smart-chains/smart-chain-setup/nspv.html#introduction"
        return data

    def get_nspv_github_link(self):
        data = "https://github.com/KomodoPlatform/libnspv"
        return data