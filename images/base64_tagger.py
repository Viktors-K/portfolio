import base64
import os
import mimetypes

# === CONFIGURATION ===
input_folder = "D:\\Programming\\Repositories\\portfolio\\images\\debian_install" # Root folder to scan
output_file = "deb_b64_tags.txt" # File to save all <script> tags
# =====================

def image_to_base64_tag(filepath, folder_name):
    """Convert an image to a <script> tag with Base64 content."""
    mime_type, _ = mimetypes.guess_type(filepath)
    if not mime_type:
        mime_type = "application/octet-stream"

    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    image_name = os.path.splitext(os.path.basename(filepath))[0].replace(" ", "-").lower()
    folder_clean = folder_name.replace(" ", "-")

    file_id = f"img-{folder_clean}-{image_name}"

    tag = (
        f'<script type="text/plain" id="{file_id}">\n'
        f"data:{mime_type};base64,{encoded}\n"
        f"</script>\n\n"
    )
    return tag


def main():
    if not os.path.exists(input_folder):
        print(f"❌ Folder not found: {input_folder}")
        return

    output_lines = []

    # Walk through ALL subdirectories
    for root, dirs, files in os.walk(input_folder):
        folder_name = os.path.basename(root)

        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip non-files or weird entries
            if not os.path.isfile(filepath):
                continue

            print(f"Processing: {filepath}")

            tag = image_to_base64_tag(filepath, folder_name)
            output_lines.append(tag)

    if not output_lines:
        print("⚠️ No files found to process.")
        return

    with open(output_file, "w", encoding="utf-8") as out:
        out.writelines(output_lines)

    print(f"\n✅ Done! Saved Base64 tags to '{output_file}'")
    print("All images from ALL folders were processed.")


if __name__ == "__main__":
    main()
