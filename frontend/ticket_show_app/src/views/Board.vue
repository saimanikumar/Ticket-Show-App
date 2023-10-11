<template>
    <div>
        <br />
        <h6 class="card-text user-name mar-fix" style="display: inline-block; font-size: x-large; padding-left: 0px;"></h6>

        <!-- Search bar -->
        <div class="search-container">
            <input type="text" v-model="searchQuery" @input="searchTheatres"
                placeholder="Search by location, venue, theatre name, show name" />
            <span class="search-icon">&#128269;</span>
        </div>

        <div class="dropdown date-filter-dropdown">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dateFilterDropdown"
                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Filter by Date
            </button>
            <div class="dropdown-menu" aria-labelledby="dateFilterDropdown">
                <!-- ... (other dropdown items) ... -->
                <div class="date-filter">
                    <input type="date" v-model="selectedDate" @input="searchTheatres" class="form-control" :min="t_date" />
                </div>
            </div>
        </div>

        <button class="btn btn-sm c2" style="margin: 5px;" @click="clearFilter">Clear</button>

        <!-- Display theatres and shows based on the search results -->
        <div v-if="filteredTheatres" class="container mt-5">
            <div v-for="theatre in filteredTheatres" class="card main-card" :key="theatre.id">
                <div class="c1 card-card2">
                    <div class="card-header">
                        <span><i class="bi bi-building"></i> {{ theatre.name }}</span>
                        <p class="venue"> <b>Venue </b> - {{ theatre.place }}</p>
                        <span class="location"><i class="bi bi-geo-alt"></i> {{ theatre.location }}</span>
                    </div>
                    <div class="card-body m1">
                        <div class="outer-card-container">
                            <div class="card-container">
                                <div v-if="theatre.shows.length !== 0">
                                    <div v-for="show in theatre.shows" class="scrollable-card" :key="show.id">
                                        <div class="scroll-content">
                                            <div class="card card-list-board">
                                                <div class="card-header">
                                                    <span><i class="bi bi-film"></i> {{ show.name }}</span>
                                                </div>
                                                <div class="card-body">
                                                    <div class="show-details">

                                                        <p><i class="bi bi-star"></i> Rating {{ show.rating }}</p>
                                                    </div>
                                                    <p class="show-date"><i class="bi bi-calendar"></i> {{
                                                        formatDate(show.show_date) }}</p>
                                                    <p class="show-timings"><i class="bi bi-clock"></i> {{
                                                        show.start_time.slice(0, -3) }} - {{ show.end_time.slice(0, -3) }}
                                                    </p>
                                                    <p class="show-timings">{{ show.tags }}</p>


                                                    <div v-if="show.available_tickets > 0">
                                                        <button @click="book(show.theatre_id, show.id)" type="button"
                                                            class="btn c2">Book</button>
                                                    </div>
                                                    <div v-else>
                                                        <button type="button" class="btn c2" disabled>
                                                            <b>Houseful</b></button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div v-else>
                                    <p>No Shows Yet!</p>
                                </div>

                                <!-- Download Button -->
                                <button @click="downloadCSV(theatre.id)" type="button" class="btn btn-secondary">
                                    <i class="bi bi-file-earmark-arrow-down"></i> Export as CSV
                                </button>


                                <div v-if="downloadStatus[theatre.id] === 'pending'" class="alert alert-info mt-2 d-status"
                                    role="alert">
                                    Sending email...
                                </div>

                                <div v-else-if="downloadStatus[theatre.id] === 'success'"
                                    class="alert alert-success mt-2 d-status" role="alert">
                                    CSV sent to email Successfully!
                                </div>

                                <div v-else-if="downloadStatus[theatre.id] === 'failed'"
                                    class="alert alert-danger mt-2 d-status" role="alert">
                                    Failed to send CSV to email.
                                </div>


                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="filteredTheatres === null">
            <br /><br />
            <h4 class="card-text">Loading...</h4>
            <ul class="nav-item"></ul>
        </div>
        <div v-if="filteredTheatres && filteredTheatres.length === 0">
            <br /><br />
            <h4 class="card-text">No Shows Available</h4>
            <ul class="nav-item"></ul>
        </div>
    </div>
</template>
  
<script>
import axios from "../axios.js";

