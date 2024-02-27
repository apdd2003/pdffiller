from fillpdf import fillpdfs

fillpdfs.print_form_fields("hh.pdf")
# print(f)
data_dict ={ "external_practitioner": "150806ddd5129-L2-S12"}

fillpdfs.write_fillable_pdf('hh.pdf', 'new.pdf', data_dict)

# If you want it flattened:
# fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')