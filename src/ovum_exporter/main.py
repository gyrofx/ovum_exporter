import argparse

from ovum_exporter import constants
from ovum_exporter.read_exporter_values import read_exporter_values
from ovum_exporter.modbus import connect_to_modbusRTU, connect_to_modbusTCP
from ovum_exporter.ovum import init_ovum


# Initial Setup, call-arguments, load json-files
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=str, default=constants.METHOD_TCP, help='How to connect: TCP or RTU')
    parser.add_argument('slave', type=int, default=constants.DEFAULT_SLAVE, help='The Modbus-Address (Slave)')
    parser.add_argument('--host', type=str, default=constants.DEFAULT_HOST, help='The IP address of the Modbus TCP host')
    parser.add_argument('--port', type=int, default=constants.DEFAULT_PORT, help='The TCP-Port of the Modbus TCP host')
    parser.add_argument('--comport', type=str, default=constants.DEFAULT_COMPORT, help='The COM Port Device')
    parser.add_argument('--baudrate', type=int, default=constants.DEFAULT_BAUDRATE, help='Baudrate for RTU Connection')
    parser.add_argument('--parity', type=str, default=constants.DEFAULT_PARITY, help='Parity for RTU Connection')
    parser.add_argument('--stopbits', type=int, default=constants.DEFAULT_STOPBITS, help='Stopbits for RTU Connection')
    parser.add_argument('--lang', type=str, default=constants.DEFAULT_LANG, help='Language Selector (de, en, ...)')
    parser.add_argument('--start_address', type=int, default=constants.DEFAULT_START_ADDRESS, help='Start address of the register')
    parser.add_argument('--stop_address', type=int, default=constants.DEFAULT_STOP_ADDRESS, help='Stop address of the register')
    parser.add_argument('--dump', action='store_true', help='Loop through addresses and dump content')
    parser.add_argument('--csv', action='store_true', help='Output is in CSV-Format')
    parser.add_argument('--hass', action='store_true', help='Create Home Assistant YAML for sensors')
    parser.add_argument('--min', action='store_true', help='Create minimal output')
    parser.add_argument('--noerror', action='store_true', help='Skip addresses with error and do not print')
    parser.add_argument('--output', type=str, default=None, help='Write output to a file')
    parser.add_argument('--dev', action='store_true', help='Debugging and test parameter')
    return parser



# Main function to call after script starts
def main():
    global args, client, descriptor, units, typeMap

    args = init_parser().parse_args()
    init_ovum()
    print(args)
    print(read_exporter_values)

    # separator = ';' if args.csv else '\t'

    if args.method == constants.METHOD_RTU:
        client, is_connected = connect_to_modbusRTU(args.comport, args.baudrate, args.parity, args.stopbits)
    else:
        client, is_connected = connect_to_modbusTCP(args.host, args.port)

    if not is_connected:
        print("Connection failed, exiting...")
        return

    values = read_exporter_values(client, args.slave)
    print(values)
    
    if client: client.close()

# Main Call
if __name__ == "__main__":
    main()
