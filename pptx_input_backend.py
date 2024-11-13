import os
from llm_response import response, parse_json, compiling_agent
from slides_classifier import slides_classifier
from process_pptx_input import PPTXProcessor

#Initiate an instance of PPTXProcessor
#processor = PPTXProcessor()
#output_dir, pptx_path = processor.process_pptx()

class PPTXOrchestrator:
    def __init__(self, file):
        """
        Initialize the PPTXOrchestrator with the uploaded file.
        
        Args:
        - file: The uploaded file object.
        """
        self.file = file
        self.cat = None
        self.processor = PPTXProcessor()  # Instantiate the processor
        self.output_dir, self.pptx_path = self.processor.process_pptx(file)
        self.all_responses_summary = None
        self.all_responses_json = None
        self.final_summary = None
        self.final_json = None
        self.slide_class = None

    def generate_summary(self):
        """Generate and store a compiled summary."""
        if self.final_summary is None:  # Only process if not already done
            all_responses_summary = ""
            for i, slide_image in enumerate(os.listdir(self.output_dir)):
                slide_image_path = os.path.join(self.output_dir, slide_image)
                slide_response = response(slide_image_path)  # Assuming response function takes image path as input
                all_responses_summary += f"Response for slide {i + 1}:\n{slide_response}\n\n"
            # Finalize the summary response
            self.final_summary = compiling_agent(all_responses_summary)
        return self.final_summary

    def generate_json(self, extract_fields, slide_class="organization"):
        """Generate and store a concatenated JSON response based on selected categories."""
        if self.final_json is None:  # Only process if not already done
            all_responses_json = ""
            
            # Call slides_classifier with the appropriate selection based on 'slide_class'
            categorized_slides = slides_classifier(self.pptx_path, slide_class=slide_class)
            
            # Determine slides to process based on the selection
            if slide_class == "schedule":
                slides_to_process = categorized_slides.get("schedule", [])
            elif slide_class == "organization":
                slides_to_process = categorized_slides.get("organization", [])
            elif slide_class == "use_case":
                slides_to_process = categorized_slides.get("use_case", [])
            else:
                # If an invalid value for 'slide_class' is given, process all slides as 'Uncategorized'
                slides_to_process = categorized_slides.get("Uncategorized", [])

            print(f"These slides are to be processed: {slides_to_process}")

            for i in slides_to_process:
                slide_image_path = os.path.join(self.output_dir, f"slide_{i}.png")
                if os.path.exists(slide_image_path):
                    # Pass slide_class to parse_json to customize the prompt
                    slide_json = parse_json(slide_image_path, extract_fields, slide_class=slide_class)
                    all_responses_json += f"Response for slide {i}:\n{slide_json}\n\n"
                else:
                    print(f"PNG file for slide {i} not found.")
            
            # Finalize the JSON response
            self.final_json = all_responses_json
            
        return self.final_json


    def orchestrator(self, extract_fields=None, output_mode="both", slide_class="both"):
        """
        Orchestrates the processing of the file and returns the desired output based on the mode.
        
        Args:
        - output_mode: "summary", "json", or "both" (default is "both")
        - cals: "organization", "schedule", or "both" (default is "both")
        
        Returns:
        - The requested output(s) as per the output_mode.
        """
        if output_mode == "summary":
            return self.generate_summary()
        elif output_mode == "json":
            return self.generate_json(slide_class=slide_class, extract_fields=extract_fields)
        else:
            return self.generate_summary(), self.generate_json(extract_fields, slide_class=slide_class)

    #Update method       
    def update_file(self, new_file):
        """
        Update the file being processed and reset the state.
        
        Args:
        - new_file: The new file object to process.
        """
        self.file = new_file
        self.output_dir, self.pptx_path = self.processor.process_pptx(new_file)
        self.all_responses_summary = None
        self.all_responses_json = None
        self.final_summary = None
        self.final_json = None

