
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    session,
    flash
)
from datetime import datetime as dt
from flask_mysqldb import MySQL
from form import (customerScreen, updateCustomer, 
deleteCustomer,withdrawMoney,
createaccount,deleteAccount,depositMoney,

customerStatusSearch,
accountStatusSearch,
accountSum,
login,
transferMoney)
from flask_mongoengine import MongoEngine
from config import Config
import sys
from model import Customer_Account,Transactions
#from model import Customer_Account


app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)



@app.route('/home',methods =['GET','POST'] )
def home():
    return render_template("base.html")

@app.route('/logout',methods =['GET','POST'] )
def logout_out():
    form = login()
    session['id']=False
    return redirect(url_for('login_enter'))





@app.route('/', methods =['GET','POST'] )
def login_enter():
    form = login()
    username  =form.username.data
    password = form.password.data
    print(username,file=sys.stderr)
    
    if username=="Tanjina" and password=="Tanjina":
        session["id"]=1
        return render_template("base.html")
    
    

    return render_template("login.html",form = form)
    
        
  
        
    


@app.route('/createcustomer', methods=['GET','POST'])

def customer():
    form = customerScreen()
    if form.validate_on_submit():
        
        ssn_id = form.ssn_id.data
        customer_name = form.customer_name.data
        age = form.age.data
        address = form.address.data
        state = form.state.data
        city = form.city.data
        if  Customer_Account.objects(ssn_id = ssn_id) and ssn_id.isnumeric():
                flash("Sorry Try Again !",'danger')

        else:
            customer = Customer_Account(ssn_id = ssn_id, customer_name = customer_name , age = age , address = address,
            state = state , city = city,account_type ="", s_m=0,c_m=0,message = "Customer Created Successfully" ,datetime =  str(dt.now()))
            customer.save()
            flash("You are successfully registered!",'success')
    return render_template("customer_screen.html",form=form)


@app.route('/profiles')
def pro():
    return render_template("profile.html")

@app.route('/update', methods=['GET','POST'])
def update_customer():
    l=[]
    form = updateCustomer()
    temp = form.customer_ssn_id.data
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id = temp):
            user =  Customer_Account.objects(ssn_id=temp).first()
        else:
            user=0
        
        new_customer_name = form.new_customer_name.data
        new_address = form.new_address.data
        new_age =  form.new_age.data
        if user!=0:
            Customer_Account.objects(ssn_id = temp).update(customer_name = new_customer_name , age = new_age , address = new_address,message = "Customer Updated Successfully",datetime =  str(dt.now()))
            flash("Customer Updation successful!",'success')
        else:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('update_customer.html',form = form, ssn_id = temp)

@app.route('/deletecustomer',methods=['GET','POST'])
def delete_customer():
        form = deleteCustomer()
        if form.validate_on_submit():
            ssn_id = form.ssn_id.data
            
            if Customer_Account.objects(ssn_id = ssn_id):
                
                
                Customer_Account.objects(ssn_id=ssn_id).delete()
                flash("Customer Deleted successful!",'success')
            else:
                flash("Customer with the given SSN_ID does not exists",'danger')
        return render_template('delete_customer.html',form=form)


@app.route('/customerstaus',methods=['GET','POST'])
def customer_status():
    form=customerStatusSearch()
    query= form.search_query.data
    if query is not None:
        accs =Customer_Account.objects(ssn_id=query) 
    else:
        accs =Customer_Account.objects() 
    print(accs)
    return render_template('customer_status.html',form=form,accs = accs)

@app.route('/accountstatus',methods=['GET','POST'])
def account_status():
    form = accountStatusSearch()
    query= form.search_query.data
    if query is not None:
        accs =Customer_Account.objects(ssn_id=query) 
    else:
        accs =Customer_Account.objects() 
    print(accs)
    return render_template('account_status.html',form = form,accs=accs)


