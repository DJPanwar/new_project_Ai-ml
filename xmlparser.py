# Import necessary libraries
import xml.etree.ElementTree as ET
import xmlschema
from datetime import datetime

# Define a class for XML parsing and processing
class XMLParser:
    def __init__(self):
        pass

    # Method to validate XML against XSD schema
    def validate_xml(self, xml_file_path, xsd_file_path):
        try:
            # Load the XML schema and validate against XML file
            schema = xmlschema.XMLSchema(xsd_file_path)
            schema.validate(xml_file_path)
            print("Validation successful: The XML is valid against the XSD.")
            return True
        
        except xmlschema.XMLSchemaValidationError as e:
            # Handle validation errors
            print("Validation failed: The XML is not valid against the XSD.")
            print("Validation errors:")
            for error in e.errors:
                print(error)
            
        except Exception as e:
            # Handle other exceptions during validation
            print("An error occurred:", str(e))
            return False

    # Method to parse XML and extract relevant data
    def parse_xml(self, xml_file_path):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            dcc = "{https://ptb.de/dcc}"
            si = "{https://ptb.de/si}"
            today = datetime.today()

            # Extract various data elements from the XML tree using XPath
            certificate_number = root.find(f'.//{dcc}uniqueIdentifier').text
            next_recalibration_date = root.find(f'.//{dcc}statement/{dcc}date').text

            customer_name = root.find(f'.//{dcc}customer/{dcc}name/{dcc}content').text
            customer_street = root.find(f'.//{dcc}calibrationLaboratory/{dcc}contact/{dcc}location/{dcc}street').text
            customer_city = root.find(f'.//{dcc}calibrationLaboratory/{dcc}contact/{dcc}location/{dcc}city').text
            customer_postal_code = root.find(f'.//{dcc}calibrationLaboratory/{dcc}contact/{dcc}location/{dcc}postCode').text
            customer_reference = root.find(f'.//{dcc}customer/{dcc}location/{dcc}further/{dcc}content').text

            item_name = root.find(f'.//{dcc}items/{dcc}item/{dcc}name/{dcc}content').text
            model_no = root.find(f'.//{dcc}items/{dcc}item/{dcc}model').text
            serial_no = root.find(f'.//{dcc}items/{dcc}item/{dcc}identifications/{dcc}identification/{dcc}name/{dcc}content').text

            temperature = root.find(f'.//{dcc}influenceConditions/{dcc}influenceCondition/{dcc}name/{dcc}content[2]').text
            temperature = '$'+ temperature.replace('±', '\\pm') +'$'

            min_humidity = root.find(f'.//{dcc}influenceConditions/{dcc}influenceCondition[2]/{dcc}data/{dcc}quantity/{si}real/{si}value').text
            min_humidity_unit = root.find(f'.//{dcc}influenceConditions/{dcc}influenceCondition[2]/{dcc}data/{dcc}quantity/{si}real/{si}unit').text
            min_humidity_unit = min_humidity_unit.replace('\\', '\\textbackslash ')

            max_humidity = root.find(f'.//{dcc}influenceConditions/{dcc}influenceCondition[2]/{dcc}data/{dcc}quantity[2]/{si}real/{si}value').text
            max_humidity_unit = root.find(f'.//{dcc}influenceConditions/{dcc}influenceCondition[2]/{dcc}data/{dcc}quantity[2]/{si}real/{si}unit').text
            max_humidity_unit = max_humidity_unit.replace('\\', '\\textbackslash ')

            equipment_type = root.find(f'.//{dcc}measuringEquipments/{dcc}measuringEquipment/{dcc}name/{dcc}content').text
            associated_uncertainity = root.find(f'.//{dcc}measuringEquipments/{dcc}measuringEquipment/{dcc}identifications/{dcc}identification/{dcc}value').text

            head_cft = root.find(f'.//{dcc}respPersons/{dcc}respPerson/{dcc}person/{dcc}name/{dcc}content').text
            calibrated_by = root.find(f'.//{dcc}respPersons/{dcc}respPerson[2]/{dcc}person/{dcc}name/{dcc}content').text
            checked_by = root.find(f'.//{dcc}respPersons/{dcc}respPerson[3]/{dcc}person/{dcc}name/{dcc}content').text
            scientist_incharge = root.find(f'.//{dcc}respPersons/{dcc}respPerson[4]/{dcc}person/{dcc}name/{dcc}content').text

            measuring_result = root.find(f'.//{dcc}data/{dcc}list/{dcc}quantity/{si}realListXMLList/{si}valueXMLList').text
            measuring_value_probe = root.find(f'.//{dcc}data/{dcc}list/{dcc}quantity[2]/{si}hybrid/{si}realListXMLList/{si}valueXMLList').text
            measuring_result_error = root.find(f'.//{dcc}data/{dcc}list/{dcc}quantity[3]/{si}realListXMLList/{si}expandedUncXMLList/{si}uncertaintyXMLList').text
            coverage_factor = root.find(f'.//{dcc}data/{dcc}list/{dcc}quantity[3]/{si}realListXMLList/{si}expandedUncXMLList/{si}coverageFactorXMLList').text
            coverage_probablity = root.find(f'.//{dcc}data/{dcc}list/{dcc}quantity[3]/{si}realListXMLList/{si}expandedUncXMLList/{si}coverageProbabilityXMLList').text
            distribution_type = root.find(f'.//{dcc}data/{dcc}list/{dcc}quantity[3]/{si}realListXMLList/{si}expandedUncXMLList/{si}distributionXMLList').text

            begin_calibration_date = root.find(f'.//{dcc}coreData/{dcc}beginPerformanceDate').text
            end_calibration_date = root.find(f'.//{dcc}coreData/{dcc}endPerformanceDate').text

            coverage_probablity = float(coverage_probablity)
            coverage_probablity = 100*coverage_probablity

            int_max_humidity = int(max_humidity)
            int_min_humidity = int(min_humidity)
            diff = (int_max_humidity + int_min_humidity) / 2
            diff1 = (diff - int_min_humidity)

            string_unit_diff = str(diff) if diff % 1 != 0 else str(int(diff))
            string_error_diff = str(diff1) if diff1 % 1 != 0 else str(int(diff1))

            humidity_final = '$' + string_unit_diff + '\\pm' + string_error_diff + '$'
            humidity_unit = '%'  

            # Construct a dictionary with extracted data  
            data = [
                {
                    "next_recalibration_date": next_recalibration_date,
                    "certificate_number": certificate_number,
                    "head_cft": head_cft,
                    "calibrated_by": calibrated_by,
                    "checked_by": checked_by,
                    "scientist_incharge": scientist_incharge,
                    "customer_name": customer_name,
                    "customer_street": customer_street,
                    "customer_city": customer_city,
                    "customer_postal_code": customer_postal_code,
                    "customer_reference": customer_reference,
                    "item_name": item_name,
                    "model_no": model_no,
                    "serial_no": serial_no,
                    "temperature": temperature,
                    "humidity_final": humidity_final,
                    "equipment_type": equipment_type,
                    "associated_uncertainity": associated_uncertainity,
                    "coverage_factor": coverage_factor,
                    "coverage_probablity": coverage_probablity,
                    "distribution_type": distribution_type,
                    "begin_calibration_date": begin_calibration_date,
                    "end_calibration_date": end_calibration_date,
                    "measuring_result" : measuring_result,
                    "measuring_value_probe" : measuring_value_probe,
                    "measuring_result_error" : measuring_result_error,
                    "humidity_unit" : humidity_unit,
                    "today" : today
                }
            ]
            # Return the extracted data as a list of dictionaries
            return data 

        except Exception as e:
            print("Error parsing XML:", str(e))
            raise
    