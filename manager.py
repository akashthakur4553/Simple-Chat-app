import random
from fastapi.websockets import WebSocket
from typing import Dict, List


class WebSocketManager:
    # List of emojis to assign randomly per IP
    EMOJI_POOL = ["😀","😎","🤖","🦊","🐱","🐶","🐼","🐸","🦄","🐙","🦋","🐢","🐝","🐬","🐳","🐞"]
    # List of random names to assign per client, unique per connected user
    NAME_POOL = ["Astra","Blaze","Cora","Dax","Eira","Finn","Gwen","Hugo","Ivy","Jax","Kara","Liam","Mira","Niko","Orla","Pax","Quinn","Rosa","Sage","Tara","Uma","Vex","Wren","Xara","Yara","Zane"]

    def __init__(self):
        self.connected_clients: List[WebSocket] = []
        # Mapping from client IP to its assigned emoji
        self.ip_to_emoji: Dict[str, str] = {}
        # Mapping from client IP to assigned random name
        self.ip_to_name: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients.append(websocket)
        client_ip = websocket.client.host
        client_port = websocket.client.port
        client_key = f"{client_ip}:{client_port}"
        # Assign a random emoji if this IP+port hasn't been seen before
        if client_key not in self.ip_to_emoji:
            self.ip_to_emoji[client_key] = random.choice(self.EMOJI_POOL)
        # Assign a unique random name if not already assigned
        if client_key not in self.ip_to_name:
            # Choose a name not already taken
            available_names = [n for n in self.NAME_POOL if n not in self.ip_to_name.values()]
            self.ip_to_name[client_key] = random.choice(available_names) if available_names else f"User{len(self.ip_to_name)+1}"
        print("client ip:", client_ip, "Port number", client_port)
        print("assigned emoji:", self.ip_to_emoji.get(client_key), "assigned name:", self.ip_to_name.get(client_key))
        # Send init payload to the newly connected client
        await websocket.send_json({
            "type": "init",
            "ip": client_key,
            "emoji": self.ip_to_emoji[client_key],
            "name": self.ip_to_name[client_key]
        })
        # Broadcast updated presence to all clients
        await self.broadcast_presence()

    async def send_message(self, client: WebSocket, sender_host: str, sender_port: int, message: dict):
        """Send a chat payload to a single client.

        The payload includes the sender's IP+port, the assigned emoji, and the message text.
        """
        sender_key = f"{sender_host}:{sender_port}"
        emoji = self.ip_to_emoji.get(sender_key, "❓")
        name = self.ip_to_name.get(sender_key, "")
        payload = {
            "ip": sender_key,
            "emoji": emoji,
            "name": name,
            "message": message.get("data", "")
        }
        await client.send_json(payload)
    async def broadcast_presence(self):
        """Notify all connected clients about current active users."""
        users = [{"ip": key, "emoji": self.ip_to_emoji.get(key), "name": self.ip_to_name.get(key)} for key in self.ip_to_emoji.keys()]
        payload = {"type": "presence", "users": users}
        await self._broadcast(payload)

    async def _broadcast(self, payload: dict):
        # Send payload to all clients, removing any that are no longer connected
        dead_clients = []
        for client in self.connected_clients:
            try:
                await client.send_json(payload)
            except Exception as e:
                # Log and mark for removal
                print(f"Error sending to client {client.client.host}:{client.client.port} - {e}")
                dead_clients.append(client)
        # Clean up dead clients
        for dc in dead_clients:
            self.connected_clients.remove(dc)
            client_key = f"{dc.client.host}:{dc.client.port}"
            self.ip_to_emoji.pop(client_key, None)
            self.ip_to_name.pop(client_key, None)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)
            # Remove emoji and name mapping for this client
            client_key = f"{websocket.client.host}:{websocket.client.port}"
            self.ip_to_emoji.pop(client_key, None)
            self.ip_to_name.pop(client_key, None)
            # Broadcast updated presence without the disconnected client
            await self.broadcast_presence()