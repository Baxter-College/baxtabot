import mammoth

wordDoc = "menu.docx"
outHTML = "testhtml.htm"
out = open(outHTML, 'w')


with open(wordDoc, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value # The generated HTML
    messages = result.messages # Any messages, such as warnings during conversion
    out.write(html)
out.close()