import gradio as gr
from pptx_input_backend import PPTXOrchestrator

#Return file path
def path_file(files):
    file_paths = files.name
    return file_paths

#Call the backend function
def process_summary(file):
    # Call the first function to get the image content
    orchestrator_instance = PPTXOrchestrator(file) 
    content = orchestrator_instance.orchestrator(output_mode="summary")
    return content

#Call the backend function
def process_json(file, extract_json, slide_class):
    # Initialize the orchestrator instance with the provided file
    orchestrator_instance = PPTXOrchestrator(file)
    
    # Call the orchestrator with output_mode="json" and slide_class as cals
    content = orchestrator_instance.orchestrator(extract_json, output_mode="json", slide_class=slide_class)
    
    return content

#Example sector
examples = [
    ["schedule", "task_name, start_time, end_time"],
    ["organization", "member_name, member_role, percent_allocate"],
    ["use_case", "use_case_name, input, output"]]

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            file_output = gr.File()
            upload_file = gr.UploadButton("Upload a Powerpoint File", type='file')
            upload_file.upload(path_file, upload_file, file_output)
            slide_select = gr.Dropdown(label="Categories",choices=["organization", "schedule", "use_case", "Person CV"], info="Select slides type to Process")
            extract_json = gr.Textbox(label="Extract fields", placeholder="Example: name, role, percent_allocate")
        with gr.Column():
            summary_output = gr.Textbox(label="Summary")
            summary = gr.Button(value="Summary")
            json_output = gr.Textbox(label="JSON")
            json = gr.Button(value="Extract Json")
    # Bind the button click event to the function
    summary.click(
        fn=process_summary,
        inputs=[upload_file],
        outputs=[summary_output]
    )
    # Bind the button click event to the function
    json.click(
        fn=process_json,
        inputs=[upload_file, extract_json, slide_select],
        outputs=[json_output]
    )
    # Add image examples
    examples = gr.Examples(
        examples=examples,  
        inputs=[slide_select, extract_json],
        label="Examples"
    )


demo.launch()