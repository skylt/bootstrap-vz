from bootstrapvz.base.fs.volume import Volume
from bootstrapvz.common.tools import log_check_call


class LogicalVolume(Volume):

    def create(self, image_path):
        self.image_path = image_path
        self.fsm.create(image_path=image_path)

    def _before_create(self, e):
        lv_size = str(self.size.bytes.get_qty_in('MiB'))
        vg, lv = e.image_path.split('/')[2:4]
        log_check_call(['lvcreate', '--size', '{mib}M'.format(mib=lv_size), '--name', lv, vg])

    def _before_attach(self, e):
        log_check_call(['vgchange', '--activate', 'y', self.image_path.split('/')[2]])
        mapper_path = '/dev/mapper/' + '-'.join(str(x) for x in self.image_path.split('/')[2:4])
        [self.loop_device_path] = log_check_call(['losetup', '--show', '--find', '--partscan', mapper_path])
        self.device_path = self.loop_device_path

    def _before_detach(self, e):
        log_check_call(['losetup', '--detach', self.loop_device_path])
        log_check_call(['vgchange', '--activate', 'n', self.image_path.split('/')[2]])
        del self.loop_device_path
        self.device_path = None

    def delete(self):
        log_check_call(['lvremove', '-f', self.image_path])
        del self.image_path
