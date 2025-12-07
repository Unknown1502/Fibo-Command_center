# 🚀 Quick Reference Guide - Generation API Enhancements

## 🎯 Quick Start

### Test All Improvements
```bash
cd backend
python test_generation.py
```

### View Performance Comparison
```bash
python show_improvements.py
```

---

## 📋 New Endpoints Cheat Sheet

### 1. Batch Generation
```bash
POST /api/generate/batch

# Example request
{
  "requests": [
    {"prompt": "A red car", "mode": "ai"},
    {"prompt": "A blue house", "mode": "manual", "camera_angle": "eye-level"}
  ],
  "parallel": true,
  "continue_on_error": true
}
```

### 2. Generation History
```bash
GET /api/generate/history?user_id=1&limit=50&offset=0&status=completed
```

### 3. Statistics
```bash
GET /api/generate/statistics?user_id=1&days=30
```

### 4. Cache Statistics
```bash
GET /api/generate/cache/stats
```

### 5. Clear Cache
```bash
DELETE /api/generate/cache
```

---

## ⚡ New Request Parameters

### Enhanced Single Generation
```json
{
  "prompt": "A luxury watch",
  "mode": "ai",
  "use_cache": true,      // NEW: Enable caching (default: true)
  "max_retries": 3,       // NEW: Retry attempts (default: 3)
  "camera_angle": "eye-level",
  "fov": "standard",
  "lighting": "studio",
  "color_palette": "vibrant",
  "composition": "rule-of-thirds",
  "style": "photorealistic"
}
```

---

## 📊 Enhanced Response Fields

```json
{
  "id": 101,
  "status": "completed",
  "image_url": "https://...",
  "parameters": {...},
  "quality_score": 0.95,
  "generation_time": 14.3,
  "reasoning": {...},
  "cached": false,        // NEW: Was this cached?
  "retry_count": 0        // NEW: How many retries?
}
```

---

## ✅ Valid Parameter Values

### mode
- `ai` - Automatic parameter selection
- `manual` - Explicit control

### camera_angle
- `eye-level`
- `low-angle`
- `high-angle`
- `dutch-tilt`
- `bird's-eye`

### fov
- `wide`
- `standard`
- `telephoto`

### lighting
- `natural`
- `studio`
- `dramatic`
- `golden-hour`
- `soft`
- `hard`

### color_palette
- `vibrant`
- `pastel`
- `monochrome`
- `warm`
- `cool`
- `neon`

### composition
- `rule-of-thirds`
- `centered`
- `dynamic`
- `minimal`

### style
- `photorealistic`
- `cinematic`
- `editorial`
- `commercial`

---

## 🧪 Testing Examples

### Test Single Generation
```python
import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/generate/",
            json={"prompt": "A luxury watch"}
        )
        print(response.json())

asyncio.run(test())
```

### Test Batch Generation
```python
async def test_batch():
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "http://localhost:8000/api/generate/batch",
            json={
                "requests": [
                    {"prompt": f"Image {i}"} for i in range(5)
                ],
                "parallel": True
            }
        )
        result = response.json()
        print(f"Successful: {result['successful']}/{result['total']}")

asyncio.run(test_batch())
```

### Check Statistics
```python
async def test_stats():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/generate/statistics",
            params={"user_id": 1, "days": 7}
        )
        stats = response.json()
        print(f"Success rate: {stats['success_rate']}%")
        print(f"Avg time: {stats['average_generation_time']}s")

asyncio.run(test_stats())
```

---

## 🐛 Common Issues & Solutions

### Issue: Cache not working
```bash
# Check cache stats
curl http://localhost:8000/api/generate/cache/stats

# Clear cache if needed
curl -X DELETE http://localhost:8000/api/generate/cache
```

### Issue: Too many retries
```json
{
  "prompt": "Test",
  "max_retries": 1  // Reduce for faster feedback
}
```

### Issue: Parameter validation fails
```bash
# Get valid parameters
curl http://localhost:8000/api/generate/parameters
```

---

## 📈 Monitoring Commands

### Check Recent Generations
```bash
curl "http://localhost:8000/api/generate/history?limit=10"
```

### Check Success Rate
```bash
curl "http://localhost:8000/api/generate/statistics?days=7" | jq '.success_rate'
```

### Check Cache Performance
```bash
curl "http://localhost:8000/api/generate/cache/stats" | jq '.'
```

### Check Average Generation Time
```bash
curl "http://localhost:8000/api/generate/statistics?days=7" | jq '.average_generation_time'
```

---

## 🎯 Best Practices

### ✅ DO
- Enable caching for repeated prompts
- Use batch generation for multiple images
- Set appropriate retry limits
- Monitor statistics weekly
- Validate parameters before sending

### ❌ DON'T
- Disable caching in production
- Use sequential batch processing unnecessarily
- Set max_retries too high (>3)
- Ignore validation errors
- Skip monitoring

---

## 📊 Performance Expectations

| Operation | Time | Cache Hit Rate |
|-----------|------|----------------|
| Single Gen (No Cache) | ~15s | N/A |
| Single Gen (Cached) | ~0.1s | 60-80% |
| Batch (3, Parallel) | ~15s | N/A |
| Batch (3, Sequential) | ~45s | N/A |
| History Query | <1s | N/A |
| Statistics | <2s | N/A |

---

## 🔧 Configuration

### Cache TTL
```python
# In generation.py
CACHE_TTL = timedelta(hours=1)  # Adjust as needed
```

### Max Batch Size
```python
# In BatchGenerationRequest
max_items=50  # Adjust in Pydantic model
```

### Retry Configuration
```python
# Default in GenerationRequest
max_retries: int = Field(default=3, ge=0, le=5)
```

---

## 📚 Documentation Files

1. **GENERATION_API_ENHANCEMENTS.md** - Complete feature documentation
2. **CODE_IMPROVEMENTS_SUMMARY.md** - Technical implementation details
3. **This file** - Quick reference guide
4. **test_generation.py** - Test suite with examples
5. **show_improvements.py** - Performance comparison

---

## 🚀 Deployment Checklist

- [ ] Run test suite: `python test_generation.py`
- [ ] Review all documentation
- [ ] Check for errors: No Python errors
- [ ] Verify backward compatibility
- [ ] Monitor cache hit rate after deployment
- [ ] Set up alerts for success rate < 90%
- [ ] Document any configuration changes

---

## 💡 Tips & Tricks

### Maximize Cache Hit Rate
```python
# Normalize prompts before sending
prompt = prompt.lower().strip()
```

### Optimize Batch Processing
```python
# Use parallel for independent images
{"parallel": True}  # 50% faster

# Use sequential for dependent images
{"parallel": False}  # Safer
```

### Monitor Health
```python
# Check every hour
stats = get_statistics(days=1)
if stats['success_rate'] < 95:
    alert()
```

---

**Last Updated**: December 7, 2025  
**Version**: 2.0.0  
**Status**: ✅ Production Ready
