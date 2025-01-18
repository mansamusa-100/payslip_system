from django.shortcuts import render, redirect
from .models import Employee
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseForbidden
from .models import Employee
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


@login_required
def add_employee(request):
    if not request.user.is_staff:  # Check if the user is an admin
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == "POST":
        # Handle employee addition logic
        pass

    return render(request, 'add_employee.html')

def add_employee(request):
    if request.method == 'POST':
        Employee.objects.create(
            user_id=request.POST['user_id'],
            name=request.POST['name'],
            email=request.POST['email'],
            basic_salary=request.POST['basic_salary'],
            housing_allowance=request.POST.get('housing_allowance', 0),
            transport_allowance=request.POST.get('transport_allowance', 0),
            other_allowances=request.POST.get('other_allowances', 0),
            tax_deduction=request.POST.get('tax_deduction', 0),
            other_deductions=request.POST.get('other_deductions', 0),
        )
        return redirect('add_employee')
    return render(request, 'add_employee.html')

@login_required
def employee_interface(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        # Fetch employee data
        try:
            employee = Employee.objects.get(user_id=user_id)
        except Employee.DoesNotExist:
            return HttpResponse("Invalid User ID. Please try again.")

        # Generate PDF payslip
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Payslip", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Name: {employee.name}", ln=True)
        pdf.cell(200, 10, txt=f"User ID: {employee.user_id}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {employee.email}", ln=True)

        # Salary Breakdown
        pdf.cell(200, 10, txt=f"Basic Salary: {employee.basic_salary}", ln=True)
        pdf.cell(200, 10, txt=f"Housing Allowance: {employee.housing_allowance}", ln=True)
        pdf.cell(200, 10, txt=f"Transport Allowance: {employee.transport_allowance}", ln=True)
        pdf.cell(200, 10, txt=f"Other Allowances: {employee.other_allowances}", ln=True)
        pdf.cell(200, 10, txt=f"Gross Salary: {employee.gross_salary}", ln=True)
        pdf.cell(200, 10, txt=f"Tax Deduction: {employee.tax_deduction}", ln=True)
        pdf.cell(200, 10, txt=f"Other Deductions: {employee.other_deductions}", ln=True)
        pdf.cell(200, 10, txt=f"Net Salary: {employee.net_salary}", ln=True)

        pdf_file = f"{employee.user_id}_payslip.pdf"
        pdf.output(pdf_file)

        # Send email and serve PDF
        #send_email(employee.email, pdf_file)
        return FileResponse(open(pdf_file, 'rb'), as_attachment=True)

    return render(request, 'employee_interface.html')


# Email Function
# def send_email(to_email, pdf_file):
#     sender_email = "your_email@example.com"
#     sender_password = "your_password"
#
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = to_email
#     msg['Subject'] = "Your Payslip"
#
#     body = "Please find your payslip attached."
#     msg.attach(MIMEText(body, 'plain'))
#
#     with open(pdf_file, 'rb') as attachment:
#         part = MIMEBase('application', 'octet-stream')
#         part.set_payload(attachment.read())
#         encoders.encode_base64(part)
#         part.add_header('Content-Disposition', f'attachment; filename={pdf_file}')
#         msg.attach(part)
#
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.send_message(msg)
#     server.quit()