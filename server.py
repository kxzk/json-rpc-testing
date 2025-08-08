import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class RPCHandler(BaseHTTPRequestHandler):
    def rpc_add(self, a, b):
        return a + b

    def rpc_divide(self, dividend, divisor):
        if divisor == 0:
            raise ValueError("Division by zero is not allowed.")
        return dividend / divisor

    def rpc_echo(self, message, times=1):
        return message * times

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        request = json.loads(self.rfile.read(content_length))

        response = {
            "jsonrpc": "2.0",
            "id": request.get("id"),
        }

        try:
            method_name = f"rpc_{request['method']}"
            method = getattr(self, method_name, None)

            if not method:
                response["error"] = {"code": -32601, "message": "Method not found"}
            else:
                params = request.get("params", [])
                if isinstance(params, list):
                    result = method(*params)
                else:
                    result = method(**params)
                response["result"] = result
        except TypeError as e:
            response["error"] = {"code": -32602, "message": f"Invalid params: {str(e)}"}
        except Exception as e:
            response["error"] = {"code": -32603, "message": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), RPCHandler)
    print("JSON-RPC server running on http://localhost:8000")
    server.serve_forever()
