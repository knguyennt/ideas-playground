import asyncio
import websockets
import json
"765c3e6dd3143bc7d61a5f8379e5b339273a1981c4a3a816ff7ee5512b7b3f57"

# request animation change: HotkeyTriggerRequest
"6988d4727d4d4e789c9e55a417b43f27" # idle
"66d8b01b25fb432b82e93903ed057301" # joy
"567913aee1da4e1899adb47277e4374f" # sad
async def connect_and_control():
    uri = "ws://localhost:8001"
    
    # You'll need a token, but for the first connection, you must request one
    # This is a simplified representation of the authentication process
    auth_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiToken": "YOUR_SAVED_TOKEN",
        "authenticationToken": "YOUR_SAVED_TOKEN",
        "pluginName": "MyPythonScript",
        "pluginDeveloper": "You",
        "requestID": "SomeUniqueID"
    }

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to VTube Studio.")
            
            # Send the authentication request
            await websocket.send(json.dumps(auth_request))
            
            # Listen for the authentication response
            response = await websocket.recv()
            print("Received response:", response)
            
            # After successful authentication, you can send other requests
            # For example, a request to trigger a hotkey:
            hotkey_request = {
                "apiName": "VTubeStudioPublicAPI",
                "requestID": "AnotherUniqueID",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyID": "some_hotkey_id_from_vts"
                }
            }
            await websocket.send(json.dumps(hotkey_request))

            hotkey_response = await websocket.recv()
            print("Hotkey response:", hotkey_response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(connect_and_control())