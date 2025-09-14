import requests
import json

def test_playlist_endpoints():
    base_url = "http://localhost:5000"
    
    print("Testing playlist endpoints...")
    
    # Test list_playlists
    try:
        response = requests.get(f"{base_url}/list_playlists")
        print(f"List Playlists - Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()
    except Exception as e:
        print(f"Error testing list_playlists: {e}")
    
    # Test create_playlist
    try:
        response = requests.post(f"{base_url}/create_playlist", 
                               json={"name": "Test Playlist"})
        print(f"Create Playlist - Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()
    except Exception as e:
        print(f"Error testing create_playlist: {e}")
    
    # Test list_music with playlist
    try:
        response = requests.get(f"{base_url}/list_music?playlist=Test Playlist")
        print(f"List Music with Playlist - Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()
    except Exception as e:
        print(f"Error testing list_music with playlist: {e}")

if __name__ == "__main__":
    test_playlist_endpoints()

