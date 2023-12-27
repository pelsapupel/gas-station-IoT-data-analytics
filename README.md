# Pertamina Gas Station Data Analytics Project (MySQL)
## Overview
Welcome to the My Pertamina Gas Station Data Analytics Project! This project focuses on analyzing and managing data related to transactions, stock, equipment, and shipping at Pertamina gas stations. As a data analyst, I have been actively involved in the development and production phases of this project, utilizing MySQL for data manipulation during development and Python along with shell scripts for automating the creation of the datamart in the production phase. In this SQL project, I use data from PT. Pertamina Patra Niaga (Commercial & Trading) and colaborated with more than 100 people. Keep in mind that I will only show dataset that complies with Indonesian data privacy law and masked any private or any crucial data, as it is not necessary for the porfolio.

## Project Structure
The project is organized into two main phases: development and production.

## Development Phase
In the development phase, the primary goal is to explore the potential of the data and to create a sustaining analysis and manipulation that are going to be useful for the next 8 years (the estimated lifecycle of our dashboard product). The data sources include transaction records, stock information, equipment data, and shipping details from Pertamina. The SQL scripts are designed to clean, aggregate, and prepare the data for further analysis.

## Data Modeling
I coordinated with a the Database Administrator to formulate the best way to present data, ways for performance optimization for query and job scheduling & plavement to move forward with the analysis.

## SQL Scripts
### Transaction Analysis: 
pertamina_dashboard_5_1_cash_non_cash_period.sql
This script focuses on extracting and analyzing transaction data, including sales, payment methods, number plate, vehicle types and types of transaction.

### Stock Management: 
pertamina_dashboard_1_6_ketahanan_stock_period.sql
Manages stock-related information, tracking inventory levels, restocking and identifying slow-moving items.

### Equipment and Human Factors Insights: 
equipment_insights.sql
Extracts insights from equipment data, such as nozzle performance, tank performance, Worker shift performance, and lifecycle analysis.

### Shipment management: shipping_data_manipulation.sql
Prepares shipping data for analysis, including delivery times, and flagging 
Production Phase
The production phase involves the automation of processes using Python and shell scripts. This ensures the seamless creation of a datamart that can be used for advanced analytics and reporting.

## Automation Scripts
### Cron Job Scheduling: 
- create_query_part1.py
- create_query_part4.py
This Python script creates the grouped SQL script for current date, yesterdays date and the whole month.

### Datamart Creation: 
- query_part_today_1.sh
- query_part_today_4.sh
A shell script that orchestrates the entire process of creating the datamart. It executes the SQL script, loads the transformed data into the datamart, performs any necessary indexing or optimization and creating logs of job transactions.
Scheduler: crontab
1 0 * * * /home/domain/engineer_user/

## How to Use
**Prerequisites** • Ensure you have MySQL installed for the development phase along with the necessary VPN configuration and IP address information. Install Python for the production phase, along with necessary libraries specified in requirements.txt.
**Development** • Execute the SQL scripts in the specified order to manipulate and analyze data in the development phase.
**Production** • Configure the MySQL connection details. Run the query_part_today_1.sh script to automate the datamart creation process. Schedule the create_query_part1.py script for regular updates.
**Conclusion** • This data analytics project for Pertamina Gas Stations aims to provide valuable insights into transactions, stock, equipment, and shipping, enabling informed decision-making. The combination of MySQL for development and Python/shell scripts for production automation ensures a robust and scalable solution for ongoing data analysis. Feel free to explore and adapt the scripts to suit your specific analytics needs!

*Note that this portfolio is a work on progress and you could ask me anytime by contacting:*
- email: davelzhaf@gmail.com
- phone: (+62)8111903055
