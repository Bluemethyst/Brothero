# Brothero

Brothero is a simple program to convert Brother Billing CSV exports to Xero CSV imports.

## Installation

Ensure you have Python installed. Download the 2 files from [here](/release) by clicking them and then the little "Download Raw File" button in the top right. Put the downloaded files in the same directory as your Brother CSV file. 

## Usage

Make sure Python is installed and run the following command:

```sh
python brothero.py <input_file> <output_file>
```

So for example, if your Brother CSV file is called `billing.csv` and you want the output to be called `xero.csv`, you would run:

```sh
python brothero.py billing.csv xero.csv
```

The output file will be created in the same directory as the input file.

## Configuration

Ensure that the `XeroSalesInvoiceTemplate.csv` file is in the same directory as the script. You can modify the `field_mapping` and `manual_values` dictionaries in the script to match your specific needs.

## Examples

### Input CSV (`billing.csv`)

```csv
ContactName,EmailAddress,Description,Quantity,UnitAmount
John Doe,john@example.com,Service,1,100
```

### Output CSV (`xero.csv`)

```csv
*ContactName,EmailAddress,*Description,*Quantity,*UnitAmount
John Doe,john@example.com,Service,1,100
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the Apache Version 2.0 License.
