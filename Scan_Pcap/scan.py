from scapy.all import *
from ipaddress import ip_address
import os
import json

allIP =collections.defaultdict(dict)
#ipleri listede toplama
def ipAdress(packets):
    PaketSayisi=1
    for pkt in packets:
        if ((ip_address(pkt[0][1].src).is_global)) or ((ip_address(pkt[0][1].dst).is_global)):
            allIP['Paket '+str(PaketSayisi)]['Source '] = (pkt[0][1].src)
            allIP['Paket '+str(PaketSayisi)]['Dest. '] = (pkt[0][1].dst)
            PaketSayisi=PaketSayisi+1
    #Json formatında yazdırıyoruz.
    with open("jsonpcap\publicIP.json", "w") as outfile:
        json.dump(allIP, outfile, indent=4)

    
if __name__ == '__main__':
    #Pcap klasörü içerisinde bulunan bütün pcap dosyalarını çekiyoruz.
    file_list = os.listdir("pcap")
    for a in range(len(file_list)):
        packet= rdpcap('pcap/'+file_list[a])
        ipAdress(packet)

    


