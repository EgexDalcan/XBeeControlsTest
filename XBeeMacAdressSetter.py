from digi.xbee.devices import XBeeDevice
from digi.xbee.models.mode import OperatingMode
from digi.xbee.packets.common import ATCommPacket
from digi.xbee.models.address import XBee64BitAddress

'''
Puts on a filter adress if there is not one already else, removes the filter adress
'''

#The filter adress that is to be changed accordingly
dest_adress = "0013A20040BABB16"

#Port of the XBee
port = "COM6"

#Openning the XBee
xbee=XBeeDevice(port,9600)
xbee.open(force_settings=True)

#Changing the destination adress according to current status
if (xbee.get_dest_address() == XBee64BitAddress.from_hex_string("000000000000FFFF")):
  #Setting the destination adress
  print("Filter Set")
  adress = XBee64BitAddress.from_hex_string(dest_adress)
  xbee.set_dest_address(adress)
  xbee.write_changes()
  xbee.apply_changes()
else:
  #Removing the destination adress
  print("Filter Removed")
  adress = XBee64BitAddress.from_hex_string("000000000000FFFF")
  xbee.set_dest_address(adress)
  xbee.write_changes()
  xbee.apply_changes()

#Preparing the packet that will make the XBee to go to AT mode
packet = ATCommPacket(xbee.get_next_frame_id(), "AP", parameter=bytearray([OperatingMode.AT_MODE.code]))
out = packet.output(False)

#Turning the XBee back to AT mode
xbee.comm_iface.write_frame(out)

xbee.close()