# StrawCrisERP - A Simple Inventory Management System for Small-Scale Electronic Components

[简体中文](README_ZH.md)
This is an inventory management system for electronic components built using the Python **Quart** framework. It uses the **AdminLTE** frontend template and the **HTML5 QR Code** library to implement QR code scanning functionality.

The system allows easy management of inventory, supports scanning to add components (currently only supports labels from LCSC and Digi-Key), filtering inventory components, editing information, retrieving components one by one, and comparing with BOM (Bill of Materials).

**Note:** This project is currently designed for local network use only. For deployment in a public network environment, please **ensure** you **add login password encryption** and perform necessary security checks.

## Features

- **Inventory Management**: Supports scanning/uploading files to add, editing information, filtering inventory components, comparing with BOM, etc.
- **QR Code Scanning**: Easily add/update/retrieve components by scanning QR codes.
- **Lightweight**: Only requires Python and MySQL to run.

## Installation & Usage

### Prerequirements

- Python 3.7+
- pip
- MySQL

### Install Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/hedgehog-qd/StrawCrisERP.git
   cd StrawCrisERP
   ``` 

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ``` 

3. Create and import the MySQL database:
   ```mysql
   CREATE DATABASE strawcriserp;
   USE strawcriserp;
   SOURCE /path/to/your/strawcriserp.sql;
   ``` 

4. Modify the configuration file `config.py`:
   ```python
   # Port Config
   port = 5000                  # The port on which you want the website to run

   # Mysql Config
   db_host = "localhost"        # MySQL host
   db_port = 3306               # MySQL port
   db_user = "strawcris"        # MySQL username
   db_passwd = "password"      # Password for the user
   db_name = "strawcriserp"     # Database name
   ``` 

5. Start the server:
   ```bash
   python main.py
   ``` 

6. If you want to run the application in the background, you can use `screen` or `nohup`.

## Feature Introduction

### Search (Search for Materials)
In the search page, you can use tags to search for components. Each tag represents a keyword, and you can add or delete tags freely.  
![Search](/images/search.png)  
![Using Tags](/images/search_tag.png)

### View All Entries (View All)
On this page, you can view all the current inventory information.  
![View All](/images/viewall.png)

### Add New Item (Add New Item)
When you purchase components, you can either add individual components on this page or directly upload a batch purchase file. Our backend will automatically process and format the data for you.  
![Add New Page](/images/addnew.png)  
![Add New Upload](/images/addnew_uploadfile.png)

- If you choose to upload a file in bulk, please ensure that the column names in your file match the required format. You can click *Download the Example* to get the sample template.  
- If you choose to add individual components, you can use the QR Scanner tool. This tool will help you automatically fill in necessary information such as MPN, quantity, SPN, and supplier.  
![Single Scan](/images/addnew_scanQR.png)

### Edit Existing Items (Edit Item)
When you inventory your stock, you can edit existing component data on this page, such as the manufacturer, purchase date, or adjust quantities. Note that you must first fill in the MPN (which can be automatically filled by scanning), and after the backend confirms the stock is available, you can modify the details.  
![Edit Page](/images/edit.png)

### Retrieve Items (Check Out)
When you finish your design or start implementation, you can retrieve items from the inventory here. You can upload a BOM (Bill of Materials) exported from your EDA software (you may need to modify two column names; the system will prompt you).  
The system will compare which components are in stock, which are missing, or if the quantity is insufficient. After the comparison, you can choose to subtract the inventory of the components listed in the BOM.  
You can also retrieve items one by one by entering the MPN (or scanning) and the required quantity, then clicking submit.  
![Checkout Page](/images/checkout.png)

## Conclusion
Feel free to try it out! If you encounter any issues, please submit an issue. Thank you!
