from flask import Flask,render_template,request
import pandas as pd
import csv,operator
import os

app = Flask(__name__)
ID =1
credit=50.0
ecommerce=0
food_del=0
medicine=0

@app.route('/')
def hello():
  return render_template('Payment_home.html')
#check for zip extention, correct columns and column count
@app.route('/shw_payment')
def paypage():
  return render_template('payment.html')
@app.route('/txnupload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        amount = request.form["amount"]
        domain = request.form["domain"]
        global ecommerce
        global food_del
        global medicine
        if domain=='E-commerce':
          ecommerce= ecommerce+1
        elif domain == 'Food Delivery':
          food_del = food_del+1
        else:
          medicine= medicine+1
        #print(amount)
        #print(domain)
        transactions = pd.read_csv('txns.csv')
        #transactions = transactions.iloc[:,0:-1]
        transactions=transactions.append({'ID':ID, 'Amount':amount, 'Domain':domain},ignore_index=True)
        #print(transactions)
        global credit
        print(credit)
        credit = credit+ 0.03*int(amount)
        print(credit)
        transactions.to_csv('txns.csv',index=False)
        return  '<script>alert("payment successful!!");</script>'+render_template('Payment_home.html')

@app.route('/rewards')
def create_rewards():
  filename = 'Coupons.csv'
  table = ""
  tr = ""
  table += '<table border=1 cellpadding=1 id="example" style="width:100%" class="table table-striped table-bordered"><tr> <th>id</th> <th>name</th><th>value</th><th>credit points</th><th>domain</th></tr>'
  

  with open(filename, 'r') as csvfile:
      datareader = csv.reader(csvfile)
      print('old')
      print(datareader)
      sortedlist = sorted(datareader, key=operator.itemgetter(3), reverse=False)
      global credit
      print(credit)
      print('new')
      print(sortedlist)
    
      for row in sortedlist:
          #print(row)
          #print(row[0])
          Coup_id = row[0]       
          company = row [1]
          value = int(row[2])
          credit1=int(row[3])
          domain=row[4]

          if credit >= credit1: 
              tr += "<tr style='color:green'>"
              tr += "<td>%s</td>" % Coup_id
              tr  += "<td>%s</td>" % company
              tr += "<td>%s</td>" % value   
              tr += "<td>%s</td>" % credit1 
              tr += "<td>%s</td>" % domain 
              
                     
              tr += "</tr>"
          else:
              tr += "<tr style='color:red'>"
              tr += "<td>%s</td>" % Coup_id
              tr += "<td>%s</td>" % company
              tr += "<td>%s</td>" % value            
              tr += "<td>%s</td>" % credit1 
              tr += "<td>%s</td>" % domain 
              tr += "</tr>"

  end = '</table></div></div></div></div></div></div></body></html>'
  html = table + tr + end
  os.remove("templates/final1.html")
  files = open("templates/final1.html", "w")
  files.write(html)
  files.close()        
  return render_template('reward_start.html')+render_template('final1.html')

if(__name__)=='__main__':
    app.run(debug=True)