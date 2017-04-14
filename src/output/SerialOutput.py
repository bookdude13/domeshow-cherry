import sys
import os
sys.path.append('libs')

from bitstring import Bits as Bits
from crc16 import crc16pure as crc16
import serial
import time
from output.CtsThread import CtsThread as CtsThread


class SerialOutput:
    def __init__(self, port, baud=115200):
        self._port = port
        self._output = serial.Serial(port=port, baudrate=baud)
        self._output.write(b'B')  # Because Xbee
        #self._cts = CtsThread(self._output)  # Because Xbee is stupid with CTS

    def close(self, message):
        print('Closing SerialOutput {0}: {1}'.format(self._port, message))
        self._output.close()

    def send(self, data):
        packet = _create_packet(_patch(data))
        #for i in range(3):
        self._output.write(packet)
            #time.sleep(0.15)

def _create_packet(data):
    magic = bytearray([0xde, 0xad, 0xbe, 0xef])
    length = Bits(uint=144, length=16).tobytes()
    payload = Bits().join([Bits(uint=x, length=8) for x in data])
    patched_str = payload.tobytes()
    crc = Bits(uint=crc16.crc16xmodem(patched_str), length=16)
    packet = Bits().join([magic, length, payload, crc])
    return packet.tobytes()

def _patch(data):
    patched = [0] * 144
    patched[0] = data[0]
    patched[1] = data[1]
    patched[2] = data[2]
    patched[3] = data[57]
    patched[4] = data[58]
    patched[5] = data[59]
    patched[6] = data[87]
    patched[7] = data[88]
    patched[8] = data[89]
    patched[9] = data[60]
    patched[10] = data[61]
    patched[11] = data[62]
    patched[12] = data[30]
    patched[13] = data[31]
    patched[14] = data[32]
    patched[16] = data[6]
    patched[17] = data[7]
    patched[18] = data[8]
    patched[19] = data[33]
    patched[20] = data[34]
    patched[21] = data[35]
    patched[22] = data[63]
    patched[23] = data[64]
    patched[24] = data[65]
    patched[25] = data[66]
    patched[26] = data[67]
    patched[27] = data[68]
    patched[28] = data[36]
    patched[29] = data[37]
    patched[30] = data[38]
    patched[32] = data[12]
    patched[33] = data[13]
    patched[34] = data[14]
    patched[35] = data[39]
    patched[36] = data[40]
    patched[37] = data[41]
    patched[38] = data[69]
    patched[39] = data[70]
    patched[40] = data[71]
    patched[41] = data[72]
    patched[42] = data[73]
    patched[43] = data[74]
    patched[44] = data[42]
    patched[45] = data[43]
    patched[46] = data[44]
    patched[48] = data[18]
    patched[49] = data[19]
    patched[50] = data[20]
    patched[51] = data[45]
    patched[52] = data[46]
    patched[53] = data[47]
    patched[54] = data[75]
    patched[55] = data[76]
    patched[56] = data[77]
    patched[57] = data[78]
    patched[58] = data[79]
    patched[59] = data[80]
    patched[60] = data[48]
    patched[61] = data[49]
    patched[62] = data[50]
    patched[64] = data[24]
    patched[65] = data[25]
    patched[66] = data[26]
    patched[67] = data[51]
    patched[68] = data[52]
    patched[69] = data[53]
    patched[70] = data[81]
    patched[71] = data[82]
    patched[72] = data[83]
    patched[73] = data[84]
    patched[74] = data[85]
    patched[75] = data[86]
    patched[76] = data[54]
    patched[77] = data[55]
    patched[78] = data[56]
    patched[80] = data[105]
    patched[81] = data[106]
    patched[82] = data[107]
    patched[83] = data[117]
    patched[84] = data[118]
    patched[85] = data[119]
    patched[86] = data[114]
    patched[87] = data[115]
    patched[88] = data[116]
    patched[89] = data[111]
    patched[90] = data[112]
    patched[91] = data[113]
    patched[92] = data[108]
    patched[93] = data[109]
    patched[94] = data[110]
    patched[96] = data[3]
    patched[97] = data[4]
    patched[98] = data[5]
    patched[99] = data[90]
    patched[100] = data[91]
    patched[101] = data[92]
    patched[102] = data[93]
    patched[103] = data[94]
    patched[104] = data[95]
    patched[105] = data[9]
    patched[106] = data[10]
    patched[107] = data[11]
    patched[112] = data[15]
    patched[113] = data[16]
    patched[114] = data[17]
    patched[115] = data[96]
    patched[116] = data[97]
    patched[117] = data[98]
    patched[118] = data[99]
    patched[119] = data[100]
    patched[120] = data[101]
    patched[121] = data[21]
    patched[122] = data[22]
    patched[123] = data[23]
    patched[128] = data[27]
    patched[129] = data[28]
    patched[130] = data[29]
    patched[131] = data[102]
    patched[132] = data[103]
    patched[133] = data[104]

    return patched
