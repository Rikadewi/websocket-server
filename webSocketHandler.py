#Tugas Besar II Jarkom
import hashlib
import base64
import socketserver

'''
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
'''
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

OPCODE_CONTINUATION_FRAME = 0x0
OPCODE_TEXT_FRAME         = 0x1
OPCODE_BINARY_FRAME       = 0x2
OPCODE_CLOSE_CONNECTION   = 0x8
OPCODE_PING               = 0x9
OPCODE_PONG               = 0xA

def createFrame(fin, rsv1, rsv2, rsv3, mask, payload_len, masking_key, payload_data):
    frame = bytearray()
    frame.append(fin | rsv1)
    frame.append(rsv2)
    frame.append(rsv3)
    frame.append(mask)
    frame.append(payload_len)
    frame.append(masking_key)
    frame.append(payload_data)
    return frame

def parseFrame(frame):
    # fin = int.from_bytes(frame[0],byteorder=big)
    fin = frame[0] & 0x80
    opcode = frame[0] & 0x0f


def make_handshake_response(key):
    return \
      'HTTP/1.1 101 Switching Protocols\r\n'\
      'Upgrade: websocket\r\n'              \
      'Connection: Upgrade\r\n'             \
      'Sec-WebSocket-Accept: %s\r\n'        \
      '\r\n' % calculate_response_key(key)

def calculate_response_key(key):
    hashed = key.encode() + GUID.encode()
    hashed = hashlib.sha1(hashed)
    response_key = base64.b64encode(hashed.digest()).strip()
    return response_key.decode('ASCII')

class webSocketHandler(socketserver.BaseRequestHandler):
    # @classmethod
    def handle(self):
        data = self.request.recv(1024)
        data = (data.decode('utf-8'))

        sp = data.split('\r\n')

        temp = dict(item.split(": ") for item in sp[1:len(sp)-2])
        temp =  {k.lower(): v for k, v in temp.items()}
        # print(temp['connection'], temp['upgrade'])

        if('connection' in temp and 'upgrade' in temp and 'sec-websocket-key' in temp):
            if(temp['connection'].lower()=='upgrade' and temp['upgrade'].lower()=='websocket'):
                key = temp['sec-websocket-key']
                response = make_handshake_response(key)
                self.request.sendall(bytearray(response,encoding='utf-8'))

                while(True):
                    data = self.request.recv(1024)
                    print(data)
                    break
            else:
                print('Error')
        else:
            print('wrong request header')
