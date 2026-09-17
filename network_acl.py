BLOCKED_SUBNETS = []

#Collect the blocked subnets from a given file
def load_blacklist(filepath):
    global BLOCKED_SUBNETS

    try:
        with open(filepath, 'r') as f:
            #go over every line and ignore empty ones
            BLOCKED_SUBNETS = [line.strip() for line in f if line.strip()]

        print(f"[SYSTEM] loaded {len(BLOCKED_SUBNETS)} subnets from {filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to load blacklist: {e}")


# Converts an IPv4 string (e.g., "192.168.1.1") to a 32-bit integer representation
def ip_to_int(ip:str)->int:
    parts = ip.split('.')#array of ip parts

    num1 = int(parts[0])
    num2 = int(parts[1])
    num3 = int(parts[2])
    num4 = int(parts[3])

    #moving each part to its place:
    res = (num1 << 24) + (num2 << 16) + (num3 << 8) + num4
    return res

# Checks if a given client IP address falls within any blocked CIDR subnets
def is_blocked(client_ip:str)-> bool:
    ip = ip_to_int(client_ip)

    for subnet in BLOCKED_SUBNETS:
        if '/' not in subnet:
            subnet += '/32' # Default to a single IP mask
            
        network_ip_str, mask_bits_str = subnet.split('/')

        network_ip = ip_to_int(network_ip_str)
        mask_bits = int(mask_bits_str)

        #bit mask for comparing ip address
        mask = (0xFFFFFFFF << (32-mask_bits)) & 0xFFFFFFFF

        if(ip & mask) == (network_ip & mask):
            print(f"[WAF BLOCK] IP {ip} blocked by ALC rule {subnet}")
            return True
    return False

