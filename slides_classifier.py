from unstructured.partition.pptx import partition_pptx

def slides_classifier(pptx, slide_class="organization"):
    # Open the pptx file and read its content
    with open(pptx, "rb") as f:
        elements = partition_pptx(file=f)  # Assuming partition_pptx returns slide elements
        processed_slides = set()
        content_headers = []  # Initialize a list to store headers for all slides

        # Extract slide headers
        for element in elements:
            if hasattr(element, 'text') and hasattr(element, 'metadata') and element.metadata.page_number:
                slide_number = element.metadata.page_number
                if slide_number not in processed_slides:
                    content_header = f"Slide {slide_number}: {element.text.strip()}\n"
                    content_headers.append((slide_number, content_header))  # Store as tuple (slide_number, header)
                    processed_slides.add(slide_number)  # Mark slide as processed

    # Step 1: Define keywords for each category
    category_keywords = {
        "organization": ["体制", "組織", "organization"],
        "schedule": ["スケジュール", "日程", "schedule"],
        "use_case": ["事例", "ユースケース", "Use Case"],
        # Add more categories and keywords as needed
    }

    # Initialize a dictionary to store categorized slides
    categorized_slides = {}

    # Step 2: Categorize slides based on keywords
    for slide_number, header in content_headers:
        # Default category if no match is found
        category = "Uncategorized"
        # Check each keyword for every category
        for cat, keywords in category_keywords.items():
            if any(keyword in header for keyword in keywords):
                category = cat
                break  # Stop checking other categories if a match is found

        # Append slide number to the corresponding category in the dictionary
        if category not in categorized_slides:
            categorized_slides[category] = []
        categorized_slides[category].append(slide_number)

    # Filter slides 
    if slide_class == "organization":
        # Return only the organization slides
        filtered_slides = {k: v for k, v in categorized_slides.items() if k == "organization"}
    elif slide_class == "schedule":
        # Return only the schedule slides
        filtered_slides = {k: v for k, v in categorized_slides.items() if k == "schedule"}
    elif slide_class == "use_case":
        # Return only the schedule slides
        filtered_slides = {k: v for k, v in categorized_slides.items() if k == "use_case"}
    #elif slide_class == "both":
        # Return all categorized slides
        #filtered_slides = categorized_slides
    else:
        # If an invalid value return all slides as uncategorized
        filtered_slides = {"Uncategorized": sum(categorized_slides.values(), [])}

    return filtered_slides