Ports: 6080 for noVNC, 8080 and 8443 for chat

WireShark filter HTTP: `tcp.port == 8080 && ip.dst == 172.20.0.2 && http`
WireShark filter HTTPS: `tcp.port == 8443 && ip.dst == 172.20.0.2`
