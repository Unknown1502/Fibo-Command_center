"""
Download all generated images from manifest.json to local files
"""

import json
import requests
from pathlib import Path
from urllib.parse import urlparse

def download_images():
    # Load manifest
    manifest_path = Path("examples/manifest.json")
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print("📥 Downloading images from CloudFront...\n")
    
    total = len(manifest['images'])
    downloaded = 0
    
    for i, image_data in enumerate(manifest['images'], 1):
        category = image_data['category']
        name = image_data['name']
        url = image_data['image_url']
        
        # Create category directory
        category_dir = Path(f"examples/{category}")
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Download image
        output_path = category_dir / f"{name}.png"
        
        if output_path.exists():
            print(f"⏭️  [{i}/{total}] Skipping {category}/{name}.png (already exists)")
            downloaded += 1
            continue
        
        try:
            print(f"⬇️  [{i}/{total}] Downloading {category}/{name}.png...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = output_path.stat().st_size / 1024
            print(f"✅ Saved {output_path} ({file_size:.1f} KB)")
            downloaded += 1
            
        except Exception as e:
            print(f"❌ Failed to download {name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✅ Downloaded {downloaded}/{total} images")
    print(f"📁 Images saved to examples/ directory:")
    print(f"   • examples/ecommerce/ - {manifest['categories']['ecommerce']} images")
    print(f"   • examples/social/ - {manifest['categories']['social']} images")
    print(f"   • examples/games/ - {manifest['categories']['games']} images")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    download_images()
