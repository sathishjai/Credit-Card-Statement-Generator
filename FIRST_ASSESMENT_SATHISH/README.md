# CIMB Credit Card Statement Generator

A Flask-based application that generates multilingual credit card statements in PDF format for CIMB Bank customers.

## Tech Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: MySQL
- **PDF Generation**: FPDF library
- **Multilingual Support**: Noto Sans fonts for multiple languages
- **Frontend**: HTML, CSS, Bootstrap

## Features

- Search customers by ID or name
- View customer statements
- Generate PDF statements in multiple languages
- Support for various character sets (Latin, Tamil, Thai, etc.)
- Responsive design

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cimb-statement-generator.git
cd cimb-statement-generator