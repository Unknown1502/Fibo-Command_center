"""
FIBO Command Center - Example Image Generator
Generates 30 professional example images across 3 categories for demo
"""

import asyncio
import httpx
import json
from pathlib import Path
from datetime import datetime

# Color codes for output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Example prompts across 3 categories
EXAMPLES = {
    "ecommerce": [
        {
            "name": "luxury_watch",
            "prompt": "Professional product photography of a luxury gold watch on white marble surface, studio lighting, 45-degree angle, macro lens, f/2.8 aperture, dramatic shadows, DCI-P3 color space"
        },
        {
            "name": "smartphone",
            "prompt": "Premium smartphone in midnight black, floating on gradient background, side lighting, 30-degree angle, clean minimalist style, sharp focus, professional product shot"
        },
        {
            "name": "sneakers",
            "prompt": "White athletic sneakers on concrete surface, natural lighting, golden hour, 45-degree angle, street style photography, shallow depth of field"
        },
        {
            "name": "headphones",
            "prompt": "Wireless over-ear headphones in matte black, levitating shot, studio lighting with rim light, centered composition, premium product photography"
        },
        {
            "name": "sunglasses",
            "prompt": "Designer aviator sunglasses on wooden surface, warm lighting, 45-degree angle, lifestyle product shot, bokeh background"
        },
        {
            "name": "coffee_machine",
            "prompt": "Modern espresso machine in brushed steel, kitchen environment, soft window light, side angle, lifestyle photography, warm color palette"
        },
        {
            "name": "laptop",
            "prompt": "Gaming laptop open on desk, RGB keyboard backlight, dark moody lighting, 30-degree angle, tech product photography, cyberpunk aesthetic"
        },
        {
            "name": "perfume_bottle",
            "prompt": "Elegant perfume bottle with gold accents, black background, dramatic spotlight, centered composition, luxury product photography, reflections"
        },
        {
            "name": "camera",
            "prompt": "Mirrorless camera with lens, photographer's desk setup, natural window light, flat lay composition, professional gear photography"
        },
        {
            "name": "backpack",
            "prompt": "Modern travel backpack in navy blue, outdoor mountain background, natural daylight, adventure lifestyle photography, product in environment"
        }
    ],
    "social": [
        {
            "name": "coffee_lifestyle",
            "prompt": "Instagram-style coffee cup on wooden table, morning light through window, cozy cafe atmosphere, warm tones, lifestyle photography, bokeh background"
        },
        {
            "name": "fitness",
            "prompt": "Fitness flatlay with yoga mat, dumbbells, water bottle, and smartwatch, bright clean lighting, top-down view, healthy lifestyle aesthetic"
        },
        {
            "name": "food_gourmet",
            "prompt": "Gourmet burger with fries on rustic wooden board, natural lighting, close-up shot, food photography, appetizing presentation, shallow depth of field"
        },
        {
            "name": "travel_beach",
            "prompt": "Tropical beach sunset with palm trees, golden hour lighting, vibrant colors, travel photography, Instagram aesthetic, dreamy atmosphere"
        },
        {
            "name": "workspace",
            "prompt": "Modern minimalist workspace with laptop and coffee, clean white desk, plants, natural light, productivity aesthetic, flat lay photography"
        },
        {
            "name": "fashion_street",
            "prompt": "Urban street style fashion portrait, city background, golden hour, fashionable outfit, lifestyle photography, trendy aesthetic"
        },
        {
            "name": "party_celebration",
            "prompt": "Colorful party celebration with balloons and confetti, bright vibrant colors, festive atmosphere, social media content, joyful mood"
        },
        {
            "name": "pet_portrait",
            "prompt": "Adorable golden retriever portrait, outdoor natural lighting, green park background, pet photography, happy expression, bokeh effect"
        },
        {
            "name": "home_decor",
            "prompt": "Scandinavian interior design living room, natural light, plants, minimalist aesthetic, home decor inspiration, cozy atmosphere"
        },
        {
            "name": "adventure_hiking",
            "prompt": "Mountain hiking adventure landscape, dramatic sunset, epic outdoor photography, adventure travel content, inspiring vista"
        }
    ],
    "games": [
        {
            "name": "fantasy_sword",
            "prompt": "Legendary fantasy sword with glowing runes, dramatic lighting, medieval game asset, intricate details, magical blue glow, epic fantasy style"
        },
        {
            "name": "scifi_weapon",
            "prompt": "Futuristic energy rifle with neon accents, sci-fi game weapon, detailed tech design, holographic sights, cyberpunk style, glowing elements"
        },
        {
            "name": "magic_potion",
            "prompt": "Mystical healing potion bottle with glowing green liquid, fantasy game item, magical particles, ornate glass design, RPG asset style"
        },
        {
            "name": "armor_knight",
            "prompt": "Detailed knight armor set with golden trim, medieval fantasy, battle-worn metal, epic game asset, heroic presentation"
        },
        {
            "name": "treasure_chest",
            "prompt": "Ancient treasure chest overflowing with gold coins and gems, fantasy RPG asset, detailed wood carving, dramatic lighting, rich colors"
        },
        {
            "name": "robot_character",
            "prompt": "Advanced combat robot character, sci-fi game design, metallic blue and silver, LED lights, futuristic military style, detailed mechanics"
        },
        {
            "name": "crystal_gem",
            "prompt": "Magical glowing crystal gem floating, purple and blue energy, fantasy game resource, ethereal glow, mystical particles"
        },
        {
            "name": "spaceship_interior",
            "prompt": "Futuristic spaceship cockpit interior, holographic displays, sci-fi game environment, neon lighting, detailed control panels, cyberpunk aesthetic"
        },
        {
            "name": "dragon_scales",
            "prompt": "Dragon scale armor texture, fantasy game material, iridescent colors, detailed reptilian pattern, mystical sheen, close-up detail shot"
        },
        {
            "name": "cyberpunk_city",
            "prompt": "Neon-lit cyberpunk city street at night, futuristic game environment, rain-soaked pavement, holographic billboards, dystopian atmosphere"
        }
    ]
}

