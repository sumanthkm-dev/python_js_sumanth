<template>
  <div class="dashboard-container">
    <div class="header">
      <button @click="logout" class="logout-btn" :class="text - align">
        Logout
      </button>
      <h1>Dashboard</h1>
      <button @click="toggleAddInvoiceModal" class="add-invoice-btn">
        Add Invoice
      </button>
    </div>

    <!-- Add Invoice Modal -->
    <AddInvoice
      v-if="showAddInvoiceModal"
      :showModal="showAddInvoiceModal"
      :stores="stores"
      :products="products"
      @close="toggleAddInvoiceModal"
      @invoiceAdded="handleInvoiceAdded"
      @error="handleError"
    />
    <!-- Aggregation Level Radio Buttons -->
    <div class="aggregation-level">
      <p>Select Aggregation Level</p>
      <label>
        <input
          type="radio"
          value="city"
          v-model="selectedAggregationLevel"
          @change="applyAggregationLevel"
        />
        City
      </label>
      <label>
        <input
          type="radio"
          value="county"
          v-model="selectedAggregationLevel"
          @change="applyAggregationLevel"
        />
        County
      </label>
      <label>
        <input
          type="radio"
          value="zip_code"
          v-model="selectedAggregationLevel"
          @change="applyAggregationLevel"
        />
        Zip Code
      </label>
    </div>

    <div class="filters">
      <div>
        <label for="store">Select Store</label>
        <select v-model="selectedStore">
          <option value="">All Stores</option>
          <option
            v-for="store in stores"
            :key="store.id"
            :value="store.store_name"
          >
            {{ store.store_name }}
          </option>
        </select>
      </div>
      <div>
        <label for="city">Select City</label>
        <select v-model="selectedCity">
          <option value="">All Cities</option>
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </div>
      <div>
        <label for="zip_code">Select Zip Code</label>
        <select v-model="selectedZipCode">
          <option value="">All Zip Codes</option>
          <option v-for="zip in zipCodes" :key="zip" :value="zip">
            {{ zip }}
          </option>
        </select>
      </div>
      <div>
        <label for="category">Select Category</label>
        <select v-model="selectedCategory">
          <option value="">All Categories</option>
          <option
            v-for="category in categories"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>
      <div>
        <label for="vendor_number">Select Vendor Number</label>
        <select v-model="selectedVendorNumber">
          <option value="">All Vendors</option>
          <option v-for="vendor in vendorNumbers" :key="vendor" :value="vendor">
            {{ vendor }}
          </option>
        </select>
      </div>
      <button @click="fetchData">Filter</button>
    </div>

    <!-- Display results -->
    <div v-if="aggregatedData.length" class="dashboard-results">
      <!-- Aggregated Data Table -->
      <div class="data-section">
        <h2 v-if="selectedAggregationLevel === 'city'">
          City Level Aggregated Data
        </h2>
        <h2 v-if="selectedAggregationLevel === 'county'">
          County Level Aggregated Data
        </h2>
        <h2 v-if="selectedAggregationLevel === 'zip_code'">
          Zip Code Level Aggregated Data
        </h2>

        <table>
          <thead>
            <tr>
              <th v-if="selectedAggregationLevel === 'city'">City</th>
              <th v-if="selectedAggregationLevel === 'county'">County</th>
              <th v-if="selectedAggregationLevel === 'zip_code'">Zip Code</th>
              <th>Total Stock</th>
              <th>Total Sales ($)</th>
              <th>Total Profit ($)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="data in aggregatedData" :key="data.id">
              <td v-if="selectedAggregationLevel === 'city'">
                {{ data.store__city }}
              </td>
              <td v-if="selectedAggregationLevel === 'county'">
                {{ data.store__county }}
              </td>
              <td v-if="selectedAggregationLevel === 'zip_code'">
                {{ data.store__zip_code }}
              </td>
              <td>{{ data.total_stock }}</td>
              <td>{{ data.total_sales.toFixed(2) }}</td>
              <td>{{ data.total_profit.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else>No data available</div>
  </div>
</template>

<script>
import axios from "axios";
import AddInvoice from "../components/AddInvoice.vue";

export default {
  components: {
    AddInvoice,
  },
  data() {
    return {
      showAddInvoiceModal: false,
      stores: [],
      cities: [],
      zipCodes: [],
      categories: [],
      vendorNumbers: [],
      selectedStore: "",
      selectedCity: "",
      selectedZipCode: "",
      selectedCategory: "",
      selectedVendorNumber: "",
      dashboardData: [],
      products: [],
      newInvoice: {
        store_id: "",
        product_id: "",
        bottles_sold: 0,
        sale_dollars: 0,
      },
      selectedAggregationLevel: "city", // Default to city
      aggregatedData: [],
    };
  },
  created() {
    this.fetchInitialData();
    this.applyAggregationLevel(); // Fetch initial data for the dashboard
  },
  methods: {
    toggleAddInvoiceModal() {
      this.showAddInvoiceModal = !this.showAddInvoiceModal;
    },
    // Fetch initial dropdown data from the backend
    async fetchInitialData() {
      try {
        const [
          storesRes,
          productsRes,
          citiesRes,
          zipCodesRes,
          categoriesRes,
          vendorsRes,
        ] = await Promise.all([
          axios.get("http://localhost:8000/api/v1/stores/"),
          axios.get("http://localhost:8000/api/v1/products/"),
          axios.get("http://localhost:8000/api/v1/cities/"),
          axios.get("http://localhost:8000/api/v1/zipcodes/"),
          axios.get("http://localhost:8000/api/v1/categories/"),
          axios.get("http://localhost:8000/api/v1/vendor_numbers/"),
        ]);

        this.stores = storesRes.data;
        this.products = productsRes.data;
        this.cities = citiesRes.data;
        this.zipCodes = zipCodesRes.data;
        this.categories = categoriesRes.data;
        this.vendorNumbers = vendorsRes.data;
      } catch (error) {
        console.error("Error fetching initial data:", error);
      }
    },
    // Fetch dashboard data based on filters
    async fetchDashboardData() {
      try {
        const params = {
          store_name: this.selectedStore,
          city: this.selectedCity,
          zip_code: this.selectedZipCode,
          category: this.selectedCategory,
          vendor_number: this.selectedVendorNumber,
          cityLevel: this.selectedAggregationLevel === "city",
          countyLevel: this.selectedAggregationLevel === "county",
          zip_codeLevel: this.selectedAggregationLevel === "zip_code",
        };

        const response = await axios.get(
          "http://localhost:8000/api/v1/dashboard/",
          {
            params,
          }
        );
        // Update the table data
        if (this.selectedAggregationLevel === "city") {
          this.aggregatedData = response.data.city_data;
        } else if (this.selectedAggregationLevel === "county") {
          this.aggregatedData = response.data.county_data;
        } else if (this.selectedAggregationLevel === "zip_code") {
          this.aggregatedData = response.data.zip_code_data;
        }
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },
    fetchData() {
      this.fetchDashboardData(); // Trigger data fetch when filter button is clicked
    },
    async applyAggregationLevel() {
      try {
        // Create params for the selected aggregation level
        let params = {};
        if (this.selectedAggregationLevel === "city") {
          params = { cityLevel: true }; // Signal backend to return city-level data
        } else if (this.selectedAggregationLevel === "county") {
          params = { countyLevel: true }; // Signal backend to return county-level data
        } else if (this.selectedAggregationLevel === "zip_code") {
          params = { zip_codeLevel: true }; // Signal backend to return zip-code-level data
        }

        // Fetch the data for the selected aggregation level
        const response = await axios.get(
          "http://localhost:8000/api/v1/dashboard/",
          {
            params,
          }
        );

        // Update the table data
        if (this.selectedAggregationLevel === "city") {
          this.aggregatedData = response.data.city_data;
        } else if (this.selectedAggregationLevel === "county") {
          this.aggregatedData = response.data.county_data;
        } else if (this.selectedAggregationLevel === "zip_code") {
          this.aggregatedData = response.data.zip_code_data;
        }
      } catch (error) {
        console.error("Error fetching aggregated data:", error);
      }
    },
    handleInvoiceAdded() {
      this.fetchDashboardData(); // Update dashboard after invoice is added
    },
    handleError() {
      this.$router.push({ name: "ErrorPageView" });
    },
    async logout() {
      try {
        await axios.post("http://localhost:8000/api/v1/logout/");
        this.$router.push({ path: "/login" });
      } catch (error) {
        console.error("Error logging out:", error);
        this.$router.push({ name: "ErrorPageView" });
      }
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
  margin-bottom: 35px;
}
.dashboard-container {
  padding: 20px;
}
.aggregation-level {
  margin-bottom: 50px;
}
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}
.filters div {
  flex: 1;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
table th,
table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
}
button {
  margin-top: 25px;
  padding: 10px 15px;
  cursor: pointer;
}
.logout-btn {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.add-invoice-btn {
  background-color: #28a745;
  color: white;
  padding: 10px 10px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  align-items: right;
  text-align: center;
}

.logout-btn:hover,
.add-invoice-btn:hover {
  opacity: 0.9;
}
</style>
