# P6. BI Insights and Storytelling
This separte README was established specifically to focus on the culminating analysis project with the smart_store dataset. Instructions for project set up and ETL can be found at https://github.com/matthewpblock/smart-store-block/blob/main/README.md

## Section 1. The Business Goal
Operational Objective: Build a targeted marketing that increases profits.  
Analytical Objective: Identify segments of the customer list can can be targeted in specific ways to increase profits. Provide recommendations for segmented messaging and a tracking mechanism to assess effectiveness.  
Initial options for targeting segmentation:
- By region
- By store
- Personalized down to the individual customer  
Emphasis: Analysis should focus on profit, not gross revenue.

## Section 2. Data Source
Data is sourced from the data warehouse created for earlier assignments in this same repository.  
#TODO        Clearly indicate which columns of which tables were used.

## Section 3. Tools
Analysis is being done within PowerBI to increase skill with this tool, both for personal proficiency and to gain knowledge to share with others.

## Section 4. Workflow & Logic
#TODO Describe the dimensions and aggregations - the logic needed for your analysis
### Profit Margin
To meet the objective of focusing on profits over gross revenue, a new calculated data point was required. Column `profit_margin` was created in the `products` table by subtracting `wholesale_price` from `unit_price`.  
![Adding new profit_margin column](p_6images/profit_margin.png)
### Profit per Transaction
Because the `sales` table records contain varying quantities of items sold, a new calculated data point for `quantity` was also required. This was created by dividing the `sale_amount` from the `sales` table by the `unit_price` from the `products` table for the corresponding `product_id` using the formula:  
```Quantity = 
DIVIDE(
    sales[sale_amount], 
    LOOKUPVALUE(
        products[unit_price], 
        products[product_id], 
        sales[product_id]
    ), 
    0 )```
![Adding new profit_per_transaction column](p_6images/profit_per_transaction.png)

If using a graphical tool like Power BI or Tableau Prep, use screenshots to show your work. 

## Section 5. Results
Present your insights with narrative and visualizations.
Explain any suggested actions based on the results you uncovered.

## Section 6: Suggested Business Action 
        What actions are recommended based on your work

## Section 7. Challenges
        Mention any challenges you encountered and how they were resolved.
