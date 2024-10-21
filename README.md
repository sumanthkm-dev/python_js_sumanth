# Sales Management Application

This is a Sales Management application built with Django backend and Vue.js frontend. It provides functionality for managing sales, 
invoices, and visualizing aggregated data for stock, sales, and profits. The application also includes filters for viewing data 
by various attributes like store, city, and zip code,category and vendor number.

### some prerequisites to run the application

To run the application, you need the following installed:

- Python 3.8+
- Django 3.2+
- Node.js 14+
- Vue.js 3
- 
### Backend Setup Django

1. Clone the repository:
2.     git clone https://github.com/your-username/sales_management.git
    

3. Navigate to the backend directory:
    
    cd sales_management/backend


4. Install dependencies:
   
    pip install -r requirements.txt

5. Run the Django server:
    python manage.py runserver
   

### Frontend Setup (Vue.js)

1. Navigate to the frontend directory:
    
    cd ../sales_management_frontend

2. Install dependencies:
    npm install

3. Run the Vue.js development server:
    
    npm run serve


### Start the Application

- Open your browser and navigate to:
    ```
    http://localhost:8080
    ```

## Running the Application

1. Ensure both the Django backend and Vue.js frontend are running as described above.
2. Open the browser and access the dashboard to manage sales, view invoices, and add new invoices.
3. Create/Add excel file export_2019.csv file in the task\sales_management directory to read it when ran comand python manage.py import_data<filename as command> path/to/yourfile.csv
     replace your file name and pathe to you csv file and run the command to create the data.


## Assumptions and Decisions

1. Backend :
    - Created models Store,Product,Sale as its briefly covers all the required data columns as per their ctaegory.
    - The sales and product data are pre-populated in the database for testing purposes from the excel file provided doesnot pushed to git because it is large file 
    - Only authenticated users can add or update invoices.
    - The API responses are aggregated for stock, sales, and profit based on city, county, and zip code filters.
    - created viewsets fro sales, products and stores for simlicity , but again created FBV for zipcodes,cities etc to fetch only those data as viewsets provides unwanted data as well.
    - dashboard endpoint handles the usecases like aggregation level based on city, zipcode and county.
  
3. Frontend :
    - The application uses Vue 3 Options API for better reactivity and scalability.
    - Filters like store, city, and zip code are applied by fetching data dynamically from the backend.
    - Users can add invoices via a modal form.

4. Security:
    - Implemented JWT authentication  to ensure tokn based validation.
    - Logout functionality ensures user sessions are securely terminated.
    - Cross-origin requests (CORS) are handled in the backend using Django middleware.

## Design Patterns

Backend (Django):
- **APIView**: Used for handling filtered sales queries, following the RESTful API design.
- **Aggregation**: Leveraging Django ORM’s `annotate` and `Sum` for aggregating sales, stock, and profit data.
  
Frontend (Vue.js):
- **Component-Based Architecture**: Breaking down the UI into reusable components (e.g., `Dashboard`, `AddInvoice`, `Filters`).
- **Composition API**: Vue 3’s Composition API allows for flexible and reusable code management.
- **Axios for API Calls**: Used to handle data fetching from the backend and dynamically update the dashboard.

Error Handling:
- **Backend**: Custom error pages and responses are returned in case of API failures.
- **Frontend**: A dedicated error page is shown if the API returns any issues while adding or fetching data.

---

## Conclusion

This application demonstrates a robust structure for managing sales and invoices, with a clean separation between frontend and backend components. The design choices were made to ensure scalability and maintainability.
As backend service is completely independent of frontend these RESTFUL API's canbe used by other services as well to read and write data.

