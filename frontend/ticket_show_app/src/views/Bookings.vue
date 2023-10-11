<template>
    container
    <div>
        <br />
        <h6 class="card-text user-name mar-fix" style="display: inline-block; font-size: x-large; padding-left: 0px;"></h6>

        <div v-if="bookings" class="container mt-5">
            <div class="row">
                <div v-for="(booking, index) in bookings" :key="booking.id" class="col-lg-3 col-md-4 col-sm-6">
                    <div class="card">
                        <div class="card-header">
                            {{ booking.theatre ? booking.theatre.name : notAvailableMsg }}
                        </div>
                        <div class="card-body">
                            <div class="booking-info">
                                <h5 class="mb-2"> {{ booking.show ? booking.show.name : notAvailableMsg }}</h5>
                                <p class="fs-14"><b>Tickets - </b> {{ booking.num_tickets }}</p>
                                <p class="fs-14"><b>Total Price</b> ₹{{ booking.cost }}</p>
                                <p class="fs-14"><b>Show Date</b> {{ booking.show ? formatDate(booking.show.show_date) :
                                    notAvailableMsg }}</p>
                                <p class="fs-14">Booked on {{ booking ? formatDate(booking.booking_date) :
                                    notAvailableMsg }}</p>
                                <!-- <p class="fs-14"><b>Show Timings:</b> {{ booking.show.start_time }} - {{ booking.show.end_time
                    }}</p> -->
                                <!-- <p v-if="booking.show.tags" class="fs-14"><b>Tags:</b> {{ booking.show.tags }}</p> -->
                                <!-- Add any other additional information you want to display here -->
                            </div>
                        </div>
                        <div class="card-footer d-flex justify-content-center">
                            <div v-if="booking.user_rating == 0">
                                <div style="padding-bottom: 5px;">Your Rating</div>

                                <button @click="rateNow(booking.show.id, booking.id)" type="button" class="btn c2 btn-sm">
                                    Rate Show
                                </button>
                            </div>
                            <div v-else>
                                Your Rating
                                <StarRating :rating="booking.user_rating" :disabled="true" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="bookings == null" class="text-center">
            <br /><br />
            <h4 class="card-text"> Loading... </h4>
        </div>

        <div v-if="bookings && bookings.length === 0" class="text-center">
            <br /><br />
            <h4 class="card-text"> No Bookings Available</h4>
        </div>


        <div v-if="showModal" class="modal-mask">
            <div class="modal-container">
                <div class="modal-header">
                    <h3>Rate Show</h3>
                    <button class="close-btn" @click="showModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <StarRating :rating="rating" @change="updateRating" />
                </div>
                <div class="modal-footer">
                    <button @click="submitRating" class="btn btn-primary">Submit</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from "../axios.js";
import StarRating from "../components/StarRating.vue";

export default {
    data() {
        return {
            bookings: null,
            notAvailableMsg: "N/A",
            showModal: false,
            rating: 0,
            showId: null,
            bookingId: null,
        };
    },

    components: {
        StarRating,
    },

    computed: {
    },

    methods: {
        async fetchTheatreName(theatreId) {
            try {
                const response = await axios.get(`/api/theatre?id=${theatreId}`);
                return response?.data?.name || this.notAvailableMsg;
            } catch (error) {
                console.error("Error fetching theatre:", error);
                return this.notAvailableMsg;
            }
        },

        async fetchShowName(showId) {
            try {
                const response = await axios.get(`/api/show?show_id=${showId}`);
                var name = response?.data?.name || this.notAvailableMsg;
                var theatre_id = response?.data?.theatre_id || this.notAvailableMsg;
                var tags = response?.data?.tags || this.notAvailableMsg;
                var show_date = response?.data?.show_date || this.notAvailableMsg;
                var start_time = response?.data?.start_time || this.notAvailableMsg;
                var end_time = response?.data?.end_time || this.notAvailableMsg;

                return {
                    name: name,
                    theatre_id: theatre_id,
                    tags: tags,
                    show_date: show_date,
                    start_time: start_time,
                    end_time: end_time,
                };

            } catch (error) {
                console.error("Error fetching show:", error);
                return this.notAvailableMsg;
            }
        },

        async loadBookings() {
            try {
                const response = await axios.get(`/api/booking`);
                this.bookings = response.data;
                // console.log(this.bookings);
                for (const booking of this.bookings) {
                    // console.log(booking.user_rating)
                    var show_details = await this.fetchShowName(booking.show_id);
                    booking.show = {
                        id: booking.show_id,
                        name: show_details.name,
                        tags: show_details.tags,
                        show_date: show_details.show_date,
                        start_time: show_details.start_time.slice(0, -3),
                        end_time: show_details.end_time.slice(0, -3),
                    };
                    booking.theatre = {
                        id: booking.theatre_id,
                        name: await this.fetchTheatreName(show_details.theatre_id),
                    };
                }
            } catch (error) {
                console.error("Error fetching bookings:", error);
            }
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString("en-IN");
        },


        updateRating(value) {
            this.rating = value;
        },

        rateNow(show_id, booking_id) {

            this.showModal = true;
            this.rating = 0;
            this.showId = show_id;
            this.bookingId = booking_id;
        },

        async submitRating() {
            try {

                // console.log("Submitting rating:", this.rating);
                // console.log(this.bookingId)

                axios({
                    method: 'POST',
                    url: '/api/user/rating',
                    data: {
                        show_id: this.showId,
                        booking_id: this.bookingId,
                        user_rating: this.rating,
                    },
                });

                this.showModal = false;
                this.rating = 0;
                this.$router.push({ name: 'user_board' });

            } catch (error) {
                console.error("Error submitting rating:", error);
            }
        },
    },

    async mounted() {
        await this.loadBookings();
    },
};
</script>

<style scoped>
.c2 {
    background-color: #8bcff4;
}

.c2:hover {
    background-color: #2faaec;
}

.c2:active {
    background-color: #2faaec;
}



.card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    min-height: 350px;
    max-height: 300px;
    max-width: 600px;
    margin: 15px;
}

.card-header {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-size: 18px;
    padding: 15px;
    overflow: hidden;
}

.card-body {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.booking-info {
    padding: 5px;
}

.booking-info h5 {
    font-size: 22px;
    margin-bottom: 10px;
}

.booking-info p {
    font-size: 16px;
    margin: 5px 0;
}

.card-footer {
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 10px;
    background-color: #f7f7f7;
    display: flex;
    justify-content: flex-end;
}

.modal-mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.modal-container {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
}

.close-btn {
    border: none;
    background-color: transparent;
    cursor: pointer;
    font-size: 24px;
}

.modal-body {
    padding: 20px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
}
</style>
