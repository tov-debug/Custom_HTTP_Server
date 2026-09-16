BLOCKED_SUBNETS = [
    "192.168.1.0/24", #local
    "10.0.0.0/8" #corporate
    #can add more

]

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
        network_ip_str, mask_bits_str = subnet.split('/')

        network_ip = ip_to_int(network_ip_str)
        mask_bits = int(mask_bits_str)

        #bit mask for comparing ip address
        mask = (0xFFFFFFFF << (32-mask_bits)) & 0xFFFFFFFF

        if(ip & mask) == (network_ip & mask):
            print(f"[WAF BLOCK] IP {ip} blocked by ALC rule {subnet}")
            return True
    return False

