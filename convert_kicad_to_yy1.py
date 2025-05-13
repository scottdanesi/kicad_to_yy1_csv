import csv
import sys

def convert_csv_to_neoden(csv_file_path, output_file_path):
    """
    Reads a CSV file, reformats the data, and writes it to a new CSV file
    in the Neoden-compatible format.

    Args:
        csv_file_path (str): The path to the input CSV file.
        output_file_path (str): The path to the output CSV file.
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as infile, \
                open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)

            # Write the header and fixed rows
            writer.writerow(['NEODEN', 'YY1', 'P&P FILE'] + [''] * 9)
            writer.writerow([''] * 12)
            writer.writerow(['PanelizedPCB', 'UnitLength', '0', 'UnitWidth', '0', 'Rows', '1', 'Columns', '1'] + [''] * 3)
            writer.writerow([''] * 12)
            writer.writerow(['Fiducial', '1-X', '13.09', '1-Y', '55.01', 'OverallOffsetX', '0.08', 'OverallOffsetY', '0.12'] + [''] * 3)
            writer.writerow([''] * 12)
            writer.writerow(['NozzleChange', 'OFF', 'BeforeComponent', '1', 'Head1', 'Drop', 'Station2', 'PickUp', 'Station1'] + [''] * 3)
            writer.writerow(['NozzleChange', 'OFF', 'BeforeComponent', '2', 'Head2', 'Drop', 'Station3', 'PickUp', 'Station2'] + [''] * 3)
            writer.writerow(['NozzleChange', 'OFF', 'BeforeComponent', '1', 'Head1', 'Drop', 'Station1', 'PickUp', 'Station1'] + [''] * 3)
            writer.writerow(['NozzleChange', 'OFF', 'BeforeComponent', '1', 'Head1', 'Drop', 'Station1', 'PickUp', 'Station1'] + [''] * 3)
            writer.writerow([''] * 12)
            writer.writerow(['Designator', 'Comment', 'Footprint', 'Mid X(mm)', 'Mid Y(mm)', 'Rotation', 'Head', 'FeederNo', 'Mount Speed(%)', 'Pick Height(mm)', 'Place Height(mm)', 'Mode', 'Skip'])

            # Check for valid reader and fieldnames before proceeding.
            if reader.fieldnames is None:
                print("Error: Input CSV file is empty or has no headers.")
                return

            output_header = ['Designator', 'Comment', 'Footprint', 'Mid X(mm)', 'Mid Y(mm)', 'Rotation', 'Head', 'FeederNo', 'Mount Speed(%)', 'Pick Height(mm)', 'Place Height(mm)', 'Mode', 'Skip']


            # Map the input CSV headers to the expected output headers.  This handles differences
            # in capitalization and spacing, and also provides a default value if a header is missing.
            header_map = {
                'Ref': 'Designator',
                'Val': 'Comment',
                'Package': 'Footprint',
                'PosX': 'Mid X(mm)',
                'PosY': 'Mid Y(mm)',
                'Rot': 'Rotation',
                'Side': None  # This field is not directly used, so we set it to None
            }

            for row in reader:
                # Initialize the output row with empty strings.
                out_row = [''] * 13
                #Populate the columns
                for in_header, out_header in header_map.items():
                    if out_header and in_header in row: # Make sure the input header exists
                        out_row[output_header.index(out_header)] = row[in_header]

                # Convert the Rotation to an integer
                try:
                    out_row[output_header.index('Rotation')] = int(float(out_row[output_header.index('Rotation')]))
                except ValueError:
                    out_row[output_header.index('Rotation')] = 0

                # Fixed values for the output CSV.
                out_row[output_header.index('Head')] = 0
                out_row[output_header.index('FeederNo')] = 1
                out_row[output_header.index('Mount Speed(%)')] = 100
                out_row[output_header.index('Pick Height(mm)')] = 0
                out_row[output_header.index('Place Height(mm)')] = 0
                out_row[output_header.index('Mode')] = 1
                out_row[output_header.index('Skip')] = 0

                writer.writerow(out_row)

        print(f"Successfully converted '{csv_file_path}' to '{output_file_path}'")

    except FileNotFoundError:
        print(f"Error: File not found at path: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if the correct number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: convert_kicad_to_yy1.py <input_csv_file> <output_csv_file>")
        sys.exit(1)  # Exit with an error code

    # Get the input and output file paths from the command line
    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]

    # Run the conversion.
    convert_csv_to_neoden(input_csv_file, output_csv_file)
