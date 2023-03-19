# Import Modules
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import ImageTk, Image, ImageOps
from fpdf import FPDF
from tkinter import filedialog

# Configure Workspace
root = tk.Tk()
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)  # disable window from resizing
root.title("Photo Inspection Report")
root.geometry('754x1000')
# 1080p - window size = 754x1000, 1440p = 1018x1360) - need to account for task bar
root.configure(bg="#ffffff")

# Fonts
font_heading = ('Arial Narrow Bold', 12)
font_body = ('Arial Narrow', 10)


# Create data model/entry structure
class FormDataModel:
    def __init__(self, reportnumber, reportdate, reporttype,
                 image1_path, image2_path, image3_path, image4_path):
        self.reportnumber = reportnumber
        self.reportdate = reportdate
        self.reporttype = reporttype
        self.image1_path = image1_path
        self.image2_path = image2_path
        self.image3_path = image3_path
        self.image4_path = image4_path


# creating data model using class
currentdata = FormDataModel("", "", "", "", "", "", "")


# Extracts input from entry fields and adds to instance of object
def updateinput(*args):
    currentdata.reportdate = date_var.get()
    currentdata.reportnumber = reportnumber_var.get()
    currentdata.reporttype = inspection_type.get()

    print(currentdata.reportdate)
    print(currentdata.reportnumber)
    print(currentdata.reporttype)


# Update variables as input is entered into entry fields using trace method
date_var = tk.StringVar()
date_var.trace_add("write", updateinput)
reportnumber_var = tk.StringVar()
reportnumber_var.trace_add("write", updateinput)
inspection_type = tk.StringVar()
inspection_type.trace_add("write", updateinput)

# Inspection Type
inspectiontype_label = tk.Label(root,
                                text=f'Inspection Type:',
                                padx=0, pady=0,
                                bg='#ffffff',
                                font=font_heading)
inspectiontype_label.place(x=150, y=125, anchor='e')

inspectiontype_combo = ttk.Combobox(root,
                                    font=font_body,
                                    textvariable=inspection_type)
inspectiontype_combo['values'] = ['Piers',
                                  'Footings',
                                  'Slab on Ground',
                                  'Slab & Footings',
                                  'Suspended Slab']
inspectiontype_combo.place(x=160, y=125, anchor='w')


# Date
date_label = tk.Label(root,
                      text=f'Date:',
                      padx=0, pady=0,
                      bg='#ffffff',  # background colour
                      font=font_heading)
date_label.place(x=150, y=50, anchor='e')  # position

date_entry = DateEntry(root,
                       width=10,
                       bg="#fffff",
                       year=2023,
                       font=font_body,
                       date_pattern='dd/mm/yyyy',
                       justify="center",
                       textvariable=date_var)
date_entry.place(x=160, y=50, anchor='w')  # position


# Report Number
reportnumber_label = tk.Label(root,
                              text=f'Report Number:',
                              padx=0, pady=0,
                              bg='#ffffff',
                              font=font_heading)
reportnumber_label.place(x=150, y=100, anchor='e')  # position

reportnumber_entry = tk.Entry(root,
                              width=12,
                              font=font_body,
                              justify="center",
                              textvariable=reportnumber_var)
reportnumber_entry.place(x=160, y=100, anchor='w')  # position

# Job Number

# Job Address

# Job Description

# Client

# Contractor


# Photo Fields - Buttons
class TKImage:
    def __init__(self, image_path, pos_x_image, pos_y_image):
        self.image_path = image_path
        self.pos_x_image = pos_x_image
        self.pos_y_image = pos_y_image

    def add_image(self):
        # Hide previous image
        canvas = tk.Canvas(root, height=360, width=360, highlightthickness=0, bd=0, relief='ridge', borderwidth=0)
        canvas.place(x=self.pos_x_image, y=self.pos_y_image, anchor='center')
        canvas.create_rectangle(0, 0, 360, 360, fill="white", outline="")

        # Add new image
        self.image_path = tk.filedialog.askopenfilename(filetypes=[("Image File", '.jpg')])
        # Check to see if user cancels - cancelling returns empty tuple
        if str(self.image_path) == '':
            pass
        else:
            img = Image.open(self.image_path)  # open image
            img_resize = ImageOps.contain(img, (350, 350))  # resize image
            img_tk = ImageTk.PhotoImage(img_resize)  # convert to tkinter image

            img_addimage = tk.Label(root, image=img_tk)  # Add image to root window
            img_addimage.image = img_tk  # create reference to image
            img_addimage.place(x=self.pos_x_image, y=self.pos_y_image, anchor='center')  # Location of image


