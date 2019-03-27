import logging

import jinja2
from svd import read_svd




cpp_template = """

/*
  Autogenerated code!
*/

namespace {{ device.name }} {

    {% for peripheral in device.peripherals %}
    namespace {{ peripheral.name }} {  // {{ peripheral.description }}

        {% for register in peripheral.registers %}

        uint32_t* pointer_{{ register.name }} = {{ peripheral.address + register.address_offset }};
        {% endfor %}

        {% for register in peripheral.registers %}
        namespace {{ register.name }} { // {{ register.description }}
            {% for field in register.fields %}
            namespace {{ field.name }} {  // {{ field.description }}
                void set_value() {
                    // TODO
                }

                int get_value() {
                    return 0;
                }
            }
            {% endfor %}
        }
        {% endfor %}
    }
    {% endfor %}
}

"""

def gen_code(device):
    template = jinja2.Template(cpp_template)
    text = template.render(device=device)
    with open('c_gen.cpp', 'w') as f:
        print(text, file=f)


def main():
    logging.basicConfig(level=logging.DEBUG)
    filename = "STM32F7_svd/STM32F7_svd_V1.4/STM32F7x7.svd"
    device = read_svd(filename)
    gen_code(device)


if __name__ == '__main__':
    main()
