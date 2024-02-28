# from fillpdf import fillpdfs
import pdfrw
ANNOT_KEY = '/Annots'               # key for all annotations within a page
ANNOT_FIELD_KEY = '/T'              # Name of field. i.e. given ID of field
ANNOT_FORM_type = '/FT'             # Form type (e.g. text/button)
ANNOT_FORM_button = '/Btn'          # ID for buttons, i.e. a checkbox
ANNOT_FORM_text = '/Tx'             # ID for textbox
ANNOT_FORM_options = '/Opt'
ANNOT_FORM_combo = '/Ch'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
ANNOT_FIELD_PARENT_KEY = '/Parent'  # Parent key for older pdf versions
ANNOT_FIELD_KIDS_KEY = '/Kids'      # Kids key for older pdf versions
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
# fillpdfs.print_form_fields("GPC_test_v5.pdf")
# print(f)

data_dict ={'patient.email': 'email',  
            'first_available':'On'  
}



def convert_dict_values_to_string(dictionary):
    """
    Converts dictionary values to string including arrays and tuples.
    Parameters
    ---------
    dictionary: dict
        Any single level dictionary. Specifically made for the data_dict returned from
        the function get_form_fields() from the fillpdf library
    Returns
    ---------
    res: dict
        The resulting dictionary with only string values.
    """
    list_delim, tuple_delim = '-', '^'
  
    res = dict()
    for sub in dictionary:

        # checking data types
        if isinstance(dictionary[sub], list):
            res[sub] = dictionary[sub]
        elif isinstance(dictionary[sub], tuple):
            res[sub] = tuple_delim.join(list([str(ele) for ele in dictionary[sub]]))
        else:
            res[sub] = str(dictionary[sub])
            
    return res    
# If you want it flattened:
# fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict, flatten=False):
    """
    Writes the dictionary values to the pdf. Currently supports text and buttons.
    Does so by updating each individual annotation with the contents of the dat_dict.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want to flatten.
    output_pdf_path: str
        Path of the new pdf that is generated.
    data_dict: dict
        The data_dict returned from the function get_form_fields()
    flatten: bool
        Default is False meaning it will stay editable. True means the annotations
        will be uneditable.
    Returns
    ---------
    """
    data_dict = convert_dict_values_to_string(data_dict)
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for Page in template_pdf.pages:
        if Page[ANNOT_KEY]:
            print('annot key')
            for annotation in Page[ANNOT_KEY]:
                print(annotation)
                target = annotation if annotation[ANNOT_FIELD_KEY] else annotation[ANNOT_FIELD_PARENT_KEY]
                if annotation[ANNOT_FORM_type] == None:
                    pass
                if target and annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    key = target[ANNOT_FIELD_KEY][1:-1] # Remove parentheses
                    target_aux = target
                    while target_aux['/Parent']:
                        key = target['/Parent'][ANNOT_FIELD_KEY][1:-1] + '.' + key
                        target_aux = target_aux['/Parent']
                    if key in data_dict.keys():
                        if target[ANNOT_FORM_type] == ANNOT_FORM_button:
                            # button field i.e. a radiobuttons
                            if not annotation['/T']:
                                if annotation['/AP']:
                                    keys = annotation['/AP']['/N'].keys()
                                    if keys[0]:
                                        if keys[0][0] == '/':
                                            keys[0] = str(keys[0][1:])
                                    list_delim, tuple_delim = '-', '^'
                                    res = dict()
                                    for sub in data_dict:
                                        if isinstance(data_dict[sub], list):
                                            res[sub] = list_delim.join([str(ele) for ele in data_dict[sub]]) 
                                        else:
                                            res[sub] = str(data_dict[sub])
                                    temp_dict = res
                                    annotation = annotation['/Parent']
                                    options = []
                                    for each in annotation['/Kids']:
                                        keys2 = each['/AP']['/N'].keys()
                                        if '/Off' in keys2:
                                            keys2.remove('/Off')
                                        if ['/Off'] in keys:
                                            keys2.remove('/Off')
                                        export = keys2[0]
                                        if '/' in export:
                                            options.append(export[1:])
                                        else:
                                            options.append(export)
                                        if f'/{data_dict[key]}' == export:
                                            val_str = pdfrw.objects.pdfname.BasePdfName(f'/{data_dict[key]}')
                                        else:
                                            val_str = pdfrw.objects.pdfname.BasePdfName(f'/Off')
                                        if set(keys).intersection(set(temp_dict.values())):
                                            each.update(pdfrw.PdfDict(AS=val_str))
                                    if data_dict[key] not in options:
                                        if data_dict[key] != "None"  and data_dict[key] != "":
                                            raise KeyError(f"{data_dict[key]} Not An Option, Options are {options}")
                                    else:
                                        if set(keys).intersection(set(temp_dict.values())):
                                            annotation.update(pdfrw.PdfDict(V=pdfrw.objects.pdfname.BasePdfName(f'/{data_dict[key]}')))
                            else:
                                # button field i.e. a checkbox
                                target.update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                                if target[ANNOT_FIELD_KIDS_KEY]:
                                    target[ANNOT_FIELD_KIDS_KEY][0].update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                        elif target[ANNOT_FORM_type] == ANNOT_FORM_combo:
                            # Drop Down Combo Box
                            export = None
                            options = annotation[ANNOT_FORM_options]
                            if len(options) > 0:
                                if type(options[0]) == pdfrw.objects.pdfarray.PdfArray:
                                    options = list(options)
                                    options = [pdfrw.objects.pdfstring.PdfString.decode(x[0]) for x in options]
                                if type(options[0]) == pdfrw.objects.pdfstring.PdfString:
                                    options = [pdfrw.objects.pdfstring.PdfString.decode(x) for x in options]
                            if type(data_dict[key]) == list:
                                export = []
                                for each in options:
                                    if each in data_dict[key]:
                                        export.append(pdfrw.objects.pdfstring.PdfString.encode(each))
                                if export is None:
                                    if data_dict[key] != "None"  and data_dict[key] != "":
                                        raise KeyError(f"{data_dict[key]} Not An Option For {annotation[ANNOT_FIELD_KEY]}, Options are {options}")
                                pdfstr = pdfrw.objects.pdfarray.PdfArray(export)
                            else:
                                for each in options:
                                    if each == data_dict[key]:
                                        export = each
                                if export is None:
                                    if data_dict[key] != "None" and data_dict[key] != "":
                                        raise KeyError(f"{data_dict[key]} Not An Option For {annotation[ANNOT_FIELD_KEY]}, Options are {options}")
                                pdfstr = pdfrw.objects.pdfstring.PdfString.encode(data_dict[key])
                            annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr))
                        elif target[ANNOT_FORM_type] == ANNOT_FORM_text:
                            # regular text field
                            target.update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
                            if target[ANNOT_FIELD_KIDS_KEY]:
                                target[ANNOT_FIELD_KIDS_KEY][0].update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
                if flatten == True:
                    annotation.update(pdfrw.PdfDict(Ff=1))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


write_fillable_pdf('GPC_test_v5.pdf', 'new2.pdf', data_dict)