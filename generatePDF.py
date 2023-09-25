import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mysql.connector


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="ivica15%",
    database="twitterapp"
)

cursor = db.cursor()

cursor.execute("Select count(ID) as PositiveNumber from twitterapp.analysis WHERE Result = 'positive'")
positive_number = cursor.fetchone();

cursor.execute("select count(ID) as NegativeNumber from twitterapp.analysis WHERE Result = 'negative'")
negative_number = cursor.fetchone();


totalRecords = positive_number[0] + negative_number[0]

positive_percent = (positive_number[0] / totalRecords)*100
negative_percent = (negative_number[0] / totalRecords)*100


# Pie chart data
labels = ['Positive', 'Negative']
sizes = [positive_percent, negative_percent]
colors = ['green', 'red']
explode = (0.1, 0)  # Explode the first slice (Positive)

# Create the pie chart for positive and negative comments
plt.figure(figsize=(8, 4))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
plt.title('Analysis on shoe product')

# Save the pie chart as an image file
plt.savefig('pie_chart.png', bbox_inches='tight', dpi=300)

# Create a PDF document and add the pie chart as an image to it
pdf_file = "analysis_report.pdf"

# Create the PDF canvas
c = canvas.Canvas(pdf_file, pagesize=letter)

# Draw the pie chart image on the PDF
c.drawImage('pie_chart.png', 100, 400, width=400, height=300)

# Add a title and description
c.setFont("Helvetica", 16)
c.drawString(100, 750, "New Shoe Design Release")
c.setFont("Helvetica", 12)
c.drawString(100, 730, "Analysis Results on Customers' Experience.")

# Close the PDF canvas
c.save()

# Display the pie chart
plt.show()
