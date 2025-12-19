from app import app, render_template
import requests
from flask import request, redirect, abort

@app.route('/admin/product')
def product():
    module = 'product'
    return render_template('backend/product/index.html', module=module)

@app.route('/admin/product/form')
def add_product():
    module = 'product'
    action = request.args.get('action','add')
    if action not in ['add','edit']:
        return abort(404)

    pro_id = request.args.get('pro_id',0)
    status = 'add' if action == 'add' else 'edit'

    return render_template('backend/product/form.html', module=module, status=status, pro_id=pro_id)