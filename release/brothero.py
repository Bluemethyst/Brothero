import csv, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="Translate CSV data from Brother export to Xero import.")
parser.add_argument("input_file", help="The input CSV file to translate.")
parser.add_argument("output_file", help="The output CSV file to create.")

args = parser.parse_args()


# Function to read the fieldnames from the Xero template CSV
def read_xero_template(template_file):
    try:
        with open(template_file, mode="r", newline="", encoding="utf-8") as template:
            reader = csv.reader(template)
            xero_fields = next(reader)  # Get the first row (headers)
            xero_fields = [
                field for field in xero_fields if field
            ]  # Filter out any empty fields
            print(f"Xero fields loaded: {xero_fields}")
            return xero_fields
    except Exception as e:
        print(f"Error reading Xero template: {e}")
        return []


# Define the mapping from export fields to Xero fields
field_mapping = {
    "ContactName": "*ContactName",  # Ensure this matches the actual export CSV header
    "EmailAddress": "EmailAddress",
    "TaxType": "*TaxType",  # Example mapping, fix according to your data
    "Description": "*Description",  # Example additional mapping
    "Location/Asset Label": "*Description",
    "BrandingTheme": "BrandingTheme",
    "Quantity": "*Quantity",
    "UnitAmount": "*UnitAmount",
    "AccountCode": "*AccountCode",
    "Discount": "Discount",
    "InvoiceNumber": "*InvoiceNumber",
    "InvoiceDate": "*InvoiceDate",
    "Due Date": "*DueDate",
    # Add more mappings here as per your export CSV headers
}

manual_values = {
    "Currency": "NZD",
    "*AccountCode": "212",
}

# Dictionary to map trigger strings to their corresponding unit amount fields
trigger_unit_amount_mapping = {
    "A4 Page Count Mono": "A4 Mono Rate",
    "A4 Page Count Colour": "A4 Colour Rate",
    "A3 Page Count Mono": "A3 Mono Rate",
    "A3 Page Count Colour": "A3 Colour Rate",
    # Add more mappings as needed...
}

# List of strings that trigger a new line
trigger_strings = list(trigger_unit_amount_mapping.keys())


def translate_csv(input_file, output_file, xero_fields, field_mapping, manual_values):
    try:
        with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            new_headers = xero_fields  # Use all fields from the template

            with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=new_headers)
                writer.writeheader()

                for row in reader:
                    new_row = {field: "" for field in new_headers}
                    field_aggregation = defaultdict(list)

                    # Populate field_aggregation based on the field_mapping
                    for key, value in row.items():
                        if key in field_mapping:
                            mapped_field = field_mapping[key]
                            field_aggregation[mapped_field].append(value)

                    # Combine fields with "|" separator
                    for xero_field, values in field_aggregation.items():
                        new_row[xero_field] = " | ".join(values)

                    # Set manual values
                    for field, value in manual_values.items():
                        if field in new_row:
                            new_row[field] = value

                    # Write the current row
                    writer.writerow(new_row)

                    # Check if certain fields contain any of the trigger strings
                    for key, value in row.items():
                        if (
                            key in trigger_strings and value != "0"
                        ):  # Check if the value is not "0"
                            # Debugging: Print that a trigger has been detected with a non-zero value
                            print(
                                f"Trigger detected for field '{key}' with non-zero value '{value}'."
                            )

                            # Add a new row based on the trigger
                            new_line_row = new_row.copy()
                            new_line_row["*Description"] = key
                            new_line_row["*Quantity"] = (
                                value  # Use the value from the original row
                            )
                            # Set the unit amount based on the corresponding trigger
                            unit_amount_key = trigger_unit_amount_mapping[key]
                            unit_amount = row.get(
                                unit_amount_key, ""
                            )  # Get the unit amount

                            # Check if the unit amount contains a dollar sign and clean it
                            if "$" in unit_amount:
                                unit_amount = unit_amount.replace("$", "").strip()

                            # Assign the cleaned unit amount (converted to int)
                            try:
                                new_line_row["*UnitAmount"] = (
                                    float(unit_amount) if unit_amount else 0.0
                                )
                            except ValueError:
                                print(
                                    f"Invalid unit amount '{unit_amount}' for field '{key}'. Defaulting to 0.0."
                                )
                                new_line_row["*UnitAmount"] = 0.0

                            writer.writerow(new_line_row)

                            # Debugging: Print the new line row
                            print(f"New line row added: {new_line_row}")

                print(f"File '{output_file}' created successfully.")

    except Exception as e:
        print(f"Error processing files: {e}")


# File paths
input_file = args.input_file  # Replace with your export CSV file
output_file = args.output_file  # The file to import into Xero
template_file = "XeroSalesInvoiceTemplate.csv"  # The Xero template CSV file

# Load Xero fields from the template
xero_fields = read_xero_template(template_file)

# Run the translation
translate_csv(input_file, output_file, xero_fields, field_mapping, manual_values)
