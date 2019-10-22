from pubsub import pub
from Gamepad_ThrusterOrder import Thruster


def send():
    def commandListener(command):
        bus = can.interface.Bus()

        msg = can.Message(arbitration_id=command[1],
                          data= command[2],
                          is_extended_id=False)
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except can.CanError:
            print("Message NOT sent")

    pub.subscribe(commandListener, 'Thruster')


if __name__ == '__main__':
    send()
