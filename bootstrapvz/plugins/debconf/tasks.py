from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tasks import packages
from bootstrapvz.common.tools import log_check_call_chroot


class DebconfSetSelections(Task):
    description = 'Set debconf(7) selections from the manifest'
    phase = phases.package_installation
    successors = [packages.InstallPackages]

    @classmethod
    def run(cls, info):
        log_check_call_chroot(['chroot', info.root, 'debconf-set-selections'],
                              stdin=info.manifest.plugins['debconf'])
