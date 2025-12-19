import os
from PIL import Image

def optimize_images(max_width=800):
    """Resizes all images to a max width, keeping aspect ratio."""
    valid_exts = ('.jpg', '.jpeg', '.png')
    files = [f for f in os.listdir() if f.lower().endswith(valid_exts)]
    
    if not files:
        print("⚠️ No images found.")
        return

    output_dir = "optimized"
    os.makedirs(output_dir, exist_ok=True)

    print(f"🖼️ Optimizing {len(files)} images...")
    for filename in files:
        try:
            with Image.open(filename) as img:
                # Calculate new size
                ratio = max_width / float(img.size[0])
                new_height = int((float(img.size[1]) * float(ratio)))
                
                # Resize
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save
                save_path = os.path.join(output_dir, filename)
                img.save(save_path, quality=85, optimize=True)
                print(f"   ✅ Saved: {save_path}")
        except Exception as e:
            print(f"   ❌ Error {filename}: {e}")

if __name__ == "__main__":
    print("--- BULK IMAGE OPTIMIZER ---")
    optimize_images()
