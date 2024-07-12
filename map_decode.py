import base64
from lzstring import LZString


def decode_bonk_map(encoded_map) -> dict:
    map_data = {}
    reader = ByteReader(base64.b64decode(LZString.decompressFromEncodedURIComponent(encoded_map)))

    map_data["physics"] = {}
    physics = map_data["physics"]
    map_data["version"] = reader.read_short()

    if map_data["version"] > 61:
        raise ValueError("Future map version, please refresh page")

    map_data["settings"] = {
        "re": reader.read_boolean(),
        "nc": reader.read_boolean()
    }

    if map_data["version"] >= 3:
        map_data["settings"]["pq"] = reader.read_short()

    if 4 <= map_data["version"] <= 12:
        map_data["settings"]["gd"] = reader.read_short()
    elif map_data["version"] >= 13:
        map_data["settings"]["gd"] = reader.read_float()

    if map_data["version"] >= 9:
        map_data["settings"]["fl"] = reader.read_boolean()

    map_data["metadata"] = {
        "rxn": reader.read_utf(),
        "rxa": reader.read_utf(),
        "rxid": reader.read_uint(),
        "rxdb": reader.read_short(),
        "n": reader.read_utf(),
        "a": reader.read_utf()
    }

    if map_data["version"] >= 10:
        map_data["metadata"]["vu"] = reader.read_uint()
        map_data["metadata"]["vd"] = reader.read_uint()

    if map_data["version"] >= 4:
        cr_count = reader.read_short()
        map_data["metadata"]["cr"] = [reader.read_utf() for _ in range(cr_count)]

    if map_data["version"] >= 5:
        map_data["metadata"]["mo"] = reader.read_utf()
        map_data["metadata"]["dbid"] = reader.read_int()

    if map_data["version"] >= 7:
        map_data["metadata"]["pub"] = reader.read_boolean()

    if map_data["version"] >= 8:
        map_data["metadata"]["dbv"] = reader.read_int()

    physics["ppm"] = reader.read_short()

    bro_count = reader.read_short()
    physics["bro"] = [reader.read_short() for _ in range(bro_count)]

    # Read shapes
    shape_count = reader.read_short()
    physics["shapes"] = []

    for _ in range(shape_count):
        shape_type = reader.read_short()
        shape = {}

        if shape_type == 1:
            shape = {
                "type": "bx",
                "w": reader.read_double(),
                "h": reader.read_double(),
                "c": [reader.read_double(), reader.read_double()],
                "a": reader.read_double(),
                "sk": reader.read_boolean()
            }
        elif shape_type == 2:
            shape = {
                "type": "ci",
                "r": reader.read_double(),
                "c": [reader.read_double(), reader.read_double()],
                "sk": reader.read_boolean()
            }
        elif shape_type == 3:
            shape = {
                "type": "po",
                "s": reader.read_double(),
                "a": reader.read_double(),
                "c": [reader.read_double(), reader.read_double()],
            }

            vertex_count = reader.read_short()
            shape["v"] = [[reader.read_double(), reader.read_double()] for _ in range(vertex_count)]

        physics["shapes"].append(shape)

    # Read fixtures
    fixture_count = reader.read_short()
    physics["fixtures"] = []

    for _ in range(fixture_count):
        fixture = {
            "sh": reader.read_short(),
            "n": reader.read_utf(),
            "fr": reader.read_double(),
            "re": reader.read_double(),
            "de": reader.read_double(),
            "f": reader.read_uint(),
            "d": reader.read_boolean(),
            "np": reader.read_boolean()
        }

        if fixture["fr"] == float("inf"):
            fixture["fr"] = None

        fp_type = reader.read_short()
        fixture["fp"] = None if fp_type == 0 else (False if fp_type == 1 else True)

        if fixture["re"] == float("inf"):
            fixture["re"] = None

        if fixture["de"] == float("inf"):
            fixture["de"] = None

        if map_data["version"] >= 11:
            fixture["ng"] = reader.read_boolean()

        if map_data["version"] >= 12:
            fixture["ig"] = reader.read_boolean()

        physics["fixtures"].append(fixture)

    # Read bodies
    body_count = reader.read_short()
    physics["bodies"] = []

    for _ in range(body_count):
        body = {
            "s": {
                "type": reader.read_utf(),
                "n": reader.read_utf(),
                "fric": reader.read_double(),
                "fricp": reader.read_boolean(),
                "re": reader.read_double(),
                "de": reader.read_double(),
                "ld": reader.read_double(),
                "ad": reader.read_double(),
                "fr": reader.read_boolean(),
                "bu": reader.read_boolean(),
                "f_c": reader.read_short(),
                "f_1": reader.read_boolean(),
                "f_2": reader.read_boolean(),
                "f_3": reader.read_boolean(),
                "f_4": reader.read_boolean()
            },
            "p": [reader.read_double(), reader.read_double()],
            "a": reader.read_double(),
            "lv": [reader.read_double(), reader.read_double()],
            "av": reader.read_double(),
            "cf": {
                "x": reader.read_double(),
                "y": reader.read_double(),
                "ct": reader.read_double(),
                "w": reader.read_boolean()
            },
            "fx": []
        }

        if map_data["version"] >= 2:
            body["s"]["f_p"] = reader.read_boolean()

        if map_data["version"] >= 14:
            body["fz"] = {"on": reader.read_boolean()}

            if body["fz"]["on"]:
                body["fz"].update(
                    {
                        "x": reader.read_double(),
                        "y": reader.read_double(),
                        "d": reader.read_boolean(),
                        "p": reader.read_boolean(),
                        "a": reader.read_boolean()
                    }
                )

                if map_data["version"] >= 15:
                    body["fz"].update(
                        {
                            "t": reader.read_short(),
                            "cf": reader.read_double()
                        }
                    )

        fixture_count = reader.read_short()
        body["fx"] = [reader.read_short() for _ in range(fixture_count)]

        physics["bodies"].append(body)

    # Read spawns
    spawn_count = reader.read_short()
    map_data["spawns"] = []

    for _ in range(spawn_count):
        spawn = {
            "x": reader.read_double(),
            "y": reader.read_double(),
            "xv": reader.read_double(),
            "yv": reader.read_double(),
            "priority": reader.read_short(),
            "r": reader.read_boolean(),
            "f": reader.read_boolean(),
            "b": reader.read_boolean(),
            "gr": reader.read_boolean(),
            "ye": reader.read_boolean(),
            "n": reader.read_utf()
        }
        map_data["spawns"].append(spawn)

    # Read capture zones
    cap_zone_count = reader.read_short()
    map_data["capZones"] = []

    for _ in range(cap_zone_count):
        cap_zone = {
            "n": reader.read_utf(),
            "l": reader.read_double(),
            "i": reader.read_short()
        }
        if map_data["version"] >= 6:
            cap_zone["ty"] = reader.read_short()

        map_data["capZones"].append(cap_zone)

    # Read joints
    joint_count = reader.read_short()
    physics["joints"] = []

    for _ in range(joint_count):
        joint_type = reader.read_short()
        joint = {}

        if joint_type == 1:
            joint = {
                "type": "revolute",
                "d": {
                    "la": reader.read_double(),
                    "ua": reader.read_double(),
                    "mmt": reader.read_double(),
                    "ms": reader.read_double(),
                    "el": reader.read_boolean(),
                    "em": reader.read_boolean()
                },
                "aa": [reader.read_double(), reader.read_double()]
            }
        elif joint_type == 2:
            joint = {
                "type": "distance",
                "d": {
                    "fh": reader.read_double(),
                    "dr": reader.read_double()
                },
                "aa": [reader.read_double(), reader.read_double()],
                "ab": [reader.read_double(), reader.read_double()]
            }
        elif joint_type == 3:
            joint = {
                "type": "prismatic",
                "pax": reader.read_double(),
                "pay": reader.read_double(),
                "pa": reader.read_double(),
                "pf": reader.read_double(),
                "pl": reader.read_double(),
                "pu": reader.read_double(),
                "plen": reader.read_double(),
                "pms": reader.read_double()
            }
        elif joint_type == 4:
            joint = {
                "type": "line",
                "sax": reader.read_double(),
                "say": reader.read_double(),
                "sf": reader.read_double(),
                "slen": reader.read_double()
            }
        elif joint_type == 5:
            joint = {
                "type": "gear",
                "n": reader.read_utf(),
                "ja": reader.read_short(),
                "jb": reader.read_short(),
                "r": reader.read_double()
            }

        if joint_type != 5:
            joint.update(
                {
                    "ba": reader.read_short(),
                    "bb": reader.read_short(),
                    "d": {
                        "cc": reader.read_boolean(),
                        "bf": reader.read_double(),
                        "dl": reader.read_boolean()
                    }
                }
            )

        physics["joints"].append(joint)

    return map_data