@app.route('/createaccount',methods=['GET','POST'])
def create_account():
    form =createaccount()
    customer_ssn_id = form.customer_id.data
    account_type = form.account_type.data
    deposit_amount = form.deposit_amount.data 
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id = customer_ssn_id):
                    user =  Customer_Account.objects(ssn_id=customer_ssn_id).first()
        else:
                user=0
        if (account_type=="savings" or account_type=='s') and user != 0:
            if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(account_type = account_type, s_m = deposit_amount, message = "Customer Savings Account Created successfully", datetime = str(dt.now()))
                    flash("Customer Savings Account Created successfully","success")
        elif (account_type=="current" or account_type=='c') and user != 0: 
            if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(account_type = account_type, c_m= deposit_amount ,  message = "Customer Current Account Created successfully" ,datetime = str(dt.now()))
                    flash("Customer Current Account Created successfully","success")
        else:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('create_account.html',form=form )


@app.route('/deleteaccount', methods=['GET','POST'])
def delete_account():
    form = deleteAccount()
    account_id = form.account_id.data
    account_type = form.account_type.data
    if form.validate_on_submit():
         if Customer_Account.objects(ssn_id = account_id):
                    user =  Customer_Account.objects(ssn_id=account_id).first()
         else:
                user=0       
         if  user != 0 and ( account_type=="savings" or account_type=='s') :
                Customer_Account.objects(ssn_id = account_id ).update(account_type = "", s_m = 0 ,message = "Savings Account Deleted Successfully" ,datetime = str(dt.now()))
                flash("Customer Savings Account Deleted successfully","success")
         elif  user != 0 and  ( account_type=="current" or account_type=='c'):
                Customer_Account.objects(ssn_id = account_id ).update(account_type = "", c_m = 0 ,message = "Current Account Deleted Successfully" ,datetime = str(dt.now()))
                flash("Customer Current Account Deleted successfully","success")
         else:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('delete_Account.html',form = form)



@app.route('/accountsummary',methods =['GET','POST'] )
def account_summary():
    form = accountSum()
    query= form.search_query.data
    acc =Transactions.objects(name=query)
    return render_template("account_summary.html",form = form,acc=acc)

@app.route('/depositmoney', methods = ['GET','POST'])
def deposit_money():
    form = depositMoney()
    bal = 0 
    customer_ssn_id = form.customer_id.data
    account_id = form.account_id.data
    account_type = form.account_type.data
    deposit_amount = form.deposit_amount.data
        
    if form.validate_on_submit():
       
        if Customer_Account.objects(ssn_id = customer_ssn_id):
                    user =  Customer_Account.objects(ssn_id=customer_ssn_id).first()
        else:
                user=0  
        if account_type == "savings" or account_type=='s' and user !=0 and customer_ssn_id==account_id:
            if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                Customer_Account.objects(ssn_id = customer_ssn_id ).update(s_m = us.s_m+deposit_amount, message = "Money Deposited Successfully To Savings Account" ,datetime =  str(dt.now()))
                us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                bal = us.s_m
                id_no = Transactions.objects().count()+1
                Transactions(id_no = id_no , description = "Deposit",name = customer_ssn_id,datetime = str(dt.now()), amount = deposit_amount  ).save()
                flash("Money Deposited Successfully To Savings Account","success")
                

        elif account_type == "current" or account_type=='c' and user!=0 and customer_ssn_id==account_id:
            if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                Customer_Account.objects(ssn_id = customer_ssn_id ).update(c_m = us.c_m+deposit_amount, message = "Money Deposited Successfully To Current Account" ,datetime = str(dt.now()))
                us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                bal = us.c_m
                id_no = Transactions.objects().count()+1
                Transactions(id_no = id_no , description = "Deposit",name = customer_ssn_id,datetime = str(dt.now()), amount = deposit_amount  ).save()
                flash("Money Deposited Successfully To Current Account","success")
        elif user == 0:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('deposit_money.html',form = form, data = [bal])


