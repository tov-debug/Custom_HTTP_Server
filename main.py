import argparse
from server import start_server
from network_acl import load_blacklist


if __name__ == "__main__":
    #connect to command line
    parser = argparse.ArgumentParser(description= "Custom HTTP Server & WAF Gateway")
    parser.add_argument('-b', '--blacklist', type=str, default='blacklist.txt', help='Path to the IP ACL blacklist file')
    args = parser.parse_args()

    load_blacklist(args.blacklist)

    print("[SYSTEM] Starting server on port 8085")
    start_server()
