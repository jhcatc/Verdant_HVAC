async def generate_pdf(order):
    # luego usamos reportlab o weasyprint
    return "invoice.pdf"


async def send_email(email, pdf_path):
    # luego SMTP o SendGrid
    print(f"Sending invoice to {email}")