def generate_html_report(valid_creds):
    with open("xvector_report.html", "w") as f:
        f.write("<html><head><title>X-Vector Report</title></head><body>")
        f.write("<h2>Valid Credentials</h2><ul>")
        for user, pwd in valid_creds:
            f.write(f"<li>{user}:{pwd}</li>")
        f.write("</ul></body></html>")
