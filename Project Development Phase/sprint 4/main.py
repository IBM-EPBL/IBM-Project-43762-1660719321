# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import ibm_db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from inventory.Vendor import Vendor
from inventory.Inventory import Inventory
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def show_login():
    return redirect(url_for('login'))


@app.route("/vendor/signup", methods=['GET', 'POST'])
def vendor_signup():
    if request.method == 'POST':
        vendor = Vendor()
        vendor.Id = ""
        vendor.Name = request.form['name']
        vendor.Shop_Name = request.form['shop_name']
        vendor.GST = request.form['gst']
        vendor.Mobile = request.form['mobile']
        vendor.Address = request.form['address']
        vendor.Email = request.form['email']
        vendor.Password = request.form['password']
        vendor.save()

        flash(u'Vendor Sign up done, you login now with your username and password.', 'success')

        return redirect(url_for('login'))
    else:
        return render_template('register_vendor.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != "" and request.form['password'] != "":
            vendor = Vendor()
            vendor.Email = request.form['username']
            vendor.Password = request.form['password']
            result = vendor.login()

            print(result)
            if len(result) > 0:
                session['name'] = result[0]['NAME']
                session['vendor_id'] = result[0]['ID']
                email_low_stock_alert(session['vendor_id'])
                return redirect(url_for('dashboard'))
            else:
                flash(u'username or password is incorrect.', 'danger')
                return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route("/dashboard", methods=['GET'])
def dashboard():
    if session['name'] is None:
        return redirect(url_for('login'))

    inventory = Inventory()
    inventory = inventory.display()
    return render_template('dashboard.html')


@app.route("/inventory", methods=['GET'])
def view_inventory():
    if session['name'] is None:
        return redirect(url_for('login'))

    inventory = Inventory()
    inventory.VendorId = session['vendor_id']
    inventory = inventory.display()

    print(inventory)
    return render_template('view_inventory.html', inventory=inventory)


@app.route("/low_inventory", methods=['GET'])
def low_inventory():
    if session['name'] is None:
        return redirect(url_for('login'))

    inventory = Inventory()
    inventory.VendorId = session['vendor_id']
    inventory = inventory.get_low_stock()
    return render_template('low_inventory.html', inventory=inventory)


@app.route("/inventory/new", methods=['GET'])
def inventory_new():
    if session['name'] is None:
        return redirect(url_for('login'))
    inventory = Inventory()
    return render_template('inventory_item.html', item=inventory)


@app.route("/inventory/edit/<int:id>", methods=['GET'])
def inventory_edit(id):
    if session['name'] is None:
        return redirect(url_for('login'))

    inventory = Inventory()
    inventory.VendorId = session['vendor_id']
    inventory = inventory.get(id)

    if len(inventory) > 0:
        item = inventory[0]
        return render_template('inventory_item.html', item=item)
    else:
        flash(u'Inventory item is not found with id = ' + str(id), 'danger')
        return render_template('inventory_item.html', item=inventory)


@app.route("/inventory/save", methods=['POST'])
def inventory_save():
    if session['name'] is None:
        return redirect(url_for('login'))

    inventory = Inventory()
    if request.form['id'] != "":
        inventory.Id = request.form['id']
    inventory.VendorId = session['vendor_id']
    inventory.Category = request.form['category']
    inventory.ItemName = request.form['item_name']
    inventory.Wholesaleprice = request.form['wholesale_price']
    inventory.Retailprice = request.form['retail_price']
    inventory.Qty = request.form['qty']
    inventory.Low_Stock_Limit = request.form['low_stock_limit']
    inventory.LotNo = request.form['lot_no']
    inventory.Note = request.form['note']
    inventory.save()

    flash(u'Inventory has been saved successfully.', 'success')
    return redirect(url_for('view_inventory'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


def email_low_stock_alert(vendor_id):
    if session['name'] is None:
        return redirect(url_for('login'))

    vendor = Vendor()
    vendors = vendor.get(vendor_id)
    vendor = vendors[0]

    inv = Inventory()
    inventory = inv.get_low_stock()

    if len(inventory) > 0:
        sg = sendgrid.SendGridAPIClient(api_key="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")
        from_email = Email("rajesh@malaris.com")
        to_email = To(vendor["EMAIL"])
        subject = "Vendor Low Stock Notification"
        content = Content("text/html", render_template('email_low_stock.html', inventory=inventory, vendor=vendor))
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
