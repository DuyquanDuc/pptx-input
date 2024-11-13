import os
import win32com.client
import pythoncom

class PPTXProcessor:
    def __init__(self):
        self.output_dir = None
        self.pptx_path = None

    def process_pptx(self, file):
        """
        This function processes an uploaded PPTX file, saves it to a directory,
        processes it using PowerPoint, and returns both the output directory and PPTX path.

        Args:
        - file: The uploaded file object.

        Returns:
        - output_dir: PNG path, pptx_path: PPTX uploaded path
        """

        # Initialize COM libraries for PowerPoint automation
        pythoncom.CoInitialize()

        # Get the temporary file path
        temp_path = file.name
        print(f"file path: {temp_path}")

        # Initialize PowerPoint application
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = 1
        
        try:
            # Open the presentation
            presentation = powerpoint.Presentations.Open(os.path.abspath(temp_path))
        
            # Create output directory for images
            self.output_dir = os.path.join(os.getcwd(), r"C:\Users\DuyQD\Desktop\GenAI\test_script\pptx_input\pptx_images")
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            # Export all slides as PNG images
            for i, slide in enumerate(presentation.Slides):
                # Save slide as PNG
                slide_image_path = os.path.join(self.output_dir, f"slide_{i + 1}.png")
                slide.Export(slide_image_path, "PNG")
        except Exception as e:
            print(f"An error occurred while processing the PPTX file: {e}")
        finally:
            # Ensure the presentation and PowerPoint are closed properly
            presentation.Close()
            powerpoint.Quit()

        # Uninitialize COM libraries
        pythoncom.CoUninitialize()

        return self.output_dir, temp_path
