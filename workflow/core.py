import os
import platform
import subprocess
from queue import Queue, Empty
import psutil
import threading

cmd = "ipconfig /all"
result = os.popen(cmd, "r")
termObj = result.read()
reachedState = False
infoDict = {}

for line in termObj.splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith("Wireless LAN adapter Wi-Fi:"):
        reachedState = True
        continue
    if reachedState:
        if line.startswith("Media State"):
            key, value = line.split(":")
            key = key.split(".", 1)
            key = key[0].strip()
            value = value.strip()
            infoDict[key] = value
        elif (line.startswith("Physical Address") or line.startswith("IPv4 Address") or line.startswith("Subnet Mask") or line.startswith("Default Gateway") or line.startswith("DHCP Server") or line.startswith("DNS Servers")):
            key, value = line.split(":",1)
            key = key.split(".")
            key = key[0].strip()
            value = value.strip()
            if(line.startswith("Physical Address")):
               key = "MAC Address"
            if(line.startswith("IPv4 Address")):
                key, value = line.split(":", 1)
                key = "Private IP Address"
                value = value.split("(")
                value = value[0].strip()
            infoDict[key] = value

print(infoDict)

private_ip = infoDict.get("Private IP Address")
private_ip_list = [int(x) for x in private_ip.split(".")]
print(private_ip_list)

gateway_ip = infoDict.get("Default Gateway")

subnet_mask = infoDict.get("Subnet Mask")
subnet_mask_list = [int(x) for x in subnet_mask.split(".")]
print(subnet_mask_list)

net_add = []
if(len(private_ip_list) == len(subnet_mask_list)):
    for i in range(0,len(private_ip_list)):
        value = private_ip_list[i]&subnet_mask_list[i]
        net_add.append(value)

print(net_add)

ones_subnet = []
for i in range(0, len(subnet_mask_list)):
    val = ~(subnet_mask_list[i]) & 0xFF
    ones_subnet.append(val)

print(ones_subnet)

broad_add = []
if(len(net_add) == len(ones_subnet)):
    for i in range(0, len(net_add)):
        value = net_add[i] | ones_subnet[i]
        broad_add.append(value)

print(broad_add)

list_ips = []
for i in range(net_add[-1]+1, broad_add[-1]):
    ip_rn = ".".join(str(net_add[num]) for num in range(0, len(net_add)-1))
    ip_rn = ip_rn + "." + str(i)
    if(ip_rn != private_ip and ip_rn != gateway_ip):
        list_ips.append(ip_rn)
print(list_ips)
print(len(list_ips))

def pinging_ip(ip_address):
    try:
        if platform.system().lower() == 'windows':
            param = '-n'
        else:
            param = '-c'
        cmd = ["ping", param, '1', ip_address]
        creationflags = 0
        if platform.system().lower() == 'windows':
            creationflags = subprocess.CREATE_NO_WINDOW
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, creationflags = creationflags)
        stdout, stderr = process.communicate(timeout=1)
        stdout_str = stdout.decode('utf-8', errors='ignore')
        stderr_str = stderr.decode('utf-8', errors='ignore')
        return ip_address, stdout_str, stderr_str
    except subprocess.TimeoutExpired:
        return ip_address, "", "Timeout occurred"
    except FileNotFoundError:
        return ip_address, "", "Error: ping command not found. Please ensure it is in your system path."
    except OSError as e:
        return ip_address, "", f"Error executing ping: {e}"

def indiv_thread(ip_queue, results):
    while True:
        try:
            ip_add = ip_queue.get(timeout=1)
        except Empty:
            break
        ip, out, err = pinging_ip(ip_add)
        if "TTL=" in out and not err:
            results.append(ip)
        ip_queue.task_done()

def determine_number_threads(cpu_threshold=70):
    total_cores = psutil.cpu_count()
    cpu_usages = psutil.cpu_percent(interval=0.1, percpu=True)
    available_cores = 0
    for usage in cpu_usages:
        if usage < cpu_threshold:
            available_cores+=1
    return max(1, min(available_cores*2, total_cores*4))

def overall_thread_manager(ips_list):
    results = []
    ip_queue = Queue()
    num_of_threads = determine_number_threads()
    print("The number of threads chosen to do the task: ", num_of_threads)
    for i in range(0, len(ips_list)):
        ip_queue.put(ips_list[i])
    threads = []
    for _ in range(0, num_of_threads):
        thread = threading.Thread(target=indiv_thread, args=(ip_queue, results))
        threads.append(thread)
        thread.start()
    ip_queue.join()
    for th in threads:
        th.join()
    return results

available_ips = []
available_ips = overall_thread_manager(list_ips)
print(available_ips)
