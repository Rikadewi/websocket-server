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
OPCODE_TEXT_FRAME = 0x1
OPCODE_BINARY_FRAME = 0x2
OPCODE_CLOSE_CONNECTION = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xA

FIN = 128


def createFrame(fin, opcode, payload_len, payload_data):
    #fin dalam bentuk integer
    #payload_len dalam bentuk integer
    #payload_data dalam bentuk bytearrat
    frame = bytearray()
    first_byte = fin + opcode
    frame.append(first_byte)
    
    if (payload_len < 0):
        print("Invalid lenght")
        second_byte = 0
        frame.append(second_byte)
    elif (payload_len <= 125):
        second_byte = payload_len
        frame.append(second_byte)
    elif (payload_len < 2**16):
        second_byte = 126
        frame.append(second_byte)
        print(payload_len)
        frame.append(payload_len >> 8)
        frame.append(payload_len & 0xff)
    else:
        second_byte = 127
        frame.append(second_byte)
        frame.append(payload_len >> 56)
        frame.append((payload_len >> 48)& 0xff)
        frame.append((payload_len >> 40)& 0xff)
        frame.append((payload_len >> 32)& 0xff)
        frame.append((payload_len >> 24)& 0xff)
        frame.append((payload_len >> 16)& 0xff)
        frame.append((payload_len >> 8)& 0xff)
        frame.append(payload_len & 0xff)


    frame += payload_data

    return frame


def unmask(masking_key, payload_data):
    result = bytearray()
    for i in range(0, len(payload_data)):
        part = payload_data[i] ^ masking_key[i % 4]
        result.append(part)
    return result


def parseFrame(frame):
    fin = frame[0] & 0x80
    opcode = frame[0] & 0x0f
    mask = frame[1] & 0x80
    payload_len = frame[1] & 0x7f
    idx = 2

    if (payload_len == 126):
        idx = idx + 2
        payload_len = frame[2:idx]
    elif (payload_len == 127):
        idx = idx + 8
        payload_len = frame[2:idx]
    print('payload len:', payload_len)

    if (mask):
        masking_key = frame[idx:idx + 4]
        payload_data = frame[idx + 4:]  #payload data masih dalam mask
        payload_data = unmask(masking_key, payload_data)
    else:
        masking_key = 0
        payload_data = frame[idx:]  #payload data masih dalam mask

    return fin, opcode, mask, payload_len, masking_key, payload_data


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
    def handle(self):
        data = self.request.recv(1024)
        data = (data.decode('utf-8'))

        sp = data.split('\r\n')

        temp = dict(item.split(": ") for item in sp[1:len(sp) - 2])
        temp = {k.lower(): v for k, v in temp.items()}
        # print(temp['connection'], temp['upgrade'])

        if ('connection' in temp and 'upgrade' in temp
                and 'sec-websocket-key' in temp):
            if (temp['connection'].lower() == 'upgrade'
                    and temp['upgrade'].lower() == 'websocket'):
                key = temp['sec-websocket-key']
                response = make_handshake_response(key)
                self.request.sendall(bytearray(response, encoding='utf-8'))

                while (True):
                    data = self.request.recv(1024)
                    # print(data)
                    fin, opcode, mask, payload_len, masking_key, payload_data = parseFrame(
                        data)
                    print(fin)
                    print(opcode)
                    print(mask)
                    print(payload_len)
                    print(payload_data.decode('utf-8'))
                    # break
                    if payload_len > 6:
                        if (payload_data.decode('utf-8')[0:6] == '!echo '):
                            phrase = payload_data[6:]
                            print(phrase)
                            response = createFrame(fin, OPCODE_TEXT_FRAME,
                                                   payload_len - 6, phrase)
                            self.request.sendall(response)
                        elif (payload_data.decode('utf-8')[0:11] ==
                              '!submission'):
                            print('wakgeng')
                            with open('submit.zip', 'rb') as zipfile:
                                filebin = zipfile.read()

                                response = createFrame(FIN,
                                                       OPCODE_BINARY_FRAME,
                                                       len(filebin), filebin)
                                print("create")
                                print(FIN)
                                print(OPCODE_BINARY_FRAME)
                                print(len(filebin))

                                fin, opcode, mask, payload_len, masking_key, payload_data = parseFrame(
                                    response)
                                print('parse')
                                print(fin)
                                print(opcode)
                                print(mask)
                                print(payload_len)
                                self.request.sendall(response)
                                # filebin.close()
                            # f = open('submit.zip', "rb")
                            # f_bin = f.read()
                            # f.close()
                            # w = open('a.zip', 'wb')
                            # w.write(f_bin)
                            # w.close()

                    break

            else:
                print('Error')
        else:
            print('wrong request header')