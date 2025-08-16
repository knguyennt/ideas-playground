import asyncio
import json
import io
import requests
import websockets
import sounddevice as sd
import soundfile as sf
import numpy as np


class VTubeStudioAPI:
    def __init__(self, plugin_name="Miku", plugin_developer="Miku"):
        self.plugin_name = plugin_name
        self.plugin_developer = plugin_developer
        self.websocket_url = "ws://localhost:8001"
        self.tts_url = "http://localhost:5000"
    
    def create_auth_token_request(self):
        return {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
            }
        }
    
    def create_auth_request(self, token):
        return {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
                "authenticationToken": token
            }
        }
    
    def create_parameter_list_request(self, token):
        return {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "InputParameterListRequest",
            "data": {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
                "authenticationToken": token
            }
        }
    
    def create_parameter_injection_request(self, token, parameter_id, value):
        return {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "mode": "set",
                "authenticationToken": token,
                "parameterValues": [
                    {
                        "id": parameter_id,
                        "value": value
                    }
                ]
            }
        }
    
    async def authenticate(self, websocket):
        await websocket.send(json.dumps(self.create_auth_token_request()))
        response = await websocket.recv()
        token = json.loads(response)["data"]["authenticationToken"]
        
        await websocket.send(json.dumps(self.create_auth_request(token)))
        await websocket.recv()
        
        await websocket.send(json.dumps(self.create_parameter_list_request(token)))
        await websocket.recv()
        
        return token
    
    async def set_mouth_open(self, websocket, token, value):
        request = self.create_parameter_injection_request(token, "MouthOpen", value)
        await websocket.send(json.dumps(request))
        
    def get_audio_from_text(self, text):
        response = requests.post(
            self.tts_url, 
            json={"text": text}, 
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            wav_io = io.BytesIO(response.content)
            return sf.read(wav_io)
        return None, None
    
    async def animate_mouth_with_audio(self, websocket, token, text):
        data, samplerate = self.get_audio_from_text(text)
        
        if data is None:
            return
            
        block_size = int(samplerate * 0.05)
        
        async def monitor_audio():
            for i in range(0, len(data), block_size):
                if i + block_size <= len(data):
                    block = data[i:i+block_size]
                    rms = np.sqrt(np.mean(block**2))
                    mouth_value = min(rms * 5, 1.0)
                    
                    await self.set_mouth_open(websocket, token, mouth_value)
                    
                await asyncio.sleep(0.05)
        
        sd.play(data, samplerate=samplerate)
        await monitor_audio()


async def main():
    api = VTubeStudioAPI()
    
    async with websockets.connect(api.websocket_url) as websocket:
        token = await api.authenticate(websocket)
        await api.animate_mouth_with_audio(
            websocket, 
            token, 
            "This is a test of the text-to-speech system with volume control."
        )


if __name__ == "__main__":
    asyncio.run(main())