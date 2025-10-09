import os
from PIL import Image

# Paths
input_folder = "D:\\Programming\\Repositories\\operetajsistemas\\os-md1\\images\\xp_install\\windowsxp"
output_folder = "D:\\Programming\\Repositories\\operetajsistemas\\os-md1\\images\\xp_install\\windowsxp_output"
quality = 60

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported formats
valid_exts = ('.jpg', '.jpeg', '.png')

# Loop through files
for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_exts):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Convert PNG to RGB if needed (to handle transparency)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        output_path = os.path.join(output_folder, filename)
        img.save(output_path, optimize=True, quality=quality)

        print(f"Compressed: {filename}")

print("✅ All images compressed and saved to:", output_folder)
