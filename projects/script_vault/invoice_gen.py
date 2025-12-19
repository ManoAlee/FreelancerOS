from reportlab.pdfgen import canvas
import csv
import os

def generate_invoice(client_name, amount, filename="invoice.pdf"):
    """Generates a simple PDF invoice."""
    c = canvas.Canvas(filename)
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "INVOICE")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Client: {client_name}")
    c.drawString(100, 680, f"Date: 2025-12-18")
    
    c.line(100, 660, 500, 660)
    
    c.drawString(100, 630, "Description")
    c.drawString(400, 630, "Amount")
    
    c.drawString(100, 600, "Freelance Services")
    c.drawString(400, 600, f"${amount}")
    
    c.line(100, 580, 500, 580)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(300, 550, f"Total Due: ${amount}")
    
    c.save()
    print(f"🧾 Invoice generated: {filename}")

if __name__ == "__main__":
    print("--- INVOICE GENERATOR ---")
    client = input("Client Name: ") or "John Doe"
    amt = input("Amount ($): ") or "500"
    generate_invoice(client, amt)