# Image 1
image1_tk = TKImage(currentdata.image1_path, 190, 405)  # Class
button_image1 = tk.Button(root, text='Open Image', command=image1_tk.add_image)  # Create button using class
button_image1.place(x=190, y=605, anchor='s')  # Placement of button withing Root window

# Image 2
image2_tk = TKImage(currentdata.image2_path, 565, 405)
button_image2 = tk.Button(root, text='Open Image', command=image2_tk.add_image)
button_image2.place(x=560, y=605, anchor='s')

# Image 3
image3_tk = TKImage(currentdata.image3_path, 190, 785)
button_image3 = tk.Button(root, text='Open Image', command=image3_tk.add_image)
button_image3.place(x=190, y=985, anchor='s')

# Image 4
image4_tk = TKImage(currentdata.image4_path, 565, 785)
button_image4 = tk.Button(root, text='Open Image', command=image4_tk.add_image)
button_image4.place(x=560, y=985, anchor='s')

# Photo Labels


class PDFImage:
    def __init__(self, pdf_instance, image, pos_x, pos_y):
        self.pdf_instance = pdf_instance
        self.image = image
        self.pos_x = pos_x
        self.pos_y = pos_y

    def create_image(self):
        if self.image == "":
            pass
        else:
            # Open image & get size
            img_pdf = Image.open(self.image)  # open image
            img_width, img_height = img_pdf.size

            # Resize image based on aspect ratio
            if img_height >= img_width:
                factor = img_width / img_height
                img_height_adjusted = 75
                img_width_adjusted = (img_height_adjusted * factor)
            else:
                factor = img_height / img_width
                img_width_adjusted = 75
                img_height_adjusted = (img_width_adjusted * factor)

            # Place image in PDF
            self.pdf_instance.image(img_pdf,
                                    x=self.pos_x,
                                    y=self.pos_y,
                                    w=img_width_adjusted,
                                    h=img_height_adjusted)


def printpdf():
    # Initiate PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')  # A4 = 210mm x 297mm

    # Add a page
    pdf.add_page()

    # Add Date
    datevariable = currentdata.reportdate  # Retrieve report date
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 7, 'Date:', align='R', border=False)  # Date Label
    pdf.set_font('helvetica', '', 10)
    pdf.cell(30, 7, datevariable, align='L', border=False, new_x="LMARGIN", new_y="NEXT")  # Date

    # Add Report Number
    reportnumber_pdf = currentdata.reportnumber  # Retrieve report number
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 7, 'Report Number:', align='R', border=False)  # Report Number Label
    pdf.set_font('helvetica', '', 10)
    pdf.cell(30, 7, reportnumber_pdf, align='L', border=False, new_x="LMARGIN", new_y="NEXT")  # Report Number

    # Add Report Type
    reporttype_pdf = currentdata.reporttype  # Retrieve report type
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 7, 'Report Type:', align='R', border=False)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(30, 7, reporttype_pdf, align='L', border=True, new_x="LMARGIN", new_y="NEXT")

    # Add Logo
    logo_pdf = Image.open('WP_Logo_Colour.png')
    pdf.image(logo_pdf, x=150, y=15, h=25)

    # Add Images - created class for adding images - pulls pathway from data model
    currentdata.image1_path = image1_tk.image_path  # Get image path from TKinter Class Instance
    image1 = PDFImage(pdf, currentdata.image1_path, 10, 55)  # Create instance of Image class
    image1.create_image()  # Call class method

    currentdata.image2_path = image2_tk.image_path
    image2 = PDFImage(pdf, currentdata.image2_path, 150, 55)
    image2.create_image()

    currentdata.image3_path = image3_tk.image_path
    image3 = PDFImage(pdf, currentdata.image3_path, 10, 150)
    image3.create_image()

    currentdata.image4_path = image4_tk.image_path
    image4 = PDFImage(pdf, currentdata.image4_path, 150, 150)
    image4.create_image()

    # Top Border
    pdf.set_line_width(0.5)
    pdf.set_draw_color(r=0, g=0, b=0)
    pdf.line(x1=5, y1=50, x2=205, y2=50)

    # Print to standardised name using input information (Date - Description - Report Number)
    pdf.output('test.pdf')
    # pdf.output(currentdata.reportnumber + 'data information' + '.pdf')


# Print to PDF
createPDF_button = tk.Button(root, text='Print Report', command=printpdf)
createPDF_button.place(x=200, y=200, anchor='e')


# infinite loop
root.tk.mainloop()
