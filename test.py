import win32com.client
import os

FILENAME = r"pptx_input\upload_file\test_20240807.pptx"

# Initialize PowerPoint application
powerpoint = win32com.client.Dispatch("PowerPoint.Application")
powerpoint.Visible = 1

try:
    # Open the presentation
    presentation = powerpoint.Presentations.Open(os.path.abspath(FILENAME))

    # Create output directory for images
    output_dir = os.path.join(os.getcwd(), r"C:\Users\DuyQD\Desktop\GenAI\test_script\pptx_input\pptx_images")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Export all slides as PNG images
    for i, slide in enumerate(presentation.Slides):
        # Save slide as PNG with the correct full path
        slide_image_path = os.path.join(output_dir, f"slide_{i + 1}.png")
        slide.Export(slide_image_path, "PNG")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the presentation and PowerPoint are closed properly
    presentation.Close()
    powerpoint.Quit()
