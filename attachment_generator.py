import xml.etree.ElementTree as ET

class AttachmentXMLGenerator:

    def __init__(self):
        self.DCC_NS = "https://ptb.de/dcc"
        self.SI_NS = "https://ptb.de/si"
        ET.register_namespace("dcc", self.DCC_NS)
        ET.register_namespace("si", self.SI_NS)

    def generate_xml(self, data_dict, output_path="attachment.xml"):
        """
        data_dict comes directly from data_to_send in execute_pdf_generator()
        """

        dcc = f"{{{self.DCC_NS}}}"
        si = f"{{{self.SI_NS}}}"

        root = ET.Element(
            f"{dcc}digitalCalibrationCertificate",
            attrib={
                "schemaVersion": "3.3.0"
            }
        )

        # -----------------------
        # administrativeData
        # -----------------------
        admin = ET.SubElement(root, f"{dcc}administrativeData")

        # --- coreData ---
        core = ET.SubElement(admin, f"{dcc}coreData")

        ET.SubElement(core, f"{dcc}uniqueIdentifier").text = data_dict.get("certificate_no", "")

        ET.SubElement(core, f"{dcc}beginPerformanceDate").text = data_dict.get("calibration_date", "")
        ET.SubElement(core, f"{dcc}endPerformanceDate").text = data_dict.get("end_date", "")

        # -----------------------
        # Persons Section
        # -----------------------
        persons = ET.SubElement(admin, f"{dcc}respPersons")

        def add_person(name):
            p = ET.SubElement(persons, f"{dcc}respPerson")
            pp = ET.SubElement(p, f"{dcc}person")
            n = ET.SubElement(pp, f"{dcc}name")
            ET.SubElement(n, f"{dcc}content").text = data_dict.get(name, "")
            return p

        add_person("tested_by")
        add_person("calibrated_by")
        add_person("checked_by")
        add_person("incharge")
        add_person("issued_by")

        # -----------------------
        # measurementResults
        # -----------------------
        meas_results = ET.SubElement(root, f"{dcc}measurementResults")
        meas_result = ET.SubElement(meas_results, f"{dcc}measurementResult")

        # Name
        name = ET.SubElement(meas_result, f"{dcc}name")
        ET.SubElement(name, f"{dcc}content").text = "Measurement Results"

        # -------------- result_table -------------
        results = ET.SubElement(meas_result, f"{dcc}results")
        result = ET.SubElement(results, f"{dcc}result", attrib={"refType": "gp_measuringResult"})

        data = ET.SubElement(result, f"{dcc}data")
        lst = ET.SubElement(data, f"{dcc}list", attrib={"refType": "gp_table1"})

        # Parse result_table (LaTeX → cleaned values)
        latex = data_dict.get("result_table", "")
        values = self.extract_values_from_latex(latex)

        # Example: Reference Values
        q = ET.SubElement(lst, f"{dcc}quantity", attrib={"refType": "basic_referenceValue"})
        qname = ET.SubElement(q, f"{dcc}name")
        ET.SubElement(qname, f"{dcc}content").text = "Reference value"

        real_list = ET.SubElement(q, f"{si}realListXMLList")
        v = ET.SubElement(real_list, f"{si}valueXMLList")
        v.text = " ".join(values)

        u = ET.SubElement(real_list, f"{si}unitXMLList")
        u.text = "\\volt"  # default

        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print("attachment.xml created successfully:", output_path)


    def extract_values_from_latex(self, latex_table):
        """
        Clean latex table rows and convert to XML numeric list.
        """
        import re
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", latex_table)
        return nums
