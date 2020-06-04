import json

p1p2id = [json.dumps({
    "p1": 0.11,
    "p1a": 3.65,
    "p1b": 3.3,
    "p2": 1.49,
    "p2a": 3.23,
    "p2b": 2.9,
    "p2vmm": 1.69,

    "chip_id": "1e807186410061d8b6a00a000b4",
    "eeprom": 80,
    "chip_number": 88,
    "chip_address": 32,
    "uadc1": 72,
    "uadc2": 73
})]

mux1 = [json.dumps({
    "aux": {"U": 0.97, "R": 417788.64, "Runits": "OHM"},
    "pin1": {"U": 2.97, "R": 9.14, "Runits": "MOHM"},
    "pin2": {"U": 0.00, "R": 0.49, "Runits": "kOHM"},
    "pin3": {"U": 3.14, "R": 9.64, "Runits": "MOHM"},
    "pin5": {"U": 0.00, "R": 0.24, "Runits": "kOHM"},
    "pin11": {"U": 0.00, "R": 0.49, "Runits": "kOHM"},
    "pin13": {"U": 0.19, "R": 60.32, "Runits": "kOHM"},
    "pin14": {"U": 0.56, "R": 205.06, "Runits": "kOHM"},
    "pin17": {"U": 0.00, "R": 0.00, "Runits": "OHM"},
    "pin18": {"U": 0.02, "R": 5.89, "Runits": "kOHM"},
    "pin19": {"U": 0.56, "R": 205.06, "Runits": "kOHM"}
})]

mux3 = [json.dumps({
    "pin4": {"U": 3.25, "R": 62.00, "Runits": "MOHM"},
    "pin6": {"U": 3.25, "R": 60.12, "Runits": "kOHM"},
    "pin7": {"U": 3.25, "R": 60.12, "Runits": "MOHM"},
    "pin9": {"U": 3.25, "R": 62.00, "Runits": "kOHM"},
    "pin10": {"U": 1.54, "R": 0.88, "Runits": "kOHM"},
    "pin12": {"U": 0.90, "R": 0.38, "Runits": "kOHM"}
})]
