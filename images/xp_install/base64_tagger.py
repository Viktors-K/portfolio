import base64
import os
import mimetypes

# === CONFIGURATION ===
input_folder = "thumb"         # Folder where your images are
output_file = "base64_tags.txt" # File to save the <script> tags

# =====================

def image_to_base64_tag(filepath, folder_name):
    """Convert an image to a <script> tag with Base64 content."""
    mime_type, _ = mimetypes.guess_type(filepath)
    if not mime_type:
        mime_type = "application/octet-stream"

    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    image_name = os.path.splitext(os.path.basename(filepath))[0].replace(" ", "-").lower()
    folder_clean = folder_name.replace(" ", "-")  # removed .lower()

    # Updated ID format
    file_id = f"img-{folder_clean}-{image_name}"

    tag = f'<script type="text/plain" id="{file_id}">\n'
    tag += f"data:{mime_type};base64,{encoded}\n"
    tag += "</script>\n\n"
    return tag


def main():
    if not os.path.exists(input_folder):
        print(f"❌ Folder not found: {input_folder}")
        return

    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    if not image_files:
        print("⚠️ No image files found in the folder.")
        return

    output_lines = []
    for filename in image_files:
        filepath = os.path.join(input_folder, filename)
        print(f"Processing: {filename}")
        output_lines.append(image_to_base64_tag(filepath, input_folder))

    with open(output_file, "w", encoding="utf-8") as out:
        out.writelines(output_lines)

    print(f"\n✅ Done! Saved Base64 tags to '{output_file}'")
    print("You can copy them directly into your HTML <head> section.")


if __name__ == "__main__":
    main()
