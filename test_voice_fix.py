#!/usr/bin/env python3
"""
Test script to verify voice loading fix
"""
import requests
import json

def test_voice_endpoint():
    """Test the /voices endpoint"""
    print("🧪 Testing Voice Loading Fix...")
    print("=" * 50)
    
    try:
        # Test the /voices endpoint
        response = requests.get('http://localhost:7000/voices')
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                voices = data['data']
                print(f"✅ Successfully loaded {len(voices)} voices:")
                for voice_id, voice_info in voices.items():
                    print(f"   - {voice_id}: {voice_info['name']}")
                return True
            else:
                print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to web interface. Make sure it's running on port 7000.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_voice_endpoint()
    print(f"\n{'✅ VOICE FIX SUCCESSFUL' if success else '❌ VOICE FIX FAILED'}") 