async def generate_image(client, category, example, index, total):
    """Generate a single image"""
    url = "http://localhost:8000/api/generate/"
    
    print(f"{Colors.BLUE}🎨 [{index}/{total}] Generating {category}/{example['name']}...{Colors.END}")
    
    try:
        response = await client.post(
            url,
            json={
                "prompt": example['prompt'],
                "mode": "manual",
                "user_id": 1,
                "camera_angle": "45-degree",
                "lighting": "studio",
                "style": "photorealistic"
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"{Colors.GREEN}✅ [{index}/{total}] Success! Quality: {data.get('quality_score', 'N/A')}, Time: {data.get('generation_time', 'N/A')}s{Colors.END}")
            return {
                "category": category,
                "name": example['name'],
                "prompt": example['prompt'],
                "image_url": data.get('image_url'),
                "quality_score": data.get('quality_score'),
                "generation_time": data.get('generation_time'),
                "generation_id": data.get('id'),
                "timestamp": datetime.now().isoformat()
            }
        else:
            print(f"{Colors.RED}❌ [{index}/{total}] Failed: {response.status_code} - {response.text}{Colors.END}")
            return None
            
    except Exception as e:
        print(f"{Colors.RED}❌ [{index}/{total}] Error: {str(e)}{Colors.END}")
        return None

async def main():
    """Main function to generate all examples"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🎨 FIBO COMMAND CENTER - EXAMPLE IMAGE GENERATOR{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    # Create output directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    for category in ["ecommerce", "social", "games"]:
        (examples_dir / category).mkdir(exist_ok=True)
    
    print(f"{Colors.YELLOW}📁 Output directory: {examples_dir.absolute()}{Colors.END}")
    print(f"{Colors.YELLOW}🎯 Generating 30 images across 3 categories{Colors.END}")
    print(f"{Colors.YELLOW}⏱️  Estimated time: 10-15 minutes (~15 seconds per image){Colors.END}\n")
    
    # Count total images
    total_images = sum(len(examples) for examples in EXAMPLES.values())
    
    # Generate images
    results = []
    index = 0
    
    async with httpx.AsyncClient() as client:
        for category, examples in EXAMPLES.items():
            print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.BLUE}📂 Category: {category.upper()} ({len(examples)} images){Colors.END}")
            print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
            
            for example in examples:
                index += 1
                result = await generate_image(client, category, example, index, total_images)
                if result:
                    results.append(result)
                
                # Small delay between requests
                if index < total_images:
                    await asyncio.sleep(1)
    
    # Save manifest
    manifest_file = examples_dir / "manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_images": len(results),
            "categories": {
                "ecommerce": len([r for r in results if r['category'] == 'ecommerce']),
                "social": len([r for r in results if r['category'] == 'social']),
                "games": len([r for r in results if r['category'] == 'games'])
            },
            "images": results
        }, f, indent=2)
    
    # Print summary
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✨ GENERATION COMPLETE!{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.GREEN}📊 Summary:{Colors.END}")
    print(f"   Total images: {len(results)}/{total_images}")
    print(f"   E-commerce: {len([r for r in results if r['category'] == 'ecommerce'])} images")
    print(f"   Social media: {len([r for r in results if r['category'] == 'social'])} images")
    print(f"   Game assets: {len([r for r in results if r['category'] == 'games'])} images")
    
    if results:
        avg_quality = sum(r.get('quality_score', 0) for r in results if r.get('quality_score')) / len(results)
        avg_time = sum(r.get('generation_time', 0) for r in results if r.get('generation_time')) / len(results)
        print(f"   Average quality score: {avg_quality:.3f}")
        print(f"   Average generation time: {avg_time:.1f}s")
    
    print(f"\n{Colors.YELLOW}📁 Manifest saved: {manifest_file.absolute()}{Colors.END}")
    print(f"{Colors.YELLOW}📂 Images organized in: examples/ecommerce, examples/social, examples/games{Colors.END}\n")
    
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Generation interrupted by user{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}\n")
        import traceback
        traceback.print_exc()
