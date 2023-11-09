from fpdf import FPDF


def create_test() -> str:
    data = [
        {"First name": "Jules", "Last name": "Smith", "Age": 34, "City": "San Juan"},
        {"First name": "Mary", "Last name": "Ramos\n \n Ramos \n    Ramos", "Age": 45, "City": "Orlando"},
        {"First name": "Lucas", "Last name": "Cimon",
         "Age": "Saint-Mahturin-sur-Loire - it may even be so long that multiple lines are needed to write it down "
                "completely",
         "City": 49},
        {"First name": "Carlson", "Last name": "Banks", "Age": 19, "City": "Los Angeles"},
    ]
    pdf = FPDF("P", "mm", "a4")
    pdf.set_font("arial", "B", 14)
    pdf.add_page()
    col_width = pdf.w / 6
    line_height = 10

    for row in data:
        row_height_lines = 1
        lines_in_row = []

        for j, datum in enumerate(row.values()):  # Extract values from the dictionary
            if j == 2:
                col_width = pdf.w / 12  # Change the width for the third column
            else:
                col_width = pdf.w / 6  # Reset the width for other columns
            output = pdf.multi_cell(col_width, line_height, str(datum), border=1, ln=3, split_only=True)
            lines_in_row.append(len(output))
            if len(output) > row_height_lines:
                row_height_lines = len(output)

        for tlines, datum in zip(lines_in_row, row.values()):  # Extract values from the dictionary
            text = str(datum).rstrip('\n') + (1 + row_height_lines - tlines) * '\n'
            pdf.multi_cell(col_width, line_height, text, border=1, ln=3)

        pdf.ln(row_height_lines * line_height)
    pdf.ln(10)
    pdf.output(f"files/scolarite.pdf", "F")
    return f"files/scolarite.pdf"

