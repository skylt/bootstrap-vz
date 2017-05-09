import bootstrapvz.common.tasks.host as host
import bootstrapvz.common.tasks.volume as volume
from bootstrapvz.base import Task
from bootstrapvz.common import phases


class AddRequiredCommands(Task):
    description = 'Adding commands required for creating and mounting logical volumes'
    phase = phases.validation
    successors = [host.CheckExternalCommands]

    @classmethod
    def run(cls, info):
        from bootstrapvz.common.fs.logicalvolume import LogicalVolume
        if type(info.volume) is LogicalVolume:
            info.host_dependencies['lvcreate'] = 'lvm2'
            info.host_dependencies['losetup'] = 'mount'


class Create(Task):
    description = 'Creating a Logical volume'
    phase = phases.volume_creation
    successors = [volume.Attach]

    @classmethod
    def run(cls, info):
        image_path = '/dev/{vg}/{lv}'.format(vg=info.manifest.volume['logicalvolume'].get('vg', None),
                                             lv=info.manifest.volume['logicalvolume'].get('lv', None))
        info.volume.create(image_path)


class Delete(Task):
    description = 'Deleting a Logical volume'
    phase = phases.cleaning

    @classmethod
    def run(cls, info):
        info.volume.delete()