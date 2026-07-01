from typing import final as sealed

@sealed
class DiscordRpcPayloadDto:
    def __init__(self):
        self.client_id: str = ""
        self.details: str = ""
        self.state: str = ""
        self.use_timestamps: bool = False
        self.as_time_remaining: bool = False
        self.total_duration_minutes: int = 60
        self.large_image_key: str = ""
        self.large_image_text: str = ""
        self.small_image_key: str = ""
        self.small_image_text: str = ""
        self.party_id: str = ""
        self.party_current_size: int = 1
        self.party_max_size: int = 4
        self.join_secret: str = ""
        self.spectate_secret: str = ""
        self.button_1_label: str = ""
        self.button_1_url: str = ""
        self.button_2_label: str = ""
        self.button_2_url: str = ""