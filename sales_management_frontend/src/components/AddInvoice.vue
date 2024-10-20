<template>
  <div class="modal" v-if="showModal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>Add New Invoice</h2>
      <form @submit.prevent="submitInvoice">
        <div class="dropdown">
          <label for="invoice_number">Invoice Number</label>
          <input
            type="number"
            v-model="newInvoice.invoice_number"
            required
            placeholder="Enter number ofInvoice Number"
          />
        </div>

        <div class="dropdown">
          <label for="date">Select Date</label>
          <input type="date" v-model="newInvoice.date" required />
        </div>
        <div class="dropdown">
          <label for="store">Select Store</label>
          <select v-model="newInvoice.store" required>
            <option value="">Select Store</option>
            <option v-for="store in stores" :key="store.id" :value="store.id">
              {{ store.store_name }}
            </option>
          </select>
        </div>

        <div class="dropdown">
          <label for="product">Select Product</label>
          <select v-model="newInvoice.product" required>
            <option value="">Select Product</option>
            <option
              v-for="product in products"
              :key="product.id"
              :value="product.id"
            >
              {{ product.item_desc }}
            </option>
          </select>
        </div>

        <div class="dropdown">
          <label for="bottles_sold">Bottles Sold</label>
          <input
            type="number"
            v-model="newInvoice.bottles_sold"
            required
            placeholder="Enter number of bottles sold"
          />
        </div>

        <div class="dropdown">
          <label for="sale_dollars">Sale Amount</label>
          <input
            type="number"
            v-model="newInvoice.sale_dollars"
            required
            placeholder="Enter sale amount"
          />
        </div>

        <div class="dropdown">
          <label for="volume_sold_gallons">Volume Sold in Gallons</label>
          <input
            type="number"
            v-model="newInvoice.volume_sold_gallons"
            required
            placeholder="Enter Volume Sold"
          />
        </div>

        <div class="dropdown">
          <label for="volume_sold_liters">Volume Sold in Liters</label>
          <input
            type="number"
            v-model="newInvoice.volume_sold_liters"
            required
            placeholder="Enter Volume Sold"
          />
        </div>

        <button type="submit">Add Invoice</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    showModal: Boolean, // Modal visibility controlled by parent
    stores: Array, // Stores data passed from parent
    products: Array, // Products data passed from parent
  },
  data() {
    return {
      newInvoice: {
        invoice_number: 0,
        date: "",
        store: "",
        product: "",
        bottles_sold: 0,
        sale_dollars: 0,
        volume_sold_gallons: 0,
        volume_sold_liters: 0,
      },
    };
  },
  methods: {
    closeModal() {
      this.$emit("close"); // Emit event to parent to close modal
    },
    async submitInvoice() {
      try {
        await axios.post(
          "http://localhost:8000/api/v1/sales/",
          this.newInvoice
        );
        alert("Invoice added successfully!");
        this.newInvoice = {
          store: "",
          product: "",
          bottles_sold: 0,
          sale_dollars: 0,
        };
        this.$emit("invoiceAdded"); // Emit event to notify parent
        this.closeModal(); // Close modal after successful submission
      } catch (error) {
        console.error("Error adding invoice:", error);
        this.$emit("error");
      }
    },
  },
};
</script>

<style scoped>
/* Modal styles */
.modal {
  display: flex;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
}
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 50%;
}
.close {
  color: red;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.dropdown {
  text-align: center;
  margin-bottom: 35px;
  align-items: center;
}
</style>
