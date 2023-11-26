
from flask import Flask,render_template,request
import datetime,jinja2,pdfkit
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('invoice_template.html')

@app.route('/gen', methods=['POST'])
def generate():
    # logo = request.form['logo']
    invoiceNum = request.form['invoiceNum']
    crDate = datetime.datetime.now().strftime("%d %B %Y")
    dueDate = request.form['dueDate']
    sndAdr = request.form['sndAdr']
    rcAdr = request.form['rcAdr']
    item1 = request.form['item1']
    item2 = request.form['item2']
    item3 = request.form['item3']
    price1 = request.form['price1']
    price2 = request.form['price2']
    price3 = request.form['price3']
    total = float(price1)+float(price2)+float(price3)

    ####################

    context = { 'invoiceNum':invoiceNum,
                'crDate':crDate,
                'dueDate':dueDate,
                'sndAdr':sndAdr,
                'rcAdr':rcAdr,
                'item1':item1,
                'item':item2,
                'item3':item3,
                'price1':price1,
                'price2':price2,
                'price3':price3,
                'total':total
            }

    template_loader = jinja2.FileSystemLoader('./templates')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'invoice_gen.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    try:
        config = pdfkit.configuration(wkhtmltopdf='./wkhtmltopdf.exe')
        output_pdf = invoiceNum+crDate+'.pdf'
        pdfkit.from_string(output_text, output_pdf, configuration=config, css='style.css')
    except Exception as e:
        app.logger.error(e)



    # or current_app.logger.error(e)
    # config = pdfkit.configuration(wkhtmltopdf='./wkhtmltopdf.exe')
    # output_pdf = 'pdf_generate.pdf'
    # pdfkit.from_string(output_text, output_pdf, configuration=config, css='style.css')

    ####################

    return render_template('invoice_gen.html',invoiceNum=invoiceNum,
                                              crDate=crDate,
                                              dueDate=dueDate,
                                              sndAdr=sndAdr,
                                              rcAdr=rcAdr,
                                              item1=item1,
                                              item=item2,
                                              item3=item3,
                                              price1=price1,
                                              price2=price2,
                                              price3=price3,
                                              total=total)

