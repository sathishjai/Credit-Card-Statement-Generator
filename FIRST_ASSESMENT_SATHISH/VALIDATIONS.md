# CIMB PDF Generator - Validation Rules

This document outlines the validation rules implemented in the CIMB PDF Generator application to ensure data integrity and proper functioning.

## Customer Information Validations

### Customer ID
- **Format**: Numeric values only
- **Length**: Must be between 1-10 digits
- **Required**: Yes
- **Example Valid Input**: 1001, 9999
- **Example Invalid Input**: ABC123, 12345678901

### Customer Name
- **Format**: Alphanumeric with spaces
- **Length**: 2-100 characters
- **Required**: Yes
- **Example Valid Input**: "John Doe", "Mary O'Connor"
- **Example Invalid Input**: "" (empty), "A" (too short)

### Card Number
- **Format**: 16 digits, may be formatted with spaces or dashes
- **Validation**: Luhn algorithm check
- **Masking**: Only last 4 digits displayed in full, others masked as XXXX
- **Required**: Yes
- **Example Valid Input**: "4111-1111-1111-1111", "5555 5555 5555 4444"
- **Example Invalid Input**: "1234-5678" (too short), "ABCD-EFGH-IJKL-MNOP" (non-numeric)

### Address
- **Format**: Alphanumeric with spaces and common punctuation
- **Length**: 5-200 characters
- **Required**: Yes
- **Example Valid Input**: "123 Main St, Apt 4B, New York, NY 10001"
- **Example Invalid Input**: "" (empty)

## Statement Information Validations

### Statement Date
- **Format**: Valid date in YYYY-MM-DD format
- **Validation**: Must be a valid calendar date
- **Required**: Yes
- **Example Valid Input**: "2023-12-31"
- **Example Invalid Input**: "2023-13-45" (invalid month/day)

### Statement Period
- **Format**: Two valid dates (start and end) in YYYY-MM-DD format
- **Validation**: 
  - End date must be after start date
  - Period should not exceed 31 days
- **Required**: Yes
- **Example Valid Input**: "2023-01-01" to "2023-01-31"
- **Example Invalid Input**: "2023-02-15" to "2023-01-15" (end before start)

### Outstanding Balance
- **Format**: Decimal number with up to 2 decimal places
- **Range**: 0.00 to 999,999,999.99
- **Required**: Yes
- **Example Valid Input**: "1250.75", "0.00"
- **Example Invalid Input**: "-100.50" (negative), "1,234.567" (too many decimal places)

### Minimum Payment Due
- **Format**: Decimal number with up to 2 decimal places
- **Validation**: Must be less than or equal to outstanding balance
- **Required**: Yes
- **Example Valid Input**: "50.00" (when balance is 1250.75)
- **Example Invalid Input**: "2000.00" (when balance is 1250.75)

### Payment Due Date
- **Format**: Valid date in YYYY-MM-DD format
- **Validation**: Must be a future date relative to statement date
- **Required**: Yes
- **Example Valid Input**: "2023-02-15" (for statement date 2023-01-15)
- **Example Invalid Input**: "2023-01-01" (for statement date 2023-01-15)

## Transaction Information Validations

### Transaction Date
- **Format**: Valid date in YYYY-MM-DD format
- **Validation**: Must fall within statement period
- **Required**: Yes
- **Example Valid Input**: "2023-01-15" (for period 2023-01-01 to 2023-01-31)
- **Example Invalid Input**: "2023-02-01" (outside statement period)

### Transaction Description
- **Format**: Alphanumeric text with spaces and common punctuation
- **Length**: 2-100 characters
- **Required**: Yes
- **Example Valid Input**: "AMAZON.COM PURCHASE", "STARBUCKS COFFEE #123"
- **Example Invalid Input**: "" (empty)

### Transaction Amount
- **Format**: Decimal number with up to 2 decimal places
- **Range**: -999,999,999.99 to 999,999,999.99
- **Required**: Yes
- **Example Valid Input**: "125.45", "-50.00"
- **Example Invalid Input**: "12,34.56" (invalid format)

### Transaction Type
- **Format**: Must be one of the predefined types
- **Valid Types**: "Payment", "Purchase", "Cash Advance", "Fee", "Interest", "Adjustment"
- **Required**: Yes
- **Example Valid Input**: "Purchase", "Payment"
- **Example Invalid Input**: "Refund" (not in predefined list)

## Language Selection Validation

### Language Code
- **Format**: Must be one of the supported language codes
- **Valid Codes**: "en", "vi", "tl", "en-gb", "ta", "th", "ms"
- **Required**: Yes
- **Example Valid Input**: "en", "ta"
- **Example Invalid Input**: "fr" (not supported), "EN" (case sensitive)

## PDF Generation Validations

### Font Availability
- **Validation**: Required font files must exist in the fonts directory
- **Fallback**: Default to NotoSans-Regular.ttf if language-specific font not available
- **Required**: Yes for PDF generation

### Output Directory
- **Validation**: The pdfs directory must exist and be writable
- **Required**: Yes for PDF generation

## Database Connection Validations

### Connection Parameters
- **Validation**: Valid host, user, password, and database name
- **Required**: Yes for database operations
- **Error Handling**: Graceful error messages if connection fails