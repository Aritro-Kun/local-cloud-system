Local Communication, under the hood
-

Let's try to understand how device A and device B would initiate a conversation, provided they are connected to the same router:

Hypothetically, device A is assumed to be knowing the private IP address of device B. But, it hasn't interacted with device B, so it is unaware of it's MAC address. Hence, the first task of device A is to ask for device B's MAC Address, because local communications are done through the MAC Addresses only. 
- Device A, sends an ARP(Address Resolution Protocol) Request in the local network. This is a broadcast message which is of the form of an Ethernet Frame and consists of the destination MAC address as the Broadcast MAC Address, this ensures that the request reaches every single connected device in the network.
- Now, the ARP request looks like this: "Who has the IP address {blah.blah.blah.blah}? Please tell your MAC address."
- And, the ARP request as we stated is a packet of data, which contains the source IP address(in this case, the private ip of device A), the source MAC address(device A's MAC address) and destination private IP address(i.e device B's private IP address).
- Once device B realises that this request is intended for it, it responds an ARP Reply.
- This ARP Reply is responded by device B directly to device A's MAC address.
- And the ARP Reply packet contains device B's MAC Address and also it's private IP Address.
- Now, that device A has device B's MAC Address, it stores/ maps this MAC address with device B's private IP address in its own ARP cache, which is a temporary table.

Now, device A and device B are aware of the middleware's. Device A has got in it's arsenal the most important thing it needed in order to communicate with B.

Now, let's hop onto how data will finally be transmitted between these two devices when they communicate with each other.
