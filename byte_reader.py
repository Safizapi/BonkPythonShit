import struct


class ByteReader:
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data
        self.position = 0

    def read_boolean(self) -> bool:
        return self.read_byte() != 0

    def read_byte(self) -> bytes:
        value = struct.unpack("B", self.data[self.position:self.position + 1])[0]
        self.position += 1
        return value

    def read_short(self) -> int:
        value = struct.unpack(">h", self.data[self.position:self.position + 2])[0]
        self.position += 2
        return value

    def read_int(self) -> int:
        value = struct.unpack(">i", self.data[self.position:self.position + 4])[0]
        self.position += 4
        return value

    def read_uint(self) -> int:
        value = struct.unpack(">I", self.data[self.position:self.position + 4])[0]
        self.position += 4
        return value

    def read_float(self) -> float:
        value = struct.unpack(">f", self.data[self.position:self.position + 4])[0]
        self.position += 4
        return value

    def read_double(self) -> float:
        value = struct.unpack(">d", self.data[self.position:self.position + 8])[0]
        self.position += 8
        return value

    def read_utf(self) -> str:
        length = self.read_short()
        value = self.data[self.position:self.position + length].decode("utf-8")
        self.position += length
        return value
