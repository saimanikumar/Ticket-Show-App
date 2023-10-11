<template>
  <div class="container container-k mt-4">
    <div class="card booking-card">
      <div class="card-header">
        <h3 class="card-title">Booking - {{ show_info.name }}</h3>
        <div v-if="show_info">
          <p class="card-subtitle mb-2 text-muted">{{ show_info.show_date }}</p>

          <p v-if="show_info.start_time" class="card-subtitle mb-2 text-muted">{{ show_info.start_time }} - {{
            show_info.end_time }}</p>
        </div>
      </div>
      <div class="card-body">
        <div class="row mb-3">

          <div class="col-md-4">
            <h5>Available seats</h5>
            <p class="mb-0">{{ show_info.available_tickets }}</p>
          </div>
          <div class="col-md-4">
            <h5> Number of Tickets</h5>
            <div class="d-flex justify-content-center">
              <input type="number" name="num_tickets" v-model="num_tickets" class="form-control" />
            </div>
          </div>

          <div class="col-md-4">
            <h5>Price</h5>
            <p class="mb-0">&#x20B9;{{ show_info.ticket_price }}</p>
          </div>

        </div>
        <hr />
        <div class="row">
          <div class="col-md-6">
            <h5>Total</h5>
            <p class="mb-0">&#x20B9;{{ price }}</p>
          </div>
          <div class="col-md-6 text-md-end">
            <button @click="postData" type="submit" class="btn btn-info text-white">Confirm Booking</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios.js";

export default {
  data() {
    return {
      show_info: {
        id: null,
        name: '',
        rating: null,
        tags: '',
        ticket_price: 0,
        show_date: null,
        start_time: null,
        end_time: null,
        theatre_id: null,
        available_tickets: null,
      },
      num_tickets: 0,
    }
  },

  components: {

  },

  computed: {
    t_date() { return new Date().toLocaleDateString('en-ca') },
    price() { return this.num_tickets * this.show_info.ticket_price }
  },

  methods: {
    postData() {
      if (this.num_tickets != 0) {
        if (this.$route.params.s_id) {
          var baseUrl = `/api/booking`
        }
        this.show_info.theatre_id = this.$route.params.th_id
        axios({
          method: 'POST',
          url: baseUrl,
          data: {
            show_id: this.show_info.id,
            num_tickets: this.num_tickets
          },
        })
          .then(() => {
            // alert('Tickets Booked')
            this.$router.push({ name: 'bookings' })
          })
          .catch((err) => {
            alert(err.message)
          })
      }
      else {
        alert('Buy atleast 1 ticket')
      }
    },
  },

  async mounted() {

    await axios.get(`/api/show?theatre_id=${this.$route.params.th_id}&show_id=${this.$route.params.s_id}`)
      .then((res) => {
        this.show_info.id = res.data.id
        this.show_info.name = res.data.name
        this.show_info.rating = res.data.rating
        this.show_info.tags = res.data.tags
        this.show_info.show_date = (res.data.show_date).split(' ')[0]
        this.show_info.ticket_price = res.data.ticket_price
        this.show_info.start_time = res.data.start_time.slice(0, -3)
        this.show_info.end_time = res.data.end_time.slice(0, -3)
        this.show_info.theatre_id = res.data.theatre_id
        this.show_info.available_tickets = res.data.available_tickets
        console.log(this.show_info)
        console.log(res.data)
      })
      .catch((err) => {
        this.error = err.message
        console.log(err)
      })

  }

}
</script>



<style scoped>
.container-k {
  padding-top: 120px;
  /* Add extra padding to push the card below the navbar */
  width: 1000px;
  height: auto;
}


.booking-card {
  /* position: relative; */
  /* top: 3%; */
  /* left: 49%; */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  padding-top: 30px;
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 24px;
  /* margin-bottom: 0; */
}

.card-subtitle {
  font-size: 16px;
  margin-bottom: 0;

}

.row {
  align-items: center;
}

h5 {
  font-size: 16px;
  margin-bottom: 8px;
}

p {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 0;
}



.btn-info {
  background-color: #4ea8d9;
  border-color: #64cae4;
  font-size: 18px;
  padding: 10px 20px;
  border-radius: 5px;
}

.btn-info:hover {
  background-color: #30a3e1;
  border-color: #32a1de;
}


.form-control {
  max-width: 150px;
  width: 100%;
  /* padding-left: 70px; */
  text-align: center;
  font-size: 16px;
  margin-bottom: 8px;
}
</style>