import base64
from byte_buffer import ByteBuffer
from urllib.parse import unquote


def decode_avatar(avatar: str) -> dict:
    def decode_layer(buffer: ByteBuffer) -> Union[dict, None]:
        layer_data = {}

        if buffer.read_byte() == 10:
            if buffer.read_byte() == 7:
                for _ in range(3):
                    buffer.read_byte()

            buffer.read_short()

            layer_data["id"] = buffer.read_short()
            layer_data["scale"] = buffer.read_float()
            layer_data["angle"] = buffer.read_float()
            layer_data["x"] = buffer.read_float()
            layer_data["y"] = buffer.read_float()
            layer_data["flipX"] = buffer.read_boolean()
            layer_data["flipY"] = buffer.read_boolean()
            layer_data["color"] = buffer.read_int()

            return layer_data

        return None

    if avatar == "":
        return {"layers": [], "bc": 4492031}

    byte_buffer = ByteBuffer(base64.b64decode(unquote(avatar)))
    avatar_data = {"layers": [], "bc": 0}

    byte_buffer.read_padding()

    shapes_count = (int(byte_buffer.read_byte()) - 1) // 2
    wtf_chaz = byte_buffer.read_byte()

    while wtf_chaz != 1:
        if wtf_chaz == 3:
            byte_buffer.read_byte()
        elif wtf_chaz == 5:
            byte_buffer.read_byte()
            byte_buffer.read_byte()

        wtf_chaz = byte_buffer.read_byte()

    for _ in range(shapes_count):
        layer = decode_layer(byte_buffer)

        if layer:
            avatar_data["layers"].append(layer)

    avatar_data["bc"] = byte_buffer.read_int()

    return avatar_data
