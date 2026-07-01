import json
import os
import struct
import time
import uuid
from typing import final as sealed

from core.interfaces import IDisposable
from core.native_methods import NativeMethods
from dtos.discord_rpc_payload_dto import DiscordRpcPayloadDto

@sealed
class DiscordRpcService(IDisposable):
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.handle = NativeMethods.INVALID_HANDLE_VALUE
        
    def connect(self):
        if self.handle != NativeMethods.INVALID_HANDLE_VALUE:
            return
            
        for i in range(10):
            self.handle = NativeMethods.open_discord_pipe(i)
            if self.handle != NativeMethods.INVALID_HANDLE_VALUE:
                break
        
        if self.handle == NativeMethods.INVALID_HANDLE_VALUE:
            raise ConnectionError
        
        handshake = json.dumps({"v": 1, "client_id": self.client_id}, separators=(",", ":"))
        self._send(0, handshake)

    def _send(self, opcode: int, payload_str: str):
        if self.handle == NativeMethods.INVALID_HANDLE_VALUE:
            raise RuntimeError
            
        payload_bytes = payload_str.encode('utf-8')
        header = struct.pack("<II", opcode, len(payload_bytes))
        full_packet = bytearray(len(header) + len(payload_bytes))
        
        mv = memoryview(full_packet) # Span<byte>
        mv[:len(header)] = header # headerBytes.AsSpan().CopyTo(bufferSpan.Slice(0, header.Length))
        mv[len(header):] = payload_bytes # payloadBytes.AsSpan().CopyTo(bufferSpan.Slice(header.Length))

        # write pipe
        if not NativeMethods.write_pipe(self.handle, full_packet):
            raise IOError

        # flush pipe
        response = NativeMethods.read_pipe(self.handle)

        if __debug__:
            if response:
                json_data = response[8:].decode("utf-8")
                print(f"[DiscordRpc::Emit] Pipe response received: {json_data}")
            else:
                print("[DiscordRpc::Emit] No response from pipe.")

    def update_presence(self, dto: DiscordRpcPayloadDto):
        activity = {}

        if dto.state: activity["state"] = dto.state
        if dto.details: activity["details"] = dto.details

        if dto.use_timestamps:
            now = int(time.time())
            if dto.as_time_remaining:
                activity["timestamps"] = {
                    "start": now,
                    "end": now + (dto.total_duration_minutes * 60)
                }
            else:
                activity["timestamps"] = {"start": now}

        assets = {}
        if dto.large_image_key: assets["large_image"] = dto.large_image_key
        if dto.large_image_text: assets["large_text"] = dto.large_image_text
        if dto.small_image_key: assets["small_image"] = dto.small_image_key
        if dto.small_image_text: assets["small_text"] = dto.small_image_text
        if assets: activity["assets"] = assets

        if dto.party_id:
            activity["party"] = {
                "id": dto.party_id,
                "size": [dto.party_current_size, dto.party_max_size]
            }

        secrets = {}
        if dto.join_secret: secrets["join"] = dto.join_secret
        if dto.spectate_secret: secrets["spectate"] = dto.spectate_secret
        if secrets: activity["secrets"] = secrets

        buttons = []
        if dto.button_1_label and dto.button_1_url:
            buttons.append({"label": dto.button_1_label, "url": dto.button_1_url})
        if dto.button_2_label and dto.button_2_url:
            buttons.append({"label": dto.button_2_label, "url": dto.button_2_url})
        if buttons: activity["buttons"] = buttons

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": os.getpid(),
                "activity": activity if activity else None
            },
            "nonce": str(uuid.uuid4())
        }

        compact_json = json.dumps(payload, separators=(",", ":"))
        if __debug__:
            print(f"[DiscordRpc::Message] Pipe message sent: {compact_json}")
        self._send(1, compact_json)
        
    def stop(self):
        if self.handle != NativeMethods.INVALID_HANDLE_VALUE:
            payload = {
                "cmd": "SET_ACTIVITY",
                "args": {"pid": os.getpid(), "activity": None},
                "nonce": str(uuid.uuid4())
            }
            try:
                self._send(1, json.dumps(payload))
            except IOError:
                pass

    def close(self):
        if self.handle != NativeMethods.INVALID_HANDLE_VALUE:
            NativeMethods.close_handle(self.handle)
            self.handle = NativeMethods.INVALID_HANDLE_VALUE

    def dispose(self):
        self.stop()
        self.close()

        self.client_id = None
        self.handle = NativeMethods.INVALID_HANDLE_VALUE
