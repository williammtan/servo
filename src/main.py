import sys

from turret import TurretCommand


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'command':
        print("Running command mode...")
        turret = TurretCommand()
    elif mode == 'follow':
        print("Running follow mode...")
        turret = TurretFollow()
        pass