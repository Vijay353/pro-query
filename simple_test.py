"""
Test the exact API call format for your Ollama installation.
"""
import requests
import json

print("=" * 60)
print("TESTING DIFFERENT OLLAMA API FORMATS")
print("=" * 60)

host = "http://localhost:11434"
model = "llama3.2"  # Without :latest tag

# Test 1: Simple generate with minimal params
print("\n1️⃣  Testing minimal /api/generate...")
try:
    response = requests.post(
        f"{host}/api/generate",
        json={
            "model": model,
            "prompt": "Say hello",
            "stream": False
        }
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ WORKS!")
        result = response.json()
        print(f"   Response: {result.get('response', '')[:100]}")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: With latest tag
print("\n2️⃣  Testing with :latest tag...")
try:
    response = requests.post(
        f"{host}/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": "Say hello",
            "stream": False
        }
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ WORKS!")
        result = response.json()
        print(f"   Response: {result.get('response', '')[:100]}")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check what the /api/tags returns exactly
print("\n3️⃣  Checking exact model name from /api/tags...")
try:
    response = requests.get(f"{host}/api/tags")
    if response.status_code == 200:
        data = response.json()
        models = data.get("models", [])
        print(f"   Found {len(models)} models:")
        for m in models:
            name = m.get("name", "")
            print(f"   📦 {name}")
            print(f"      Exact name to use: '{name}'")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Try the exact model name from tags
print("\n4️⃣  Testing with EXACT model name from tags...")
try:
    # Get the exact name first
    response = requests.get(f"{host}/api/tags")
    if response.status_code == 200:
        models = response.json().get("models", [])
        if models:
            exact_name = models[0].get("name")
            print(f"   Using: {exact_name}")
            
            response = requests.post(
                f"{host}/api/generate",
                json={
                    "model": exact_name,
                    "prompt": "Say hello",
                    "stream": False
                }
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ WORKS!")
                result = response.json()
                print(f"   Response: {result.get('response', '')[:100]}")
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("Based on the test above, use the model name that WORKS")
print("in your .env file as OLLAMA_MODEL=")