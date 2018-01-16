from websocket import create_connection
import json, base64, hashlib, urlparse, hmac, time

###
# websocket-apikey-auth-test.py
#
# Reference Python implementation for authorizing with websocket.
# See https://www.bitmex.com/app/wsAPI for more details, including a list
# of methods.
###

# These are not real keys - replace them with your keys.
API_KEY = "CfwQ4SZ6gM_t6dIy1bCLJylX"
API_SECRET = "f9XOPLacPCZJ1dvPzN8B6Et7nMEaPGeomMSHk8Cr2zD4NfCY"

# Switch these comments to use testnet instead.
# BITMEX_URL = "wss://testnet.bitmex.com"
BITMEX_URL = "wss://www.bitmex.com"

VERB = "GET"
ENDPOINT = "/realtime"
def main():
    """Authenticate with the BitMEX API & request account information."""
    test_with_message()
    test_with_querystring()
def test_with_message():
    # This is up to you, most use microtime but you may have your own scheme so long as it's increasing
    # and doesn't repeat.
    nonce = int(round(time.time() * 1000))
    # See signature generation reference at https://www.bitmex.com/app/apiKeys
    signature = bitmex_signature(API_SECRET, VERB, ENDPOINT, nonce)

    # Initial connection - BitMEX sends a welcome message.
    ws = create_connection(BITMEX_URL + ENDPOINT)
    print("Receiving Welcome Message...")
    result = ws.recv()
    print("Received '%s'" % result)

    # Send API Key with signed message.
    request = {"op": "authKey", "args": [API_KEY, nonce, signature]}
    ws.send(json.dumps(request))
    print("Sent Auth request")
    result = ws.recv()
    print("Received '%s'" % result)

    # Send a request that requires authorization.
    request = {"op": "subscribe", "args": "position"}
    ws.send(json.dumps(request))
    print("Sent subscribe")
    result = ws.recv()
    print("Received '%s'" % result)
    result = ws.recv()
    print("Received '%s'" % result)

    ws.close()