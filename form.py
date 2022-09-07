from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Email,ValidationError,Length
from flask import flash
from model import Customer_Account



class login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder":" Username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder":" Password"})
    submit=SubmitField("Login")



class customerScreen(FlaskForm):
    ssn_id=StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    customer_name=StringField("Customer Name",validators=[DataRequired()], render_kw={"placeholder":"Customer Name"})
    age=IntegerField("Age",validators=[DataRequired()],render_kw={"placeholder":"Age"})
    address=TextAreaField("Address",validators=[DataRequired()],render_kw={"placeholder":"Address"})
    state=StringField("State",validators=[DataRequired()],render_kw={"placeholder":"State"})
    city=StringField("City",validators=[DataRequired()],render_kw={"placeholder":"City"})
    submit=SubmitField("Submit")

class updateCustomer(FlaskForm):
    customer_ssn_id = StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    new_customer_name = StringField("New Customer Name",validators=[DataRequired()],render_kw={"placeholder": "Customer Name"})
    new_address = TextAreaField("New Address",validators=[DataRequired()],render_kw={"placeholder": "New Address"})
    new_age = IntegerField("New Age",validators=[DataRequired()],render_kw={"placeholder": "New Age"})


class deleteCustomer(FlaskForm):
    ssn_id=StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    
    submit=SubmitField("Confirm Delete")

    


class transferMoney(FlaskForm):
    customer_id =StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    source_account_type = StringField("Source Account Type",validators=[DataRequired()])
    target_account_type = StringField("Target Account Type",validators=[DataRequired()])
    transfer_amount = IntegerField("Tranfers Amount", validators=[DataRequired()])
    submit=SubmitField("Transfer")

class withdrawMoney(FlaskForm):
    customer_id =StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    account_id = StringField("Account ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    account_type = StringField("Account Type",validators=[DataRequired()])
    withdraw_amount = IntegerField("Withdraw Amount", validators=[DataRequired()])
    submit=SubmitField("Submit")


class depositMoney(FlaskForm):
    customer_id = StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    account_id = StringField("Account ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    account_type = StringField("Account Type",validators=[DataRequired()])
    deposit_amount = IntegerField("Deposit Amount", validators=[DataRequired()])
    submit=SubmitField("Submit")

class createaccount(FlaskForm):
    customer_id =StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    account_type = SelectField('Account type', choices=[('savings', 'Savings'), ('current', 'Current')], validators=[DataRequired()])
    deposit_amount = IntegerField("Deposit Amount",validators=[DataRequired()],render_kw={"placeholder": "Deposit Amount"})
    submit=SubmitField("Create")

class deleteAccount(FlaskForm):
    account_id =StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)],render_kw={"placeholder":"SSN ID"})
    account_type = StringField("Account Type",validators=[DataRequired()])
    delete = SubmitField("Delete")




class accountSum(FlaskForm):
    search_query = StringField("Customer SSN_ID", validators=[DataRequired()],render_kw={"placeholder":"SSN ID"})
    search = SubmitField("Search")



class customerStatusSearch(FlaskForm):
    search_query = StringField("search", validators=[DataRequired()],render_kw={"placeholder":"SSN ID"})
    search = SubmitField("Search")

class accountStatusSearch(FlaskForm):
    search_query = StringField("search", validators=[DataRequired()],render_kw={"placeholder":"SSN ID"})
    search = SubmitField("Search")