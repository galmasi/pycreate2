##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# This decodes packets and returns a namedtuple (immutable)

from struct import Struct
from collections import namedtuple
from .OI import WHEEL_OVERCURRENT, BUMPS_WHEEL_DROPS, BUTTONS, CHARGE_SOURCE, LIGHT_BUMPER, STASIS

# build some packet decoders:
#   use: unpack_bool_byte(data)[0] -> returns tuple, but grab 0 entry
unpack_bool_byte = Struct('?').unpack         # 1 byte bool
unpack_byte = Struct('b').unpack              # 1 signed byte
unpack_unsigned_byte = Struct('B').unpack     # 1 unsigned byte
unpack_short = Struct('>h').unpack            # 2 signed bytes (short)
unpack_unsigned_short = Struct('>H').unpack   # 2 unsigned bytes (ushort)



# Some data is bit mapped. These namedtuples break those out for easier use
BumpsAndWheelDrop = namedtuple('BumpsAndWheelDrop', 'bump_left bump_right wheeldrop_left wheeldrop_right')
WheelOvercurrents = namedtuple('WheelOvercurrents', 'side_brush_overcurrent main_brush_overcurrent right_wheel_overcurrent left_wheel_overcurrent')
Buttons = namedtuple('Buttons', 'clean spot dock minute hour day schedule clock')
ChargingSources = namedtuple('ChargingSources', 'internal_charger home_base')
LightBumper = namedtuple('LightBumper', 'left front_left center_left center_right front_right right')
Stasis = namedtuple('Stasis', 'toggling disabled')

def unpack_bumps_wheeldrops (d):
    return BumpsAndWheelDrop(
        bool(d & BUMPS_WHEEL_DROPS.BUMP_RIGHT),
        bool(d & BUMPS_WHEEL_DROPS.BUMP_LEFT),
        bool(d & BUMPS_WHEEL_DROPS.WHEEL_DROP_RIGHT),
        bool(d & BUMPS_WHEEL_DROPS.WHEEL_DROP_LEFT)
    )

def unpack_wheelovercurrents(d):
    return WheelOvercurrents(
        bool(d & WHEEL_OVERCURRENT.SIDE_BRUSH),
        bool(d & WHEEL_OVERCURRENT.MAIN_BRUSH),
        bool(d & WHEEL_OVERCURRENT.RIGHT_WHEEL),
        bool(d & WHEEL_OVERCURRENT.LEFT_WHEEL)
    )

def unpack_buttons(d):
    return Buttons(
        bool(d & BUTTONS.CLEAN),
        bool(d & BUTTONS.SPOT),
        bool(d & BUTTONS.DOCK),
        bool(d & BUTTONS.MINUTE),
        bool(d & BUTTONS.HOUR),
        bool(d & BUTTONS.DAY),
        bool(d & BUTTONS.SCHEDULE),
        bool(d & BUTTONS.CLOCK)
    )

def unpack_chargingsources(d):
    return ChargingSources(
        bool(d & CHARGE_SOURCE.INTERNAL),
        bool(d & CHARGE_SOURCE.HOME_BASE)
    )

def unpack_lightbumper(d):
    return LightBumper(
        bool(d & LIGHT_BUMPER.LEFT),
        bool(d & LIGHT_BUMPER.FRONT_LEFT),
        bool(d & LIGHT_BUMPER.CENTER_LEFT),
        bool(d & LIGHT_BUMPER.CENTER_RIGHT),
        bool(d & LIGHT_BUMPER.FRONT_RIGHT),
        bool(d & LIGHT_BUMPER.RIGHT)
    )

def unpack_stasis(d):
    return Stasis(
        bool(d & STASIS.TOGGLING),
        bool(d & STASIS.DISABLED)
    )

# This is the big kahuna ... packet 100, everything
Sensors = namedtuple('Sensors', [
    'bumps_wheeldrops',
    'wall',
    'cliff_left',
    'cliff_front_left',
    'cliff_front_right',
    'cliff_right',
    'virtual_wall',
    'overcurrents',
    'dirt_detect',
    'ir_opcode',
    'buttons',
    'distance',
    'angle',
    'charger_state',
    'voltage',
    'current',
    'temperature',
    'battery_charge',
    'battery_capacity',
    'wall_signal',
    'cliff_left_signal',
    'cliff_front_left_signal',
    'cliff_front_right_signal',
    'cliff_right_signal',
    'charger_available',
    'open_interface_mode',
    'song_number',
    'song_playing',
    'oi_stream_num_packets',
    'velocity',
    'radius',
    'velocity_right',
    'velocity_left',
    'encoder_counts_left',
    'encoder_counts_right',
    'light_bumper',
    'light_bumper_left',
    'light_bumper_front_left',
    'light_bumper_center_left',
    'light_bumper_center_right',
    'light_bumper_front_right',
    'light_bumper_right',
    'ir_opcode_left',
    'ir_opcode_right',
    'left_motor_current',
    'right_motor_current',
    'main_brush_current',
    'side_brush_current',
    'statis'
])

Sensors0 = namedtuple('Sensors', [
    'bumps_wheeldrops',
    'wall',
    'cliff_left',
    'cliff_front_left',
    'cliff_front_right',
    'cliff_right',
    'virtual_wall',
    'overcurrents',
    'dirt_detect',
    'ir_opcode',
    'buttons',
    'distance',
    'angle',
    'charger_state',
    'voltage',
    'current',
    'temperature',
    'battery_charge',
    'battery_capacity'])

