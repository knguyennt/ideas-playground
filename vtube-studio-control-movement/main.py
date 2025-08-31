import asyncio
import json
import io
from urllib import response
import requests
import websockets
import sounddevice as sd
import soundfile as sf
import numpy as np
import  gradio as gr
from openai import OpenAI

openai_client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lmstudilo")

# Global VTubeStudio connection
vtube_api = None
vtube_websocket = None
vtube_token = None
animation_lock = asyncio.Lock()  # Prevent concurrent animations
connection_health_task = None  # Background task for connection health monitoring

async def monitor_connection_health():
    """Background task to monitor WebSocket health"""
    global vtube_websocket, vtube_token
    
    while True:
        try:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            if is_websocket_open(vtube_websocket):
                try:
                    # Send a ping to keep connection alive
                    await vtube_websocket.ping()
                except Exception as e:
                    print(f"Health check ping failed: {e}")
                    # Connection seems dead, clean it up
                    await cleanup_vtube_connection()
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in connection health monitor: {e}")

def is_websocket_open(websocket):
    """Check if websocket is open and ready for communication"""
    if websocket is None:
        return False
    
    # For newer websockets versions
    if hasattr(websocket, 'closed'):
        return not websocket.closed
    
    # For older websockets versions
    if hasattr(websocket, 'state'):
        return websocket.state.name == 'OPEN'
    
    # Fallback - assume it's open if we can't determine
    return True

async def initialize_vtube_connection():
    global vtube_api, vtube_websocket, vtube_token, connection_health_task
    
    # Check if websocket needs to be created or reconnected
    if not is_websocket_open(vtube_websocket):
        try:
            vtube_api = VTubeStudioAPI()
            
            # More aggressive keepalive settings for long operations
            vtube_websocket = await asyncio.wait_for(
                websockets.connect(
                    vtube_api.websocket_url, 
                    ping_interval=20,  # Send ping every 20 seconds
                    ping_timeout=20,   # Wait 20 seconds for pong
                    close_timeout=10,  # Close timeout
                    max_size=10*1024*1024,  # 2MB message size limit
                    max_queue=64,      # Larger queue for animation data
                    compression=None   # Disable compression for better performance
                ),
                timeout=100  # 100 second connection timeout
            )
            
            vtube_token = await vtube_api.authenticate(vtube_websocket)
            print("Successfully connected to VTube Studio")
            
            # Start health monitoring if not already running
            if connection_health_task is None or connection_health_task.done():
                connection_health_task = asyncio.create_task(monitor_connection_health())
            
        except asyncio.TimeoutError:
            print("Timeout connecting to VTube Studio")
            vtube_websocket = None
            vtube_token = None
            raise
        except Exception as e:
            print(f"Failed to connect to VTube Studio: {e}")
            vtube_websocket = None
            vtube_token = None
            raise
    
    return vtube_websocket, vtube_token

