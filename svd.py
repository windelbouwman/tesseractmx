
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger('svd')


class Device:
    def __init__(self):
        self.peripherals = []
    
    def __repr__(self):
        return f'Device {self.name} with {len(self.peripherals)} peripherals'


class Peripheral:
    def __init__(self, name, description, address):
        self.name = name
        self.description = description
        self.address = address
        self.registers = []

    def __repr__(self):
        return f"Peripheral {self.name} @ 0x{self.address:X}"


class Register:
    def __init__(self, name, description, fields):
        self.name = name
        self.description = description
        self.fields = fields


class Field:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class SvdParser:
    def __init__(self, tree):
        self._root = tree.getroot()

    def parse_device(self):
        device_node = self._root
        device = Device()
        device.peripherals = [
            self.parse_peripheral(peripheral_node)
            for peripheral_node in device_node.findall("./peripherals/peripheral")
        ]
        device.name = self.get_text(device_node, "./name")
        device.description = self.get_text(device_node, "./description")
        logger.info('Read %s', device)
        return device

    def parse_peripheral(self, peripheral_node):
        # print(peripheral_node)
        name = self.get_text(peripheral_node, "./name")
        description = self.get_text(peripheral_node, "./description")
        address = self.get_int(peripheral_node, './baseAddress')
        peripheral = Peripheral(name, description, address)
        peripheral.registers = [
            self.parse_register(register_node)
            for register_node in peripheral_node.findall("./registers/register")
        ]
        # print(peripheral)
        logger.debug('Read %s', peripheral)
        return peripheral

    def parse_register(self, register_node):
        # Load data:
        name = self.get_text(register_node, './name')
        description = self.get_text(register_node, './description')
        address_offset = self.get_int(register_node, './addressOffset')
        size = self.get_int(register_node, './size')

        # Construct data:
        fields = [
            self.parse_field(field_node) for field_node in register_node.findall('./fields/field')

        ]
        register = Register(name, description, fields)
        register.address_offset = address_offset
        register.size = size
        return register

    def parse_field(self, field_node):
        name = self.get_text(field_node, './name')
        description = self.get_text(field_node, './description')
        field = Field(name, description)
        return field

    def get_text(self, node, tag, default=""):
        node = node.find(tag)
        if node is not None:
            # print(node, tag)
            return node.text
        else:
            return default
    
    def get_int(self, node, tag):
        """ Read an int. """
        node = node.find(tag)
        if node is None:
            raise ValueError(f'Tag {tag} not found.')
        text = node.text.lower()
        if 'x' in text:
            value = int(text, 16)
        else:
            value = int(text)
        return value


def read_svd(filename):
    logger.info('Reading %s', filename)
    tree = ET.parse(filename)
    parser = SvdParser(tree)
    return parser.parse_device()


def main():
    logging.basicConfig(level=logging.DEBUG)
    filename = "STM32F7_svd/STM32F7_svd_V1.4/STM32F7x7.svd"
    read_svd(filename)


if __name__ == '__main__':
    main()

