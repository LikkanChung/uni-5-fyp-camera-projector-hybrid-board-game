from ..utils.utils import PORT
from .network import Network

def main():
    print("CLIENT STARTED")
    print("CONNECTING TO SERVER")

    ip_port = "ip:port"
    player_id = "player_id"
    print(f"CONNECTED TO SERVER\n\ton {ip_port}\n\tas player {player_id}")

    net = Network("localhost", PORT)

    net.send(input("send to server:"))
