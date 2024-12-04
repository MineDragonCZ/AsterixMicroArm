import serial
import time


class RobotController:
    def __init__(self, port, baudrate=115200, timeout=1):
        """
        Initializes the RobotController with a serial connection.

        :param port: The serial port the robot is connected to (e.g., "COM3" or "/dev/ttyUSB0").
        :param baudrate: The baud rate for serial communication (default is 115200).
        :param timeout: Timeout for reading from the serial port (default is 1 second).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        # Initialize the serial connection
        self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(2)  # Wait for the connection to establish

    def send_gcode(self, gcode):
        """
        Sends a G-code command to the robot.

        :param gcode: The G-code command string (e.g., "G1 X10 Y10 Z10 F100").
        """
        if not self.serial_connection.is_open:
            print("Serial port is not open!")
            return

        # Send G-code to the robot
        self.serial_connection.write((gcode + '\n').encode('utf-8'))
        print(f"Sent: {gcode}")

        # Optionally, read the response (if the robot sends anything back)
        response = self.read_response()
        if response:
            print(f"Received: {response}")

    def read_response(self):
        """
        Reads the response from the robot after sending a G-code command.
        """
        if self.serial_connection.in_waiting > 0:
            response = self.serial_connection.readline().decode('utf-8').strip()
            return response
        return None

    def move_to_position(self, x, y, z, feedrate=100):
        """
        Sends a G-code command to move the robot to a specific position.

        :param x: The X position (in mm).
        :param y: The Y position (in mm).
        :param z: The Z position (in mm).
        :param feedrate: The feedrate (in mm/min) for movement (default is 100).
        """
        gcode = f"G1 X{x} Y{y} Z{z} F{feedrate}"
        self.send_gcode(gcode)

    def home(self):
        """
        Sends a G-code command to home the robot (move to the origin).
        """
        self.send_gcode("G28")  # G28 is commonly used to home axes

    def set_speed(self, feedrate):
        """
        Sets the robot's movement speed (feedrate).

        :param feedrate: The speed (in mm/min).
        """
        gcode = f"F{feedrate}"
        self.send_gcode(gcode)

    def close(self):
        """
        Closes the serial connection.
        """
        if self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial connection closed.")
