import pdfrw 
source = "hh.pdf"
destination = "output.pdf"
myTemplate = pdfrw.PdfReader(source)
MYKEY = '/Annots'
FIELDKEY = '/T'
VALUE_KEY = '/V'
RECTKEY = '/Rect'
SUB_KEY = '/Subtype'
WIDGET= '/Widget'
data = {

    "external_practitioner": "1508065129-L2-S12"
}
def fill_form(source, dest, data):
    myTemplate = pdfrw.PdfReader(source)
    for pg_number in myTemplate.pages:
        annots = pg_number[MYKEY]
        for annot in annots:
            print("annots:", annot)
            if annot[SUB_KEY] == WIDGET:
                if annot['/Parent'] and annot['/Parent'][FIELDKEY]:
                    key = annot['/Parent'][FIELDKEY][1:-1]
                    print("key:",key)
                    if key in data.keys():
                        if type(data[key]) == bool:
                            if data[key] == True:
                                # annot.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                                annot.update(pdfrw.PdfDict(V='Yes'))
                        else:
                            annot.update(pdfrw.PdfDict(AP=pdfrw.PdfName(f'{data[key]}')))
                            annot.update(pdfrw.PdfDict(V='{}'.format(data[key])))
                            annot.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
    pdfrw.PdfWriter().write(dest, myTemplate)
fill_form(source, destination, data)


# import pdfrw

def fill_pdf(pdf_template, form_data, output_path):
    template_pdf = pdfrw.PdfReader(pdf_template)
    annotations = template_pdf.pages[0]['/Annots']
    for annotation in annotations:
        
        if '/Parent' in annotation:
            print(annotation)
            field_name = annotation['/Parent']['/T']
            print("field_name",field_name)
            if field_name in form_data:
                field_value = '/'+form_data[field_name]
                print(field_value,annotation['/Parent']['/V'] )
                if field_value == annotation['/Parent']['/V']:
                    annotation.update(pdfrw.PdfDict(V=f'{field_value}'))
                    # annotation.update(pdfrw.PdfDict(V=pdfrw.PdfName(field_value)))
                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))

                    annotation.update(pdfrw.PdfDict(AP=pdfrw.PdfName(field_value)))


    pdfrw.PdfWriter().write(output_path, template_pdf)

# Example usage
# json_data = { "(external_practitioner)": "1508065129-L2-S12"}
# pdf_template = "hh.pdf"  # Replace with the path to your PDF form
# output_path = "filled_form.pdf"  # Replace with the desired output path

# fill_pdf(pdf_template, json_data, output_path)