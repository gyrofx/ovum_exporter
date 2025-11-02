import pymodbus.client as modbusClient
from pymodbus.exceptions import ModbusIOException

# Connect to Modbus TCP
def connect_to_modbusTCP(host, port):
    client = modbusClient.ModbusTcpClient(host=host, port=port)
    try:
        client.connect()
        return client, client.is_socket_open()
    except ModbusIOException as e:
        print(f"Failed to connect to tcp host: {host}")
        print("Error:", e)
        return None, False

# Connect to Modbus RTU
def connect_to_modbusRTU(comport, baudrate, parity, stopbits):
    client = modbusClient.ModbusSerialClient(port=comport, baudrate=baudrate, parity=parity, stopbits=stopbits)
    try:
        client.connect()
        return client, client.is_socket_open()
    except ModbusIOException as e:
        print(f"Failed to connect to rtu port: {comport}")
        print("Error:", e)
        return None, False
    

def read_register(client, address, count, slave):
    response = []
    try:
        register_content = client.read_holding_registers(address, count, slave)
        if register_content.isError():
            return response, True
        else:
            for i in range(0, len(register_content.registers)):
                hex = format(register_content.registers[i], '04X')
                dec_unsigned = int(hex, 16)
                if dec_unsigned & 0x8000:
                    dec_signed = -((dec_unsigned^0xFFFF)+1)
                else:
                    dec_signed = dec_unsigned
                byte1 = int(hex[:2], 16)
                byte2 = int(hex[-2:], 16)
                char1 = chr(byte1) if (31 < byte1 < 127) and (31 < byte2 < 127) else ""
                char2 = chr(byte2) if (31 < byte1 < 127) and (31 < byte2 < 127) else ""
                bin = format(register_content.registers[i], '016b')
                address_dec = address+i
                data = {"address_hex": f"{address_dec:#0{6}x}", "address": f"{address +i}", "hex": f"{hex}", "byte1": f"{byte1}", "byte2": f"{byte2}", "UInt16": f"{dec_unsigned}", "Int16": f"{dec_signed}", "char1": f"{char1}", "char2": f"{char2}", "bin": f"{bin}"}
                response.append(data)
            return response, False
    except ModbusIOException as e:
        return response, True