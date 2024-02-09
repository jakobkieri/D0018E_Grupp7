from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
customer_bp = Blueprint('customer', __name__, 
                        template_folder='templates',
                        static_folder='static')
