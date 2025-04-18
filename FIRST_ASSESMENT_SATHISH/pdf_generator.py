from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

# Dictionary for translations
translations = {
    'en': {
        'STATEMENT DATE': 'Statement Date',
        'STATEMENT PERIOD': 'Statement Period',
        'Credit Card eStatement Campaign 2024': 'Credit Card eStatement Campaign 2024',
        'Switch to eStatements...': 'Switch to eStatements and get RM20 cashback!',
        'TOTAL OUTSTANDING BALANCE': 'Total Outstanding Balance',
        'MINIMUM PAYMENT DUE': 'Minimum Payment Due',
        'PAYMENT DUE DATE': 'Payment Due Date',
        'TRANSACTION DETAILS': 'Transaction Details',
        'Date': 'Date',
        'Description': 'Description',
        'Amount': 'Amount',
        'COMPUTER_GENERATED': 'This is a computer-generated statement. No signature is required.',
        'CUSTOMER_SERVICE': 'For inquiries, please contact our 24-hour Customer Service at 1300 88 6688',
        'COPYRIGHT': '© {} CIMB Bank. All Rights Reserved.'
    },
    'ta': {
        'STATEMENT DATE': 'அறிக்கை தேதி',
        'STATEMENT PERIOD': 'அறிக்கை காலம்',
        'Credit Card eStatement Campaign 2024': 'கிரெடிட் கார்டு மின்-அறிக்கை பிரச்சாரம் 2024',
        'Switch to eStatements...': 'மின்-அறிக்கைகளுக்கு மாறி RM20 ரொக்கப்பணம் பெறுங்கள்!',
        'TOTAL OUTSTANDING BALANCE': 'மொத்த நிலுவை இருப்பு',
        'MINIMUM PAYMENT DUE': 'குறைந்தபட்ச செலுத்த வேண்டிய தொகை',
        'PAYMENT DUE DATE': 'பணம் செலுத்த வேண்டிய தேதி',
        'TRANSACTION DETAILS': 'பரிவர்த்தனை விவரங்கள்',
        'Date': 'தேதி',
        'Description': 'விவரம்',
        'Amount': 'தொகை',
        'COMPUTER_GENERATED': 'இது கணினி உருவாக்கிய அறிக்கை. கையொப்பம் தேவையில்லை.',
        'CUSTOMER_SERVICE': 'விசாரணைகளுக்கு, எங்கள் 24-மணி நேர வாடிக்கையாளர் சேவையை 1300 88 6688 என்ற எண்ணில் தொடர்பு கொள்ளவும்',
        'COPYRIGHT': '© {} CIMB வங்கி. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.'
    }
}

def tr(key, lang='en'):
    """Translate a key to the specified language"""
    return translations.get(lang, translations['en']).get(key, key)

def generate_statement_pdf(customer_data, output_path, lang='en'):
    """Generate a PDF statement using WeasyPrint with language support"""
    try:
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('statement_weasy.html')

        # Format dates
        statement_date = datetime.strptime(customer_data['statement_date'], '%Y-%m-%d').strftime('%d %b %Y')
        period_start = datetime.strptime(customer_data['period_start'], '%Y-%m-%d').strftime('%d %b %Y')
        period_end = datetime.strptime(customer_data['period_end'], '%Y-%m-%d').strftime('%d %b %Y')

        # Prepare template context
        context = {
            'customer_name': customer_data['name'],
            'customer_address': customer_data['address'],
            'card_no': customer_data['card_no'],
            'acc_no': customer_data['acc_no'],
            'statement_date': statement_date,
            'period_start': period_start,
            'period_end': period_end,
            'out_bal': customer_data['outstanding_balance'],
            'min_due': customer_data['minimum_payment'],
            'due_date': customer_data['payment_due_date'],
            'transactions': customer_data['transactions'],
            'tr': tr,
            'lang': lang,
            'statement_year': datetime.now().year
        }

        # Render HTML
        html_content = template.render(**context)

        # Create PDF using WeasyPrint
        html = HTML(string=html_content, base_url=os.path.dirname(os.path.abspath(__file__)))
        css = CSS(string='''
            @page {
                size: A4;
                margin: 2.5cm;
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                }
            }
        ''')

        # Generate PDF
        html.write_pdf(
            output_path,
            stylesheets=[css],
            presentational_hints=True
        )

        return True, f"PDF generated successfully at {output_path}"

    except Exception as e:
        error_message = f"Error generating PDF: {str(e)}"
        # Log the error
        with open('logs/cimb_pdf_error_log.txt', 'a') as log_file:
            log_file.write(f"{datetime.now()}: {error_message}\n")
        return False, error_message