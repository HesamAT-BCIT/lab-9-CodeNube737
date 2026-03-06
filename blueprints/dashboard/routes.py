# blueprints/dashboard/routes.py

#
# Use @dashboard_bp.route decorators. Import:
#   - render_template, session, redirect, url_for (from flask)
#   - dashboard_bp from .
#   - get_profile_data from utils.profile
#   - get_current_user from utils.auth

from flask import render_template, session, redirect, url_for
from . import dashboard_bp

from utils.auth import get_current_user
from utils.profile import get_profile_data


@dashboard_bp.route("/")
def home():
    """Home page. Redirects to login if no active session."""
    current_user = get_current_user()
    if current_user:
        profile_data = get_profile_data(current_user)
        return render_template("dashboard.html", first_name=profile_data.get('first_name', ''), profile=profile_data, jwt_token=session.get('jwt_token'))
    return redirect(url_for("auth.login"))

