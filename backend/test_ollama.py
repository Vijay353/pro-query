#!/usr/bin/env python3
"""
Diagnostic script to test Ollama connection.
Run this to verify Ollama is working before starting the backend.

Usage:
    python test_ollama.py
"""
import httpx
import json
import asyncio


async def test_ollama():
    """Test Ollama API endpoints."""
    
    print("=" * 60)
    print("Testing Ollama Connection")
    print("=" * 60)
    
    host = "http://localhost:11434"
    model = "llama3.2"
    
    # Test 1: Check if Ollama is running
    print("\n1️⃣  Testing if Ollama is running...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{host}/api/tags")
            if response.status_code == 200:
                print("   ✅ Ollama is running!")
                models = response.json().get("models", [])
                print(f"   📦 Available models: {len(models)}")
                for m in models:
                    print(f"      - {m.get('name')}")
            else:
                print(f"   ❌ Ollama returned status {response.status_code}")
                return
    except httpx.ConnectError:
        print("   ❌ Cannot connect to Ollama at http://localhost:11434")
        print("   💡 Start Ollama with: ollama serve")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Check if model is available
    print(f"\n2️⃣  Checking if model '{model}' is available...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{host}/api/tags")
            models = response.json().get("models", [])
            model_names = [m.get("name") for m in models]
            
            # Check exact match or partial match
            found = False
            for m in model_names:
                if model in m or m in model:
                    print(f"   ✅ Model found: {m}")
                    found = True
                    break
            
            if not found:
                print(f"   ❌ Model '{model}' not found")
                print(f"   💡 Pull it with: ollama pull {model}")
                return
    except Exception as e:
        print(f"   ❌ Error checking models: {e}")
        return
    
    # Test 3: Test /api/chat endpoint (new format)
    print("\n3️⃣  Testing /api/chat endpoint (new Ollama format)...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{host}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Say 'Hello from Ollama!' in exactly those words."
                        }
                    ],
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("message", {}).get("content", "")
                print(f"   ✅ /api/chat works!")
                print(f"   💬 Response: {answer[:100]}...")
                return True
            elif response.status_code == 404:
                print("   ⚠️  /api/chat endpoint not found (404)")
                print("   🔄 Trying old /api/generate endpoint...")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error with /api/chat: {e}")
    
    # Test 4: Test /api/generate endpoint (old format)
    print("\n4️⃣  Testing /api/generate endpoint (old Ollama format)...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{host}/api/generate",
                json={
                    "model": model,
                    "prompt": "Say 'Hello from Ollama!' in exactly those words.",
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "")
                print(f"   ✅ /api/generate works!")
                print(f"   💬 Response: {answer[:100]}...")
                print("\n   ⚠️  You're using an older Ollama version.")
                print("   💡 Update Ollama for better performance:")
                print("      https://ollama.ai/download")
                return True
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error with /api/generate: {e}")
    
    print("\n" + "=" * 60)
    print("❌ Tests Failed")
    print("=" * 60)
    return False


async def main():
    """Run tests."""
    success = await test_ollama()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ All Tests Passed!")
        print("=" * 60)
        print("\nYour Ollama setup is working correctly.")
        print("You can now start your backend with:")
        print("  uvicorn main:app --reload --port 8000")
    else:
        print("\n" + "=" * 60)
        print("🔧 Troubleshooting Steps")
        print("=" * 60)
        print("\n1. Make sure Ollama is running:")
        print("   ollama serve")
        print("\n2. Pull the model:")
        print("   ollama pull llama3.2")
        print("\n3. Check Ollama version:")
        print("   ollama --version")
        print("\n4. Update Ollama if needed:")
        print("   Visit: https://ollama.ai/download")


if __name__ == "__main__":
    asyncio.run(main())