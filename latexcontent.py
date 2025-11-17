# Importing the XMLParser class from the 'xmlparser' module
from xmlparser import XMLParser

print("DEBUG: Creating XMLParser instance...")
# Instantiating the XMLParser class
xml_parser = XMLParser()

print("DEBUG: Parsing attachment.xml ...")
# Parsing the XML file and extracting dat
data = xml_parser.parse_xml("attachment.xml")
print("DEBUG: XML Parsed Successfully. Data Loaded.")

# Assuming the 'data' list contains dictionaries, extracting the first dictionary
first_dictionary = data[0]

# Extracting specific data elements from the dictionary
# (Assigning each value to individual variables for further use)
measuring_result = first_dictionary['measuring_result']
print("measuring_result =", measuring_result)
measuring_value_probe = first_dictionary['measuring_value_probe']
print("measuring_value_probe =", measuring_value_probe)
measuring_result_error = first_dictionary['measuring_result_error']
print("measuring_result_error =", measuring_result_error)
next_recalibration_date = first_dictionary['next_recalibration_date']
print("next_recalibration_date =", next_recalibration_date)
certificate_number = first_dictionary['certificate_number']
print("next_recalibration_date =", next_recalibration_date)
head_cft = first_dictionary['head_cft']
print("head_cft =", head_cft)
calibrated_by = first_dictionary['calibrated_by']
print("calibrated_by =", calibrated_by)
checked_by = first_dictionary['checked_by']
print("checked_by =", checked_by)
scientist_incharge = first_dictionary['scientist_incharge']
print("scientist_incharge =", scientist_incharge)
customer_name = first_dictionary['customer_name']
print("customer_name =", customer_name)
customer_street = first_dictionary['customer_street']
print("customer_street =", customer_street)
customer_city = first_dictionary['customer_city']
print("customer_city =", customer_city)
customer_postal_code = first_dictionary['customer_postal_code']
print("customer_postal_code =", customer_postal_code)
customer_reference = first_dictionary['customer_reference']
print("customer_reference =", customer_reference)
item_name = first_dictionary['item_name']
print("item_name =", item_name)
model_no = first_dictionary['model_no']
print("model_no =", model_no)
serial_no = first_dictionary['serial_no']
print("serial_no =", serial_no)
temperature = first_dictionary['temperature']
print("temperature =", temperature)
humidity_final = first_dictionary['humidity_final']
print("humidity_final =", humidity_final)
equipment_type = first_dictionary['equipment_type']
print("equipment_type =", equipment_type)
associated_uncertainity = first_dictionary['associated_uncertainity']
print("associated_uncertainity =", associated_uncertainity)
coverage_factor = first_dictionary['coverage_factor']
print("coverage_factor =", coverage_factor)
coverage_probablity = first_dictionary['coverage_probablity']
print("coverage_probablity =", coverage_probablity)
distribution_type = first_dictionary['distribution_type']
begin_calibration_date = first_dictionary['begin_calibration_date']
end_calibration_date = first_dictionary['end_calibration_date']

