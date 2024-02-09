from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
admin_bp = Blueprint('admin', __name__, 
                        template_folder='templates',
                        static_folder='static')


@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    return render_template("AdmMain.html")
