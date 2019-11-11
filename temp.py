# temp = bytearray()
# firstbyte = 128 + 0x1
# firstbyte += 300
# # temp.append(128)
# temp.append(firstbyte)
# print(temp)

import webSocketHandler

coba = 'ini cuman data pendek'

temp = webSocketHandler.createFrame(128, 0x1, 21, coba.encode('utf-8'))
print(coba.encode('utf-8'))
print(temp)
fin, opcode, mask, payload_len, masking_key, payload_data = webSocketHandler.parseFrame(
    temp)

print(fin)
print(opcode)
print(mask)
print(payload_len)
print(payload_data.decode('utf-8'))
