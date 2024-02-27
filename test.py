from pdfrw import PdfReader

def get_radio_button_fields(pdf_path):
    """
    Get radio button fields and their options from a PDF form.
    
    Args:
    - pdf_path: Path to the PDF file
    
    Returns:
    - A dictionary where keys are field names and values are lists of available options
    """
    radio_button_fields = {}
    pdf = PdfReader(pdf_path)

    for page in pdf.pages:
        if '/Annots' in page and page['/Annots']:
            for annot in page['/Annots']:
                obj = annot
                if obj and obj.get('/Subtype') == '/Widget':
                    field_name = obj.get('/Parent')
                    try:
                        print(field_name['/T'])
                        if field_name:
                            if field_name not in radio_button_fields:
                                radio_button_fields[field_name] = []
                            if '/T' in obj:
                                options = obj['/V']
                                if isinstance(options, dict):
                                    for key in options.keys():
                                        radio_button_fields[field_name].append(key[1:])
                                else:
                                    radio_button_fields[field_name].append(options[1:])
                        
                    except:
                        pass
                    # if field_name:
                    #     if field_name not in radio_button_fields:
                    #         radio_button_fields[field_name] = []
                    #     if '/AP' in obj:
                    #         options = obj['/AP']['/N']
                    #         if isinstance(options, dict):
                    #             for key in options.keys():
                    #                 radio_button_fields[field_name].append(key[1:])
                    #         else:
                    #             radio_button_fields[field_name].append(options[1:])
    
    return radio_button_fields

# Example usage
pdf_path = "hh.pdf"  # Replace with your PDF file path
radio_button_fields = get_radio_button_fields(pdf_path)

# Print the field names and available options
for field_name, options in radio_button_fields.items():
    print(f"Field Name: {field_name}")
    print("Options:")
    for option in options:
        print(f"- {option}")