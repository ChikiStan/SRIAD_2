def adc_convert_for_axel(axel: bytes):
    if axel:
        if int(axel) > 32767:
            return (int(axel) - 65535) / 8192
        else:
            return int(axel) / 8192
    return 0


def adc_convert_for_gyro(gyro: bytes):
    if gyro:
        if int(gyro) > 32767:
            return (int(gyro) - 65535) / 65.5
        else:
            return (int(gyro)) / 65.5
    return 0