# Defining a class for generating LaTeX content
class LatexGenerator:
    def __init__(self):
        print("DEBUG: LatexGenerate pdf")
        pass
    
    # Method to split a string by spaces and process the values
    def change(self, string):
        print(f"DEBUG: Splitting value for: {string}")
        split_values = string.split()
        print("DEBUG: Split value=", split_values)
        processed_values = []
        current = ""

        for val in split_values:
            if val.startswith('\\'):
                current += f" {val}"
            else:
                if current:
                    processed_values.append(current.strip())
                    current = ""
                processed_values.append(val)

        if current:
            processed_values.append(current.strip())

        print("DEBUG: Process value:", processed_values)
        return processed_values

    # Method to generate a LaTeX table with a headline and data
    def generate_latex_table_with_headline(self, lists):
        print("DEBUG: Generating latex Table")
        print("DEBUG: List ", lists)
        num_columns = len(lists)
        num_rows = max(len(lst) for lst in lists)

        headline = ["Nominal Value (in V)", "Measured Value(in V)", "Error(in V)"]

        table = "\\begin{tabular}{|" + "|".join(["c"] * num_columns) + "|}\n"
        table += "\\hline\n"
        
        # Add headline
        table += " & ".join(headline) + " \\\\\n"
        table += "\\hline\n"

        for i in range(num_rows):
            row = [lst[i] if i < len(lst) else '' for lst in lists]
            table += " & ".join(row) + " \\\\\n"
            table += "\\hline\n"

        table += "\\end{tabular}"
        print("DEBUG: Table generated")
        return table

    # Method to generate LaTeX content using extracted data
    def generate_latex_content(self):
        print("DEBUG: start latex Generation")
        measuring_result_list = self.change(measuring_result)
        measuring_value_probe_list = self.change(measuring_value_probe)
        measuring_result_error_list = self.change(measuring_result_error)

        print("DEBUG: Creating table..")
        latex_table = self.generate_latex_table_with_headline([measuring_result_list, measuring_value_probe_list, measuring_result_error_list])
        

        print("DEBUG: Embedding all value into Latex templte")
        # Accessing XML data and creating LaTeX content
        latex_content = f'''
        \\documentclass[a4paper]{{article}}

        % Load necessary packages for using Arial-like font
        \\usepackage[a-3u]{{pdfx}} % For PDF/X compliance
        \\usepackage{{attachfile}} % For attaching files to the PDF
        \\usepackage{{geometry}} % For setting page geometry
        \\usepackage{{fancyhdr}} % For custom headers and footers
        \\usepackage{{graphicx}} % For including graphics
        \\usepackage{{color}} % For adding color
        \\usepackage{{helvet}}  % Helvetica clone
        \\usepackage{{embedfile}} % For embedding files
        \\usepackage{{tabularx}} % For the tabularx environment
        \\usepackage{{siunitx}} % For typesetting units
        \\usepackage{{lastpage}} % For page number references

        % Set Arial-like font as the default sans-serif font
        \\renewcommand{{\\familydefault}}{{\\sfdefault}}

        % Setting up fancy headers and footers  
        \\fancyhf{{}}
        \\fancyhead[L]{{\\includegraphics[width=0.18\\textwidth,height=25.0mm]{{logo.png}} \\\\[3pt]}}
        \\fancyhead[R]{{
            Date: {{\\today}} \\\\
            Next Calibration Date: {next_recalibration_date} \\\\
            {{Page \\thepage}} \\\\
            Certificate Number: {certificate_number} \\\\[2pt]
        }}
        \\fancyfoot[L]{{
            \\setlength{{\\tabcolsep}}{{1pt}} % Adjusting column separation
                \\begin{{tabularx}}{{\\textwidth}}{{@{{\\extracolsep{{0.001pt}}}} p{{0.1\\textwidth}} X X X X X X X X}}  % Adjusting column widths
                    Head CFT: & & Calibrated By: & & Checked By: & & Scientist incharge: & \\\\
                    & ({head_cft}) & & ({calibrated_by}) & & ({checked_by}) & & ({scientist_incharge}) \\\\
                \\end{{tabularx}}
                \\vspace{{0.1 cm}}
        }} 

        % Setting page style, header, and footer properties
        \\setlength{{\\headheight}}{{25mm}}
        \\pagestyle{{fancy}}
        \\renewcommand{{\\headrulewidth}}{{0.8pt}}
        \\renewcommand{{\\footrulewidth}}{{0.8pt}}
        \\renewcommand{{\\familydefault}}{{\\sfdefault}}
        \\newcommand{{\\embedmyfile}}[1]{{\\embedfile{{#1}}}} % Command to embed a file

        % Begin document
        % Document content starts here

        \\begin{{document}} 
            % Embedding a file 'attachment.xml'
            \\embedfile{{attachment.xml}}
            \\begin{{center}}
                {{\\fontfamily{{phv}}\\fontsize{{18pt}}{{20pt}}\\selectfont\\textbf{{\\textcolor{{black}}{{\\\\[3pt]Calibration Certificate : {item_name}}}}}}}
            \\end{{center}}
            
            \\vspace{{2cm}}  % Adding some vertical space
            
            \\renewcommand{{\\arraystretch}}{{1.5}} % Increasing row height
            
            \\begin{{center}}
                \\setlength{{\\tabcolsep}}{{12pt}} % Adjusting column separation
                \\begin{{tabularx}}{{\\textwidth}}{{@{{\\extracolsep{{8pt}}}} p{{0.4\\textwidth}} X}}  % Adjusting column widths
                    1. Calibrated for: & {customer_name} \\\\
                    & {customer_street} \\\\
                    & {customer_city} \\\\
                    & {customer_postal_code} \\\\
                    & {customer_reference} \\\\
                    &  \\\\
                    2. Description and Identification of instrument: & {item_name} \\\\
                    & {model_no} \\\\
                    & {serial_no} \\\\
                    & \\\\
                    3. Environmental Conditions:
                    & Temperature: {{{temperature}}} \\\\
                    & Humidity: ({{{humidity_final}}})\\% \\\\ 
                    & \\\\
                    4. Standard(s) Used: & {equipment_type} \\\\
                    Associated Uncertainity: & {associated_uncertainity} \\\\
                    & \\\\
                    5. Traceability of standard(s) used: & {equipment_type} (Primary Standard)\\\\
                    & \\\\
                    6. Principle/ Methodology of Calibration: & The {item_name} has been calibrated by comarison method with {equipment_type} as per calibration procedure no. \\\\
                \\end{{tabularx}}
            \\end{{center}}

            \\pagebreak
            7. Measurements:   \\\\
            \\begin{{center}}
                {latex_table} \\\\
            \\vspace{{0.5 cm}}  
            \\end{{center}}
            The report expanded uncertainity is at a coverage factor k + {coverage_factor} which corresponds approximaltely {coverage_probablity}\% for a {distribution_type} distribution. \\\\
            \\\\

            \\begin{{flushleft}}
                \\setlength{{\\tabcolsep}}{{1pt}} % Adjusting column separation
                \\begin{{tabularx}}{{\\textwidth}}{{@{{\\extracolsep{{8pt}}}} p{{0.4\\textwidth}} X}}  % Adjusting column widths
                    8. Dates of Calibration: & {begin_calibration_date} to {end_calibration_date} \\\\
                    & \\\\
                    9. Remarks: & (i) The {item_name} has been calibrated \\\\
                    & (ii) The noise of the {item_name} is inclusive 
                \\end{{tabularx}}
                \\vspace{{2 cm}}
            \\end{{flushleft}}
        \\end{{document}}
        '''

        print("DEBUG: Latex content generated sucessfully")
        # Return the latex content
        return latex_content
