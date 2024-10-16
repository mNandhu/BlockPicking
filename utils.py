from xarm.wrapper import XArmAPI
from time import sleep


class ArmHandler:
    def __init__(self,ip = '192.168.1.155'):
        """
        Initialize the arm
        (Try setting ethernet ip in your laptop (DHCP->Manual)to 192.168.1.225)
        """

        self.arm = XArmAPI(ip)
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(0)
        self.arm.connect()
        self.arm.move_gohome()

    def place_block_on(self, x=225, y=-95, z=87):
        """
        Drop the block at the given position, by default at assumed conveyor belt position
        :param x:
        :param y:
        :param z:
        :return:
        """
        # self.arm.move_gohome()
        self.arm.set_position(x, y, z, roll=180, pitch=0, yaw=0)
        self.arm.set_suction_cup(False)
        self.arm.set_position(x=x, y=y, z=z + 20, roll=180, pitch=0, yaw=0)
        self.arm.move_gohome()

    def pickup_and_wait(self):
        """
        Starts the suction cup at home position, and waits for 4 seconds
        :return:
        """
        self.arm.move_gohome()
        self.arm.set_suction_cup(True)
        sleep(4)

    def pickup_block_from(self, x, y, z=20) -> bool:
        """
        Pickup block from the given coordinates, z default for small cube
        :param x:
        :param y:
        :param z:
        :return: Returns false if out of bounds
        """
        if not self.is_in_range(x,y):
            print("Out of RANGE")
            return False

        self.arm.set_position(x=x, y=y, z=z + 10, roll=180, pitch=0, yaw=0)
        self.arm.set_suction_cup(True)
        sleep(0.5)
        self.arm.set_position(x=x, y=y, z=z, roll=180, pitch=0, yaw=0)
        sleep(1)
        self.arm.set_position(x=x, y=y, z=z + 110, roll=180, pitch=0, yaw=0)
        # self.arm.move_gohome()

        return True

    @staticmethod
    def is_in_range(x , y):
        return (215 < x < 300) and y >= 0

    def disconnect(self):
        self.arm.set_suction_cup(False)
        sleep(2)
        self.arm.move_gohome()
        self.arm.disconnect()
