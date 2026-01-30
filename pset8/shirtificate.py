from fpdf import FPDF
def main():
    name = input("Name: ")
    pdf = FPDF(orientation='P', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 30, "CS50 Shirtificate", align='C', ln=True)
    pdf.image("shirtificate.png", x=49, y=80, w=100)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.set_xy(0, 120)
    pdf.cell(0, 10, name, align='C')
    pdf.output("shirtificate.pdf")

if __name__ == "__main__":
    main()