async def cleanup_vtube_connection():
    global vtube_websocket, vtube_token, connection_health_task
    
    # Cancel health monitoring task
    if connection_health_task and not connection_health_task.done():
        connection_health_task.cancel()
        try:
            await connection_health_task
        except asyncio.CancelledError:
            pass
    
    if is_websocket_open(vtube_websocket):
        try:
            await vtube_websocket.close()
        except Exception as e:
            print(f"Error closing websocket: {e}")
    vtube_websocket = None
    vtube_token = None

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
        try:
            await websocket.send(json.dumps(self.create_auth_token_request()))
            response = await websocket.recv()
            token = json.loads(response)["data"]["authenticationToken"]
            
            await websocket.send(json.dumps(self.create_auth_request(token)))
            await websocket.recv()
            
            await websocket.send(json.dumps(self.create_parameter_list_request(token)))
            await websocket.recv()
            
            return token
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed during authentication")
            raise
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise
    
    async def set_mouth_open(self, websocket, token, value):
        try:
            # Check if websocket is still open before sending
            if not is_websocket_open(websocket):
                raise websockets.exceptions.ConnectionClosed(None, None)
                
            request = self.create_parameter_injection_request(token, "MouthOpen", value)
            
            # Add timeout to prevent hanging on slow sends
            await asyncio.wait_for(
                websocket.send(json.dumps(request)),
                timeout=5.0  # 5 second timeout for sending
            )
            
            # Small delay to prevent overwhelming the connection
            await asyncio.sleep(0.1)  # 1ms delay
            
        except asyncio.TimeoutError:
            print("Timeout sending mouth parameter")
            raise websockets.exceptions.ConnectionClosed(None, None)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed while setting mouth parameter")
            raise
        except Exception as e:
            print(f"Failed to set mouth parameter: {e}")
            raise
        
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
        # Limit text length to prevent overly long animations
        if len(text) > 1000:
            print(f"Text too long ({len(text)} chars), truncating to 1000 characters")
            text = text[:1000] + "..."
        
        data, samplerate = self.get_audio_from_text(text)
        
        if data is None:
            return
            
        block_size = int(samplerate * 0.05)
        
        async def monitor_audio():
            print("monitor_audio_")
            last_mouth_value = 0
            consecutive_errors = 0
            max_errors = 5  # Allow up to 5 consecutive errors before giving up
            
            for i in range(0, len(data), block_size):
                try:
                    # Check connection before each operation
                    if not is_websocket_open(websocket):
                        print("WebSocket connection lost during animation")
                        break
                        
                    if i + block_size <= len(data):
                        block = data[i:i+block_size]
                        rms = np.sqrt(np.mean(block**2))
                        mouth_value = min(rms * 5, 1.0)
                        
                        # Only send if value changed significantly to reduce traffic
                        print("mouth_value: ", mouth_value)
                        print("last_mouth_value: ", last_mouth_value)
                        if abs(mouth_value - last_mouth_value) > 0.2:
                            await self.set_mouth_open(websocket, token, mouth_value)
                            last_mouth_value = mouth_value
                            consecutive_errors = 0  # Reset error count on success
                        
                    # Every 50 iterations (~2.5 seconds), send a keepalive ping
                    if i % (block_size * 50) == 0 and i > 0:
                        try:
                            await websocket.ping()
                        except Exception as e:
                            print(f"Keepalive ping failed: {e}")
                    
                    await asyncio.sleep(0.1)
                    
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed during mouth animation")
                    break
                except Exception as e:
                    consecutive_errors += 1
                    print(f"Error during mouth animation (attempt {consecutive_errors}): {e}")
                    if consecutive_errors >= max_errors:
                        print("Too many consecutive errors, stopping animation")
                        break
                    # Small delay before retrying
                    await asyncio.sleep(0.1)
                    
            # Reset mouth to closed position at the end
            try:
                if is_websocket_open(websocket):
                    await self.set_mouth_open(websocket, token, 0)
            except Exception as e:
                print(f"Error resetting mouth position: {e}")
        
        sd.play(data, samplerate=samplerate)
        await monitor_audio()



async def main(input, history):
    response = openai_client.chat.completions.create(
        model="miku",
        messages= history +  [{"role": "user", "content": input}]
    )
    res = response.choices[0].message.content
    
    async def animate_response():
        # Use lock to prevent concurrent animations
        async with animation_lock:
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    websocket, token = await initialize_vtube_connection()
                    await vtube_api.animate_mouth_with_audio(websocket, token, res)
                    break  # Success, exit retry loop
                    
                except websockets.exceptions.ConnectionClosed:
                    retry_count += 1
                    print(f"VTube Studio connection was closed, retry {retry_count}/{max_retries}")
                    await cleanup_vtube_connection()
                    
                    if retry_count < max_retries:
                        # Wait before retrying, with exponential backoff
                        wait_time = 2 ** retry_count
                        print(f"Waiting {wait_time} seconds before retry...")
                        await asyncio.sleep(wait_time)
                    else:
                        print("Max retries reached, giving up on animation")
                        
                except Exception as e:
                    retry_count += 1
                    print(f"Error during animation (retry {retry_count}/{max_retries}): {e}")
                    
                    if retry_count < max_retries:
                        await cleanup_vtube_connection()
                        await asyncio.sleep(1)
                    else:
                        print("Max retries reached, giving up on animation")
    
    asyncio.create_task(animate_response())
    return res

async def something():
    try:
        gr.ChatInterface(main, type="messages").launch()
    finally:
        # Clean up connections on exit
        await cleanup_vtube_connection()

if __name__ == "__main__":
    try:
        asyncio.run(something())
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        # Ensure cleanup runs
        try:
            asyncio.run(cleanup_vtube_connection())
        except Exception as e:
            print(f"Error during cleanup: {e}")