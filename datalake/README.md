## Raw Data Metadata
### Overview
This file contains raw data metadata for the Pertamina Gas Station Data Analytics Project. The data given above is transactions, stock levels, equipment details, and shipping records, providing a comprehensive view of Pertamina gas station operations. The data is updated at a frequency of every 5 minutes and is stored in the datalake.

### Data
1. Transaction Data

File Name: Datalake Transaksi.csv

Columns: Timestamp, TransactionID, SiteID, ProductID, PumpID, Quantity, Volume, PaymentMethod, VehicleNumber, etc.

Description: Captures real-time information about each transaction

2. Stock Data

File Name: Datalake Pembacaan Tanki.csv

Columns: Timestamp, TankID, ProbeStatus, TankTypeID, GaugeVolume, TheoriticalVolume, etc. 

Description: Represents the current stock levels for each product at Pertamina gas stations, along with the important details of the tank.

3. Equipment Data

File Name: equipment_details.csv

Columns: EquipmentID, EquipmentType, MaintenanceSchedule, LastMaintenanceDate

Description: Contains information about equipment, including type, maintenance schedule, and the date of the last maintenance activity.

4. Shipping Data

File Name: shipping_records.csv

Columns: ShipmentID, ProductID, Destination, ShipmentDate, DeliveryStatus

Description: Tracks shipping details, including shipment ID, product ID, destination, shipment date, and delivery status.

### Update Frequency
The raw data is updated every 5 minutes to ensure the latest information is available for analysis. This frequent update cadence enables timely decision-making and enhances the accuracy of insights derived from the data.

### Usage
The raw data stored in the datalake serves as the foundation for creating analyses and datamarts. These structured datasets are later utilized for visualization, providing stakeholders with a comprehensive understanding of Pertamina gas station operations in real-time. Explore, analyze, and visualize the data to extract valuable insights for informed decision-making.
