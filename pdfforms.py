# import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
def get_form_fields():
    reader = PdfReader("new.pdf")
    writer = PdfWriter()

    page = reader.pages[0]
    fields = reader.get_fields()
    print(fields)
    # writer.add_page(page)

    # writer.update_page_form_field_values(
    #     writer.pages[0], {"gender": "male"}
    # )

    # # write "output" to PyPDF2-output.pdf
    # with open("filled-out.pdf", "wb") as output_stream:
    #     writer.write(output_stream)

    #     # return jsonify({'form_fields': ff, "bytearray": file_data, "file_name": file_name})
get_form_fields()