import platform
import subprocess
import logging
import os
import sys
print(os.curdir)
sys.path.append(os.pardir)
from util import logger

log = logger.Logger(loglevel=logging.INFO, loggername=__name__).getlog()

# 获取当前电脑的uuid
def get_device_id():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid


# 获取当前电脑的操作系统
def isWindows():
    try:
        if platform.system().lower() == 'windows':
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
    return False

def isLinux():
    try:
        if platform.system().lower() == 'linux':
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
    return False


if __name__ == '__main__':
    print(get_device_id())