def SensorPacketDecoder(data, pktid=100):
    """
    This function decodes a Create 2 packet 100 and returns a Sensor object,
    which is really a namedtuple. The Sensor class holds all sensor values for
    the Create 2. It is basically like a C struct.
    """

    if pktid == 100:

        if len(data) != 80:
            raise Exception('Sensor: expected 80 bytes, got {}'.format(len(data)))
        return Sensors(
            unpack_bumps_wheeldrops(unpack_bool_byte(data[0:1])[0]),
            unpack_bool_byte(data[1:2])[0],         # wall
            unpack_bool_byte(data[2:3])[0],         # cliff left
            unpack_bool_byte(data[3:4])[0],         # cliff front left
            unpack_bool_byte(data[4:5])[0],         # cliff front right
            unpack_bool_byte(data[5:6])[0],         # cliff right
            unpack_bool_byte(data[6:7])[0],         # virtual wall
            unpack_wheelovercurrents(unpack_unsigned_byte(data[7:8])[0]),
            unpack_byte(data[8:9])[0],              # dirt detect
            # packet 16 or data bit 9 - unused
            unpack_unsigned_byte(data[10:11])[0],   # ir opcode
            unpack_buttons(unpack_unsigned_byte(data[11:12])[0]),
            unpack_short(data[12:14])[0],           # distance
            unpack_short(data[14:16])[0],           # angle
            unpack_unsigned_byte(data[16:17])[0],   # charge state
            unpack_unsigned_short(data[17:19])[0],  # voltage
            unpack_short(data[19:21])[0],           # current
            unpack_byte(data[21:22])[0],            # temperature in C, use CtoF if needed
            unpack_unsigned_short(data[22:24])[0],  # battery charge
            unpack_unsigned_short(data[24:26])[0],  # battery capacity
            unpack_unsigned_short(data[26:28])[0],  # wall
            unpack_unsigned_short(data[28:30])[0],  # cliff left
            unpack_unsigned_short(data[30:32])[0],  # cliff ront left
            unpack_unsigned_short(data[32:34])[0],  # cliff front right
            unpack_unsigned_short(data[34:36])[0],  # cliff right
            # packets 32, 33 or data bits 36, 37, 38 - unused
            unpack_chargingsources(unpack_unsigned_byte(data[39:40])[0]),
            unpack_unsigned_byte(data[40:41])[0],   # oi mode
            unpack_unsigned_byte(data[41:42])[0],   # song number
            unpack_bool_byte(data[42:43])[0],       # song playing
            unpack_unsigned_byte(data[43:44])[0],   # oi stream num packets
            unpack_short(data[44:46])[0],           # velocity
            unpack_short(data[46:48])[0],           # turn radius
            unpack_short(data[48:50])[0],           # velocity right
            unpack_short(data[50:52])[0],           # velocity left
            unpack_unsigned_short(data[52:54])[0],  # encoder left
            unpack_unsigned_short(data[54:56])[0],  # encoder right
            unpack_lightbumper(unpack_unsigned_byte(data[56:57])[0]),
            unpack_unsigned_short(data[57:59])[0],  # light bump left
            unpack_unsigned_short(data[59:61])[0],  # light bmp front left
            unpack_unsigned_short(data[61:63])[0],  # light bump center left
            unpack_unsigned_short(data[63:65])[0],  # light bump center right
            unpack_unsigned_short(data[65:67])[0],  # light bump front right
            unpack_unsigned_short(data[67:69])[0],  # light bump right
            unpack_unsigned_byte(data[69:70])[0],   # ir opcode left
            unpack_unsigned_byte(data[70:71])[0],   # ir opcode right
            unpack_short(data[71:73])[0],           # left motor current
            unpack_short(data[73:75])[0],           # right motor current
            unpack_short(data[75:77])[0],           # main brush current
            unpack_short(data[77:79])[0],           # side brush current
            unpack_stasis(unpack_unsigned_byte(data[79:80])[0])
        )
    elif pktid == 0:
        if len(data) != 26:
            raise Exception('Expected 26 bytes from sensor, got {}'.format(len(data)))
        return Sensors0(
            unpack_bumps_wheeldrops(unpack_bool_byte(data[0:1])[0]),
            unpack_bool_byte(data[1:2])[0],         # wall
            unpack_bool_byte(data[2:3])[0],         # cliff left
            unpack_bool_byte(data[3:4])[0],         # cliff front left
            unpack_bool_byte(data[4:5])[0],         # cliff front right
            unpack_bool_byte(data[5:6])[0],         # cliff right
            unpack_bool_byte(data[6:7])[0],         # virtual wall
            unpack_wheelovercurrents(unpack_unsigned_byte(data[7:8])[0]),
            unpack_byte(data[8:9])[0],              # dirt detect
            # packet 16 or data bit 9 - unused
            unpack_unsigned_byte(data[10:11])[0],   # ir opcode
            unpack_buttons(unpack_unsigned_byte(data[11:12])[0]),
            unpack_short(data[12:14])[0],           # distance
            unpack_short(data[14:16])[0],           # angle
            unpack_unsigned_byte(data[16:17])[0],   # charge state
            unpack_unsigned_short(data[17:19])[0],  # voltage
            unpack_short(data[19:21])[0],           # current
            unpack_byte(data[21:22])[0],            # temperature in C, use CtoF if needed
            unpack_unsigned_short(data[22:24])[0],  # battery charge
            unpack_unsigned_short(data[24:26])[0])  # battery capacity
        
