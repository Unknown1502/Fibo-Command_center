"""
Test script for generation API improvements
Tests all new features: caching, retry logic, batch generation, statistics
"""
import asyncio
import httpx
import json
from datetime import datetime


BASE_URL = "http://localhost:8000/api/generate"


async def test_single_generation():
    """Test single generation with all new features"""
    print("\n🧪 Testing Single Generation...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test with AI mode
        response = await client.post(
            f"{BASE_URL}/",
            json={
                "prompt": "A luxury watch on a marble table",
                "mode": "ai",
                "use_cache": True,
                "max_retries": 2
            }
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generation successful!")
            print(f"   - Image URL: {result['image_url'][:50]}...")
            print(f"   - Quality Score: {result['quality_score']}")
            print(f"   - Generation Time: {result['generation_time']}s")
            print(f"   - Cached: {result['cached']}")
            print(f"   - Retries: {result['retry_count']}")
            return result
        else:
            print(f"❌ Failed: {response.text}")
            return None


async def test_cache_hit():
    """Test that caching works"""
    print("\n🧪 Testing Cache Hit...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Make the same request twice
        request_data = {
            "prompt": "A smartphone with a sleek design",
            "mode": "manual",
            "camera_angle": "eye-level",
            "lighting": "studio",
            "style": "photorealistic",
            "use_cache": True
        }
        
        # First request (should miss cache)
        print("First request (cache miss expected)...")
        start1 = datetime.utcnow()
        response1 = await client.post(f"{BASE_URL}/", json=request_data)
        time1 = (datetime.utcnow() - start1).total_seconds()
        
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"✅ First request: {time1:.2f}s, cached={result1['cached']}")
        
        # Second request (should hit cache)
        print("Second request (cache hit expected)...")
        start2 = datetime.utcnow()
        response2 = await client.post(f"{BASE_URL}/", json=request_data)
        time2 = (datetime.utcnow() - start2).total_seconds()
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Second request: {time2:.2f}s, cached={result2['cached']}")
            
            if result2['cached'] and time2 < time1:
                print(f"🎉 Cache is working! {((time1 - time2) / time1 * 100):.1f}% faster")
            else:
                print("⚠️ Cache might not be working as expected")


async def test_parameter_validation():
    """Test parameter validation"""
    print("\n🧪 Testing Parameter Validation...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test invalid mode
        response = await client.post(
            f"{BASE_URL}/",
            json={
                "prompt": "Test image",
                "mode": "invalid_mode"
            }
        )
        
        if response.status_code == 422:
            print("✅ Invalid mode rejected correctly")
        else:
            print(f"❌ Expected 422, got {response.status_code}")
        
        # Test invalid camera angle
        response = await client.post(
            f"{BASE_URL}/",
            json={
                "prompt": "Test image",
                "mode": "manual",
                "camera_angle": "invalid_angle"
            }
        )
        
        if response.status_code == 422:
            print("✅ Invalid camera_angle rejected correctly")
        else:
            print(f"❌ Expected 422, got {response.status_code}")
        
        # Test prompt too short
        response = await client.post(
            f"{BASE_URL}/",
            json={
                "prompt": "ab"  # Too short (min 3 chars)
            }
        )
        
        if response.status_code == 422:
            print("✅ Short prompt rejected correctly")
        else:
            print(f"❌ Expected 422, got {response.status_code}")


async def test_batch_generation():
    """Test batch generation"""
    print("\n🧪 Testing Batch Generation...")
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        # Create batch request
        batch_request = {
            "requests": [
                {
                    "prompt": "A red sports car",
                    "mode": "manual",
                    "camera_angle": "low-angle",
                    "lighting": "dramatic",
                    "style": "cinematic"
                },
                {
                    "prompt": "A peaceful garden",
                    "mode": "manual",
                    "camera_angle": "eye-level",
                    "lighting": "natural",
                    "style": "photorealistic"
                },
                {
                    "prompt": "A futuristic city",
                    "mode": "manual",
                    "camera_angle": "high-angle",
                    "lighting": "neon",
                    "style": "cinematic"
                }
            ],
            "parallel": True,
            "continue_on_error": True
        }
        
        print(f"Generating {len(batch_request['requests'])} images in parallel...")
        start = datetime.utcnow()
        
        response = await client.post(
            f"{BASE_URL}/batch",
            json=batch_request
        )
        
        elapsed = (datetime.utcnow() - start).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch completed in {elapsed:.2f}s")
            print(f"   - Total: {result['total']}")
            print(f"   - Successful: {result['successful']}")
            print(f"   - Failed: {result['failed']}")
            
            for i, res in enumerate(result['results']):
                if res:
                    print(f"   - Image {i+1}: {res['image_url'][:50]}...")
                else:
                    print(f"   - Image {i+1}: Failed - {result['errors'][i]}")
        else:
            print(f"❌ Batch failed: {response.text}")


async def test_generation_history():
    """Test generation history endpoint"""
    print("\n🧪 Testing Generation History...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/history",
            params={"user_id": 1, "limit": 10}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {len(result['results'])} generations")
            print(f"   - Total in database: {result['total']}")
            
            if result['results']:
                latest = result['results'][0]
                print(f"   - Latest: {latest['prompt'][:50]}... ({latest['status']})")
        else:
            print(f"❌ Failed: {response.text}")


async def test_statistics():
    """Test statistics endpoint"""
    print("\n🧪 Testing Statistics...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/statistics",
            params={"user_id": 1, "days": 7}
        )
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics retrieved successfully")
            print(f"   - Total generations (7 days): {stats['total_generations']}")
            print(f"   - Average generation time: {stats['average_generation_time']}s")
            print(f"   - Average quality score: {stats['average_quality_score']}")
            print(f"   - Success rate: {stats['success_rate']}%")
            print(f"   - Status breakdown: {stats['status_breakdown']}")
            print(f"   - Mode breakdown: {stats['mode_breakdown']}")
        else:
            print(f"❌ Failed: {response.text}")


async def test_cache_stats():
    """Test cache statistics"""
    print("\n🧪 Testing Cache Statistics...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/cache/stats")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Cache stats retrieved")
            print(f"   - Total cached: {stats['total_cached']}")
            print(f"   - Valid: {stats['valid']}")
            print(f"   - Expired: {stats['expired']}")
            print(f"   - TTL: {stats['ttl_hours']} hours")
        else:
            print(f"❌ Failed: {response.text}")


async def test_clear_cache():
    """Test cache clearing"""
    print("\n🧪 Testing Cache Clear...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.delete(f"{BASE_URL}/cache")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Cache cleared: {result['cleared']} items")
        else:
            print(f"❌ Failed: {response.text}")


async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 FIBO Generation API - Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Test basic functionality
        await test_single_generation()
        
        # Test parameter validation
        await test_parameter_validation()
        
        # Test caching
        await test_cache_hit()
        
        # Test batch generation (commented out by default - takes time)
        # await test_batch_generation()
        
        # Test history and statistics
        await test_generation_history()
        await test_statistics()
        
        # Test cache management
        await test_cache_stats()
        await test_clear_cache()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
