import smbus
import numpy as np

# 0x00: Select master data -- AS72651
# 0x01: Select first slave data -- AS72652
# 0x02: Select second slave data -- AS72653
# 0x4F: DEV_SEL register address

bus = smbus.SMBus(2)

STATUS_REGISTER = 0x00
WRITE_REGISTER = 0x01
READ_REGISTER = 0x02
DEVICE_SLAVE_ADDRESS = 0x49
MASTER_READ = 0x93
MASTER_WRITE = 0x92

RAW_VALUE_RGA_HIGH = 0x08
RAW_VALUE_RGA_LOW = 0x09

RAW_VALUE_SHB_HIGH = 0x0A
RAW_VALUE_SHB_LOW = 0x0B

RAW_VALUE_TIC_HIGH = 0x0C
RAW_VALUE_TIC_LOW = 0x0D

RAW_VALUE_UJD_HIGH = 0x0E
RAW_VALUE_UJD_LOW = 0x0F

RAW_VALUE_VKE_HIGH = 0x10
RAW_VALUE_VKE_LOW = 0x11

RAW_VALUE_WLF_HIGH = 0x12
RAW_VALUE_WLF_LOW = 0x13


# def read_data(ADDRESS,):
#	return np.int32(bus.read_byte_data(I2C_ADDRESS_MASTER, num))

def get_decimal(virtual_reg_L, virtual_reg_H):  # might be wrong
    # Gets most significant bit (MSG) and shifts by 8
    high = i2cm_as7265_read(virtual_reg_H) << 8
    # Combines MSB and LSB and scales based off of values in the
    return np.int16((high | i2cm_as7265_read(virtual_reg_L)))

    # THINGS WE NEED DEFINED
    # I2C_AS7265_SLAVE_STATUS_REG = STATUS_REGISTER
    # virtualReg =


def i2cm_as7265_read(virtualReg):
    print("hello")
    # while True:
    #     # Read slave I²C status to see if the read buffer is ready.
    #     status = bus.read_byte_data(STATUS_REGISTER)  # i2cm_read(I2C_AS7265_SLAVE_STATUS_REG)
    #     if (status & READ_REGISTER) == 0:
    #         # No inbound TX pending at slave. Okay to write now.
    #         break
    #     # Send the virtual register address (disabling bit 7 to indicate a read).
    i = 0
    while i < 1000:
        i += 1
    bus.write_byte(WRITE_REGISTER, virtualReg & 0x7F)
    i = 0
    while i < 1000:
        i += 1

    # while True:
    #     # Read the slave I²C status to see if our read data is available.
    #     status = bus.read_byte_data(STATUS_REGISTER)
    #     if (status & WRITE_REGISTER) != 0:
    #         # Read data is ready.
    #         break
    #     # Read the data to complete the operation.
    data = bus.read_byte(READ_REGISTER)  # i2cm_read(I2C_AS72XX_SLAVE_READ_REG)
    return data


# write function
# def i2cm_AS7265_write(virtualReg, d):
#     while True:
#         # Read slave I²C status to see if the write buffer is ready.
#         status = i2cm_read(I2C_AS72XX_SLAVE_STATUS_REG);
#         if ((status & I2C_AS72XX_SLAVE_TX_VALID) == 0):
#             # No inbound TX pending at slave. Okay to write now.
#             break
#     bus.write_byte_data(I2C_AS72XX_SLAVE_WRITE_REG, virtualReg)
#     while True:
#         status = bus.read_byte_data()


def main():
    # dataFile = open("output.txt", "w")

    while True:
        # loop through virtual registers

        rga_data = get_decimal(RAW_VALUE_RGA_LOW, RAW_VALUE_RGA_HIGH)
        shb_data = get_decimal(RAW_VALUE_SHB_LOW, RAW_VALUE_SHB_HIGH)
        tic_data = get_decimal(RAW_VALUE_TIC_LOW, RAW_VALUE_TIC_HIGH)
        ujd_data = get_decimal(RAW_VALUE_UJD_LOW, RAW_VALUE_UJD_HIGH)
        vke_data = get_decimal(RAW_VALUE_VKE_LOW, RAW_VALUE_VKE_HIGH)
        wlf_data = get_decimal(RAW_VALUE_WLF_LOW, RAW_VALUE_WLF_HIGH)

        print(rga_data, shb_data, tic_data, ujd_data, vke_data, wlf_data)
if __name__ == "__main__":
    main()