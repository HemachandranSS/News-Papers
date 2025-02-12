import json
import re

def extract_table_data(document_content):
    # Find the section with the table
    table_start = document_content.find("Companies That Have Shown Growth In Net Profit And Sales")
    if table_start == -1:
        raise ValueError("Table section not found in document")
    
    # Extract table content
    table_content = document_content[table_start:]
    # Split into lines
    lines = table_content.split('\n')
    
    # Find where the actual data starts (after headers)
    data_start_idx = -1
    for i, line in enumerate(lines):
        if "Amber Enterp." in line:
            data_start_idx = i
            break
    
    if data_start_idx == -1:
        raise ValueError("Could not find start of table data")
    
    # Extract table rows until the end of the table
    table_rows = []
    current_idx = data_start_idx
    while current_idx < len(lines):
        line = lines[current_idx].strip()
        # Break if we hit an empty line or a section marker
        if not line or "*Companies are sorted" in line:
            break
        table_rows.append(line)
        current_idx += 1
    
    return table_rows

def parse_company_data(table_rows):
    companies = []
    
    for row in table_rows:
        # Split the row and clean up the values
        parts = row.split()
        if len(parts) < 10:  # Skip rows that don't have enough data
            continue
            
        try:
            # Extract company name
            company_name_parts = []
            i = 0
            while i < len(parts) and not parts[i].replace('.', '').replace('-', '').replace(',', '').isdigit():
                company_name_parts.append(parts[i])
                i += 1
            company_name = ' '.join(company_name_parts)
            
            # Get the remaining numeric values
            values = parts[i:]
            if len(values) < 10:
                continue
                
            # Clean numeric values (remove commas and convert to float)
            def clean_number(val):
                return float(val.replace(',', ''))
            
            # Create company data structure
            company_data = {
                "company_name": company_name,
                "sales": {
                    "Q3FY25": clean_number(values[2]),
                    "Q3FY24": clean_number(values[0]),
                    "Q2FY25": clean_number(values[1]),
                    "YoY_Growth": clean_number(values[4]),
                    "QoQ_Growth": clean_number(values[3])
                },
                "net_profit": {
                    "Q3FY25": clean_number(values[7]),
                    "Q3FY24": clean_number(values[5]),
                    "Q2FY25": clean_number(values[6]),
                    "YoY_Growth": clean_number(values[9]),
                    "QoQ_Growth": clean_number(values[8])
                }
            }
            companies.append(company_data)
            
        except (IndexError, ValueError) as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {str(e)}")
            continue
    
    return companies

def process_document(document_content):
    try:
        # Extract table rows
        table_rows = extract_table_data(document_content)
        
        # Parse the data into structured format
        companies_data = parse_company_data(table_rows)
        
        # Convert to JSON
        json_output = json.dumps(companies_data, indent=2)
        
        return json_output
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Assuming document_content is the text from your PDF
    document_content = """[Your PDF content here]"""
    
    json_result = process_document(document_content)
    if json_result:
        print(json_result)