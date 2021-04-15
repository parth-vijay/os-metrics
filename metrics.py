import psutil
import shutil
import time
import platform
import subprocess, re

def cpu():
    return "CPU Usage: " + str(psutil.cpu_percent()), psutil.cpu_count()

def memory():
    totalMem = str(dict(psutil.virtual_memory()._asdict())['total']/(1024*1024))
    freeMem = str(dict(psutil.virtual_memory()._asdict())['free']/(1024*1024))
    usedMem = str(dict(psutil.virtual_memory()._asdict())['used']/(1024*1024))
    if platform.system() == "Linux":
        bufferMem = str(dict(psutil.virtual_memory()._asdict())['buffers']/(1024*1024))
        cacheMem = str(dict(psutil.virtual_memory()._asdict())['cached']/(1024*1024))
    availableMem = str(dict(psutil.virtual_memory()._asdict())['available']/(1024*1024))
    try:
        return "Total Mem: " + totalMem, "Free Mem: " + freeMem, "Used Mem: " + usedMem, "Buffered Mem: " + bufferMem, cacheMem, "Avail Mem: " + availableMem
    except:
        return "Total Mem: " + totalMem, "Free Mem: " + freeMem, "Used Mem: " + usedMem, "Avail Mem: " + availableMem

def disk():
    totalDisk, usedDisk, freeDisk = shutil.disk_usage("/")
    diskRead = str(dict(psutil.disk_io_counters(perdisk=False, nowrap=True)._asdict())['read_bytes']/(1024*1024))
    diskWrite = str(dict(psutil.disk_io_counters(perdisk=False, nowrap=True)._asdict())['write_bytes']/(1024*1024))
    return "Total Disk: " + str(totalDisk), "Used Disk: " + str(usedDisk), "Free Disk: " + str(freeDisk), "Disk Read: " + diskRead, "Disk Write: " + diskWrite

def network():
    netBytesSent = str(dict(psutil.net_io_counters()._asdict())['bytes_sent']/(1024*1024))
    netBytesRec = str(dict(psutil.net_io_counters()._asdict())['bytes_recv']/(1024*1024))
    netPacketSent = str(dict(psutil.net_io_counters()._asdict())['packets_sent'])
    netPacketRec = str(dict(psutil.net_io_counters()._asdict())['packets_recv'])
    return "Net Bytes Received: " + netBytesRec, "Net Bytes Sent: " + netBytesSent, "Net Packet Sent: " + netPacketSent, "Net Packet Received: " + netPacketRec

def service_metrics():
    services = ['apache2', 'mysql', 'postgresql']
    service_status_data = []
    for service in services:
        p =  subprocess.Popen(["systemctl", "status",  service], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        output = output.decode('utf-8')

        service_regx = r"Loaded:.*\/(.*service);"
        status_regx= r"Active:(.*) since (.*);(.*)"
        service_status = {}
        for line in output.splitlines():
            service_search = re.search(service_regx, line)
            status_search = re.search(status_regx, line)

            if service_search:
                service_status['service'] = service_search.group(1)

            elif status_search:
                service_status['status'] = status_search.group(1).strip()
                service_status['since'] = status_search.group(2).strip()
                service_status['uptime'] = status_search.group(3).strip()
        service_status_data.append(service_status)

    return service_status_data

# print(cpu(),"\n",memory(),"\n",disk(),"\n",network(),"\n",service_metrics())
print(service_metrics())