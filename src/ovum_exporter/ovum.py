
from ovum_exporter import constants
from ovum_exporter.modbus import read_register
from ovum_exporter.utils import load_json

descriptor = None
units = None
typeMap = None

def init_ovum():
    global descriptor, units, typeMap
    descriptor = load_json(constants.JSON_DESCRIPTOR)
    units = load_json(constants.JSON_UNITS)
    typeMap = load_json(constants.JSON_TYPEMAP)

def read_ovum(client, register_address, slave):
    read_count = 10
    lang = 'en'

    response, error = read_register(client, register_address, read_count, slave)
    if not error:
        address_hex = response[0]['address_hex']
        address = response[0]['address']
        parameter = f"{response[6]['char1']}{response[6]['char2']}{response[7]['char1']}{response[7]['char2']}"
        is_not_menu = (int(response[5]['bin'][0], 2) == 0)
        is_readonly = (int(response[5]['bin'][1], 2) == 0) if is_not_menu else ""
        if is_not_menu:
            value = int(f"{response[1]['hex']}{response[0]['hex']}", 16)
            if value & 0x80000000:
                value = -((value ^ 0xFFFFFFFF) + 1)
        else:
            value = ""
        precision = int(response[4]['bin'][:4], 2) if is_not_menu else ""
        value_float = round(value * 10 ** (-precision), precision) if is_not_menu else ""
        unit_id = int(response[4]['bin'][-7:], 2) if is_not_menu else ""
        unit_text = units.get(f'{unit_id}', {}).get('expected', '') if is_not_menu else ""
        multi_id = response[9]['UInt16'] if (is_not_menu and (response[9]['UInt16'] != "0")) else ""
        if is_not_menu:
            min_val = int(f"{response[2]['hex']}", 16)
            if min_val > 32767:
                min_val -= 65536
            if (f"{response[2]['bin']}" != "1000000000000000") and (f"{response[2]['bin']}" != "0000000000000000"):
                min_val = round(min_val * 10 ** (-precision), precision)
            max_val = int(f"{response[3]['hex']}", 16)
            if max_val & 0x80000000:
                max_val = -((max_val ^ 0xFFFFFFFF) + 1)
            if (f"{response[3]['bin']}" != "0111111111111111") and (f"{response[3]['bin']}" != "1111111111111111"):
                max_val = round(max_val * 10 ** (-precision), precision)
        else:
            min_val = ""
            max_val = ""
        descriptor_id = response[8]['UInt16']
        matching_item = next((item for item in descriptor if f"{item['iddescriptor']}" == descriptor_id),None)
        descriptor_text = matching_item.get("tlangalphakey", {}).get(lang, "") if matching_item else ""
        if (multi_id != ""):
            for item in typeMap:
                if f"{multi_id}" in item:
                    for tvalue in item[f"{multi_id}"]["tvalues"]:
                        if tvalue["in_INPUT"] == value:
                            value_float = tvalue["alphakey"][lang]
                            break
                    else:
                        value_float = ""
                    break
            else:
                value_float = ""
        return {
            "address_hex": address_hex,
            "address": address,
            "parameter": parameter,
            "value": value,
            "precision": precision,
            "value_float": value_float,
            "unit_text": unit_text,
            "unit_id": unit_id,
            "multi_id": multi_id,
            "min_val": min_val,
            "max_val": max_val,
            "is_readonly": is_readonly,
            "is_not_menu": is_not_menu == False,
            "descriptor_id": descriptor_id,
            "descriptor_text": descriptor_text
        }
    else:
        print(f"error: {error}")
        return None
    