@app.route('/transfermoney', methods = ['GET','POST'])
def transfer_money():
    form = transferMoney()
    customer_ssn_id = form.customer_id.data
    source_account_type = form.source_account_type.data
    target_account_type = form.target_account_type.data
    transfer_amount = form.transfer_amount.data 
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id = customer_ssn_id):
            user = Customer_Account.objects(ssn_id = customer_ssn_id).first()

            if (source_account_type == "savings" or source_account_type == "s") and user.s_m >= transfer_amount and source_account_type!=target_account_type :
                if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                    us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(s_m = us.s_m-transfer_amount, c_m = us.c_m+transfer_amount, message = "Money Sucessfully Transfered From Savings Account To Current Account" ,datetime =  str(dt.now()))
                    id_no = Transactions.objects().count()+1
                    Transactions(id_no = id_no , description = "Transfer",name = customer_ssn_id,datetime = str(dt.now()), amount = transfer_amount  ).save()
                    flash("Money Transfered Successfully From Savings Account to Current Account",'success')
            elif (source_account_type == "current"  or source_account_type == "c" )and user.c_m >= transfer_amount  and source_account_type!=target_account_type  :
                if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                    us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(s_m = us.s_m+transfer_amount, c_m = us.c_m-transfer_amount, message = "Money Sucessfully Transfered From Current Account To Savings Account" ,datetime = str(dt.now()))
                    id_no = Transactions.objects().count()+1
                    Transactions(id_no = id_no , description = "Transfer",name = customer_ssn_id,datetime = str(dt.now()), amount = transfer_amount  ).save() 
                    flash("Money Transfered Successfully From Current Account to Savings Account",'success')
            elif  (source_account_type == "savings" or source_account_type == "s") and user.s_m < transfer_amount :
                flash("You dont have sufficient balance in your Savings account",'danger')
            elif (source_account_type == "current"  or source_account_type == "c" )and user.c_m < transfer_amount:
                flash("You dont have sufficient balance in your Current account",'danger')
            elif (source_account_type==target_account_type):
                flash("Source Account Type and Target Account Type should not be the same",'danger')
        else:
            flash("Customer ID dosen't  match with Account ID","danger")  
        
               
    return render_template('transfer_money.html',form = form,)


@app.route('/withdrawmoney', methods = ['GET','POST'])
def withdraw_money():
    form = withdrawMoney()
    customer_ssn_id = form.customer_id.data
    account_id = form.account_id.data
    account_type = form.account_type.data
    withdraw_amount = form.withdraw_amount.data 
    bal = 0  
    
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id = customer_ssn_id):
            user = Customer_Account.objects(ssn_id = customer_ssn_id).first()
            if (account_type == "savings" or account_type=='s')  and user.s_m >= withdraw_amount and account_id == customer_ssn_id:
                    us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(s_m = us.s_m-withdraw_amount,message = "Money Withdrawn Successfully From Svaings Account" ,datetime = str(dt.now()))
                    us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                    bal = us.s_m       
                    id_no = Transactions.objects().count()+1
                    Transactions(id_no = id_no , description = "Withdraw",name = customer_ssn_id,datetime = str(dt.now()), amount = withdraw_amount  ).save()
                    flash("Money Withdrawn Successfully From Savings Account",'success') 
            if (account_type == "current" or account_type == "c") and user.c_m >= withdraw_amount and account_id == customer_ssn_id:
                    us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(c_m = us.c_m-withdraw_amount,message = "Money Withdrawn Successfully From Current Account" ,datetime =  str(dt.now()))
                    us = Customer_Account.objects(ssn_id = customer_ssn_id ).first()
                    bal = us.s_m      
                    id_no = Transactions.objects().count()+1
                    Transactions(id_no = id_no , description = "Withdraw",name = customer_ssn_id,datetime = str(dt.now()), amount = withdraw_amount  ).save() 
                    flash("Money Withdrawn Successfully From Current Account",'success') 
            elif user.s_m < withdraw_amount:
                flash("You dont have sufficient balance in your Savings account",'danger')      
            elif user.c_m < withdraw_amount:
                flash("You dont have sufficient balance in your Current account",'danger')
            elif account_id!=customer_ssn_id:
                flash("Customer ID dosen't  match with Account ID","danger")                
        else:
            flash("Customer with the given SSN_ID does not exists","danger")
    return render_template('withdraw_money.html',form = form,  data=[bal])



    


