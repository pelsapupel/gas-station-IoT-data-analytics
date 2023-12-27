## Stock Performance Evaluation

I create datamart for an analysis in stock performance

The objective of the creation of datamart are:
1. Find the Status of the tank observed
2. Find the time needed for the petrol in the tank to lasts
3. Displays it as a comprehensive information about the product

To achieve those objectives, I need these data:
1. Data of Gas/Petrol Tank
2. Data of Transaction
3. Data of Shipment

The data explorations
1. To find the status of the tank we must know the last volume of the tank from the datalake and show it as the "last stock readings"
2. To find the status of the tank we must also know the different sensor statuses from the IoT expert on the field
3. To calculate the time needed for the petrol in the tank to lasts we must find the stock and the sales velocity
4. To find sales velocity we encountered problems that i will talk about in the next section but overall we can calculate it by total sales/selling time.
5. We found that
6. etc  

I encountered multiple challenges and limitations from the data:
1. Every tank is not regularly online yet we want to analyze the performance of the stock that is needed by the station
2. Every oil dispenser is not regularly online yet we want to analyze the amount of volume throughput of the procucts.
3. We cannot acquire the selling time of each station as each station could change their opening and closing time regularly because some stations are privately-owned.
4. etc


