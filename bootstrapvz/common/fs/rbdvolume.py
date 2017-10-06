from qemuvolume import QEMUVolume


class RbdVolume(QEMUVolume):

    extension = ''
    qemu_format = 'raw'
