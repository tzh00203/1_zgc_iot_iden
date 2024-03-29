
nmap_lib_path = "./nmap-service-probes"

nmap_lib = open(nmap_lib_path, "r", encoding="utf-8").readlines()

probe_list = []

for line in nmap_lib:
    if line.startswith("Probe "):
        probe_list.append(line)

probe_str = "".join(probe_list)

with open("./nmap_probe_request", "w", encoding="utf-8") as f:
    f.write(probe_str)




