# blueprints/profile/routes.py

# Use @profile_bp.route decorators. Import:
#   - request, render_template, session, redirect, url_for (from flask)
#   - profile_bp from .
#   - get_profile_data, set_profile from utils.profile
#   - validate_profile_data, normalize_profile_data from utils.validation
#   - get_current_user from utils.auth
from flask import request, render_template, session, redirect, url_for

from utils.auth import get_current_user
from . import profile_bp
from utils.profile import get_profile_data, set_profile
from utils.validation import validate_profile_data, normalize_profile_data


@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """HTML form to create/update the current user's profile."""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("login"))

    if request.method == "GET":
        profile_data = get_profile_data(current_user)
        return render_template("profile.html", profile=profile_data, error=None)

    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    student_id = request.form.get("student_id", "")

    error = validate_profile_data(first_name, last_name, student_id)
    if error:
        profile_data = {"first_name": first_name, "last_name": last_name, "student_id": student_id}
        return render_template("profile.html", profile=profile_data, error=error)

    normalized = normalize_profile_data(first_name, last_name, student_id)
    set_profile(current_user, normalized, merge=False)
    return redirect(url_for("home"))

