# Test Case 01: Valid Customer Search by ID

## Test Description
Search for a customer using a valid customer ID and generate a statement in English.

## Test Environment
- **Operating System**: Windows 10
- **Browser**: Chrome 120.0.6099.130
- **Application Version**: CIMB PDF Generator v1.0
- **Database**: MySQL 8.0 with test data loaded

## Prerequisites
1. Application is running on localhost:5000
2. Database connection is established
3. Test data is loaded in the database
4. Required fonts are downloaded

## Test Steps
1. Navigate to the application homepage
2. Select "ID" as the search type from the dropdown
3. Enter "2" in the search value field
4. Select "English (en)" as the language
5. Click the "Search" button
6. Verify customer details are displayed
7. Click on "View Statements" button
8. Select a statement from the list
9. Click "Generate PDF" button
10. Verify PDF is generated and download option appears

## Input
- **Search Type**: ID
- **Search Value**: 2
- **Language**: English (en)

## Expected Output
- Customer with ID 2 should be found
- Customer details should be displayed correctly:
  - Name: Sarah Johnson
  - Address: 456 Oak Avenue, Apt 7B, Springfield, IL 62701
  - Card Number: 5555-6666-7777-8888
  - Account Number: 80-0024166-7
- List of available statements should be shown
- Option to generate PDF should be available
- Generated PDF should:
  - Display correct customer information
  - Show statement details in English
  - Include transaction history
  - Have proper formatting with borders
  - Display CIMB branding

## Actual Result
- Customer with ID 2 was found
- Customer details displayed correctly:
  - Name: Sarah Johnson
  - Address: 456 Oak Avenue, Apt 7B, Springfield, IL 62701
  - Card Number: 5555-6666-7777-8888
  - Account Number: 80-0024166-7
- 3 statements were listed for the customer:
  - January 2024
  - February 2024
  - March 2024
- PDF generation option was available
- Generated PDF correctly displayed:
  - Customer information
  - Statement details in English
  - Transaction history with 8 transactions
  - Proper formatting with borders
  - CIMB branding elements

## Screenshots
1. [Homepage with search form completed](../sample_output/test01_search_form.png)
2. [Customer details page](../sample_output/test01_customer_details.png)
3. [Statements list page](../sample_output/test01_statements_list.png)
4. [Generated PDF preview](../sample_output/test01_pdf_preview.png)

## Status
**PASS**

## Notes
- The search functionality correctly identified the customer by ID and displayed all relevant information.
- PDF generation completed in 1.2 seconds.
- All text in the PDF was correctly displayed in English.
- The PDF included proper formatting with borders, CIMB branding, and all required sections.
- Transaction details were correctly sorted by date.
- The statement summary calculations matched the expected values.

## Test Data
```sql
-- Customer record used in this test
SELECT * FROM customers WHERE customer_id = 2;
-- Statement records for this customer
SELECT * FROM statements WHERE customer_id = 2;
-- Transaction records for the first statement
SELECT * FROM transactions WHERE statement_id = 4;
```