export default {
    data() {
        return {
            theatres: null,
            searchQuery: "",
            downloadStatus: {},
            selectedDate: null,
        };
    },


    computed: {
        t_date() { return new Date().toLocaleDateString('en-ca') },
        // Computed property to filter theaters based on the search query and selected date
        filteredTheatres() {
            if (!this.theatres) return null; // Handle initial loading

            let filteredTheatres = this.theatres;

            // Apply search filter
            if (this.searchQuery.trim()) {
                const search = this.searchQuery.trim().toLowerCase();
                filteredTheatres = filteredTheatres.filter((theatre) => {
                    const locationMatch = theatre.location.toLowerCase().startsWith(search);
                    const nameMatch = theatre.name.toLowerCase().startsWith(search);
                    const placeMatch = theatre.place.toLowerCase().startsWith(search);
                    const showMatch = theatre.shows.some((show) => show.name.toLowerCase().startsWith(search));
                    return locationMatch || nameMatch || showMatch || placeMatch;
                });
            }

            // Apply date filter
            if (this.selectedDate) {
                const selectedDate = new Date(this.selectedDate).setHours(0, 0, 0, 0);
                filteredTheatres = filteredTheatres.map((theatre) => {
                    const filteredShows = theatre.shows.filter((show) => {
                        const showDate = new Date(show.show_date).setHours(0, 0, 0, 0);
                        return showDate === selectedDate;
                    });
                    return { ...theatre, shows: filteredShows };
                });
            }


            return filteredTheatres;
        },
    },

    components: {},

    methods: {
        clearFilter() {
            this.searchQuery = ""; // Clear the search query
            this.selectedDate = null; // Clear the date filter
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString("en-IN");
        },
        book(theatre_id, show_id) {
            this.$router.push({ name: "user_booking", params: { th_id: theatre_id, s_id: show_id } });
        },


        async init_board() {
            this.theatres = null;
            const currentDate = new Date();
            const currentTime = currentDate.getTime();

            try {
                const response = await axios.get("/api/theatre");
                const theatresData = response.data;

                for (let i in theatresData) {
                    const theatreId = theatresData[i].id;
                    const showResponse = await axios.get(`/api/show?theatre_id=${theatreId}`);
                    const showsData = showResponse.data;

                    // Filter shows for the current date and time
                    const filteredShows = showsData.filter((show) => {
                        const showDate = new Date(show.show_date); // Ensure showDate is a Date object
                        showDate.setHours(0, 0, 0, 0); // Set the time to 00:00:00 to ignore time for comparison
                        const showStartTime = new Date(`1970-01-01T${show.start_time}`).getTime();

                        return (
                            showDate.getTime() >= currentDate.setHours(0, 0, 0, 0) && showStartTime <= currentTime
                        );
                    });

                    theatresData[i].shows = filteredShows;
                }

                this.theatres = theatresData;
            } catch (error) {
                console.error(error);
            }
        },

        async fetchShowsForSelectedDate() {
            if (!this.selectedDate) return;
            const selectedDate = new Date(this.selectedDate);
            const selectedTime = selectedDate.getTime();

            try {
                for (let i in this.theatres) {
                    const theatreId = this.theatres[i].id;
                    const showResponse = await axios.get(`/api/show?theatre_id=${theatreId}`);
                    const showsData = showResponse.data;

                    // Filter shows for the selected date
                    const filteredShows = showsData.filter((show) => {
                        const showDate = new Date(show.show_date);
                        showDate.setHours(0, 0, 0, 0);
                        const showStartTime = new Date(`1970-01-01T${show.start_time}`).getTime();

                        return showDate.getTime() === selectedTime && showStartTime <= Date.now();
                    });

                    this.theatres[i].shows = filteredShows;
                }
            } catch (error) {
                console.error(error);
            }
        },


        searchTheatres() {

        },


        async fetchEmailStatus(taskId) {
            try {
                const response = await axios.get(`/api/email_status?task_id=${taskId}`);
                return response.data;
            } catch (error) {
                console.error(error);
                return null;
            }
        },

        async downloadCSV(theatreId) {
            try {
                const response = await axios.post("/api/send_csv_to_email", { theatre_id: theatreId });
                const taskId = response.data.task_id;

                this.downloadStatus[theatreId] = 'pending';

                // Fetch the email status 
                const intervalId = setInterval(async () => {
                    const statusResponse = await this.fetchEmailStatus(taskId);
                    if (statusResponse) {
                        this.downloadStatus[theatreId] = statusResponse.status;
                        if (statusResponse.status === 'success') {
                            clearInterval(intervalId);
                        }
                    }
                }, 1000);
            } catch (error) {
                console.error(error);
                this.downloadStatus[theatreId] = 'failed';
            }


        },


    },

    mounted() {
        this.init_board();
    },

};
</script>
  
<style scoped>
.date-filter-dropdown {
    display: inline-block;
    margin-left: 10px;
}

.date-filter-dropdown .dropdown-toggle {
    font-size: 14px;
}

.date-filter-dropdown .dropdown-menu {
    padding: 10px;
}

.date-filter input[type="date"] {
    width: 100%;
    padding: 6px 12px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 14px;
}

.btn-outline-secondary {
    font-size: 14px;
    margin-left: 10px;
}

.search-container {
    position: relative;
    max-width: 500px;
    margin: 0 auto;
}

.search-container input[type="text"] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

.search-icon {
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    font-size: 20px;
    cursor: pointer;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.location {
    font-size: 14px;
    color: #666;
    margin-left: 10px;
}

.venue,
.show-date,
.show-timings {
    font-size: 14px;
    color: #333;
    margin-top: 8px;
}

.main-card {
    position: relative;
    margin: 20px;
}

.card-container {
    overflow-x: hidden;
    white-space: nowrap;
}

.scrollable-card {
    display: inline-block;
    width: 200px;
    margin-right: 10px;
    padding: 10px;
}

.card-list-board {
    background-color: hwb(0 100% 0%);
    min-width: 200px;
    max-width: 800px;
}

.card-list-board:hover {
    /* Add hover styles as needed */
    transition: 0.3s transform cubic-bezier(0.155, 1.105, 0.295, 1.12),
        0.3s box-shadow,
        0.3s -webkit-transform cubic-bezier(0.155, 1.105, 0.295, 1.12);
    transform: scale(1.075);
    box-shadow: 35px 20px 30px rgba(130, 130, 130, 0.5);
    z-index: 10;
}

.card-card2 {
    min-height: 200px;
    max-height: 600px;
}


.d-status {
    width: 280px;
    padding: 7px;
    margin: 0 auto;
}

.c2 {
    background-color: #8bcff4;
}

.c2:hover {
    background-color: #2faaec;
}

.c2:active {
    background-color: #2faaec;
}

.main-card {
    position: relative;
}

.main-card:hover .card-container {
    overflow-x: auto;
}

.main-card:hover .card-container::-webkit-scrollbar {
    height: 12px;
}

.main-card:hover .card-container::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
}

.main-card:hover .card-container::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.1);
}
</style>