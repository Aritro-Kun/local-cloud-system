Local-File-Storage-System
-

The project is mainly to explore methods how an user can get to setup local file sharing system between thier devices in a **local-area-network**. (LAN).

We first will try to give you an overview of how devices are connected to each other in a local network or maybe in the internet.

Let's first understand, what happens when you connect your device to a router. Say, you have just bought a router which is connected to the *ISP(Internet Service Provider)*. Then you connect your device to this router. So, what happens under the hood?


Your device first sends something called a DHCP Disover. Omg, so many jargons. Lets get a hang. What is this? First, let's understand *DHCP(Dynamic Host Configuration Protocol)*. It's basically a set of info, which every device receives from DHCP servers. When your device is connected to the router, it does the following things:
- It does a **DHCP Discover**, where it boradcastsa DHCP Discover message so as to locate the available DHCP servers in the network.
- Now, the DHCP servers which receive this DHCP Discover message respond with a **DHCP Offer** which includes an available IP address(note: this is private ip, exclusive for this device) and some other configuration parameter(which we will discuss in a while).
- The device now selects an offer and sends a **DHCP Request** message to the selected DHCP server, which is basically a request for the offered IP address and other configurations.
- The DHCP server which is sent this DHCP Request then sends a **DHCP Acknowledge** message to the device, thus confirming the assigning of the IP address and the configurations.

This four step process is known as a DHCP DORA process. After this process is done, the device receives a packet of DHCP info which consists of stuffs like:
- The assigned private IP address
- The default gateway(the IP address of the router, this is used when the device communicates with devices outside the LAN)
- The Subnet Mask (this is a pretty cool thing, you can run ipconfig in your terminal and you may find something like 255.255.255.0 and it has a pretty cool use, it is basically used to differentiate the network portion and the host portion of the private ip, if the network portion of two private ip's match, then it means those two devcies are connected to the same network.)
- DNS Server (your device will try to speak to google.com, but that's the name of the domain, the device needs the ip address of the server which runs google.com, so it reaches this server to find the ip address of the domains, it needs. Fun Fact: You can manually change the DNS Server of your system.)
- DHCP Server
- Lease Time (each device is assigned a private ip, but it is for a limited time, this limited time is known as lease)



Good progress so far, each of the connected devices now have a private IP, oh btw, what is IP Address, it stands for Internet Protocol Address, which each device gets when connected to the internet, basically just an address. Although I have never mentioned the word public IP address so as to avoid confusion and typically used private IP all along, but let's try to draw a line between these two. 

- Public IP Address:
  -- This is usually for your router, since when you communicate with a friend sitting 50KMs apart connected to their own WiFi(router) then your device connected to your router communicates with their router through the ISP(Internet Service Provider). So it's basically the router of yours which is available for communication in the internet, so it has a public IP address which makes it addressable in the web.
- Private IP Address:
  -- This is for your personal device, which is connected to the router. The router communicates with your friend, receives information and sends that to your private IP(the device you are using, rn).

Better to have an analogy: Your router(public IP Address) is like the country name and your device(private IP address) is your city/town name.


Back to our topic: We are considering an exceptional case, where our communicating devices are connected in the same network(the Local Network, thus). Now, when two devices residing in a local network communicate with each other, they dont necessarily use their private IPs, although they do, but the ultimate communication is through something known as a **MAC Address(Media Access Control)**. 

*Btw, we got over so many jargons already, already enough to flex in front of your non-tech friends. ;)*

Okay, so what happens is: When device A wants to communicate with device B, provided they are connected to the same network, then the following steps happen:

