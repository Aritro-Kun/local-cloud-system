So, here we discuss how you can have the info you get while you do `ipconfig /all` in your windows, in your Mac.
-

It involves quite a few drastic, tiring yet exciting steps, so let's get along.

- Open your terminal `command(next to your spacebar) + space`
- Inside your terminal type out `nano network-info.sh`
- Next, copy this in the file, simply copy it and paste it in the file:
  

INTERFACE="en0"

echo "=== Network Information for Interface: $INTERFACE ==="
echo

echo "Private IP Address:"
ipconfig getifaddr $INTERFACE
echo

echo "Subnet Mask:"
ipconfig getoption $INTERFACE subnet_mask
echo

echo "MAC Address:"
networksetup -getmacaddress $INTERFACE | awk '{print $3}'
echo

echo "Default Gateway:"
ipconfig getoption $INTERFACE router
echo

echo "DNS Servers:"
scutil --dns | awk '/nameserver\[[0-9]+\]/ {getline; print}' | sort -u
echo

echo "DHCP Server:"
ipconfig getpacket $INTERFACE | grep "server_identifier" | awk '{print $3}'
echo


- Then save this file, for this type `Ctrl + O`, i mean Oh, as in O in operate. Then click Enter and `Ctrl + X` to exit out of the file.
- Make the file executable: `chmod +x network-info.sh`
- Now run it: `./network-info.sh`

Kabooom, youhave the necessities, you require right now,



