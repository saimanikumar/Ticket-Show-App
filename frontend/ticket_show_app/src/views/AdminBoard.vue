<template>
    <div>
        <error-popup :error-message="errorPopupMessage" @close="closeErrorPopup"></error-popup>


        <h6 class="card-text user-name mar-fix" style="display: inline-block; font-size: x-large; padding-left: 0px;">
            <span v-for="i in 178">&nbsp;</span>
        </h6>


        <div class="search-container">
            <input type="text" v-model="searchQuery" @input="searchTheatres"
                placeholder="Search by location, venue, theater name, show name" />
            <span class="search-icon">&#128269;</span>
        </div>


        <a @click="createTheatre" class="nav-link btn btn-outline-light c2" role="button"
            style="display: inline-block; padding: 10px; font-size: medium;">
            <i class="bi bi-plus"></i>Add Theatre
        </a>

        <div>
            <div v-if="theatres" class="row">
                <div v-for="theatre in filteredTheatres" :key="theatre.id" class="list-column col-lg-3 col-md-4">
                    <div class="card card-list">

                        <div class="card-header">

                            <div class="dropdown">
                                <button type="button" class="btn btn-light dropdown-toggle" data-bs-toggle="dropdown">
                                    <i class="bi bi-geo-alt"></i> {{ theatre.name }}
                                </button>
                                <ul class="dropdown-menu button-color">

                                    <li>
                                        <a @click="updateTheatre(theatre.id)"
                                            class="dropdown-item btn btn-primary button-color">
                                            <i class="bi bi-pencil"></i> Update
                                        </a>
                                    </li>

                                    <li>
                                        <a @click="deleteTheatre(theatre.id)"
                                            class="dropdown-item btn btn-outline-danger button-color">
                                            <i class="bi bi-trash"></i> Delete
                                        </a>
                                    </li>

                                </ul>
                            </div>

                        </div>

                        <div class="card-body card-body-color overflow-auto card-list-body">

                            <a @click="createShow(theatre.id)" class="nav-link btn btn-outline-light c2" role="button"
                                style="display: inline-block; padding: 5px;">
                                <i class="bi bi-plus"></i>Add Show
                            </a>
                            <div> Location - {{ theatre.location }}</div>
                            <div> Venue - {{ theatre.place }}</div>

                            <div class="card-text">
                                <Show v-for="show in theatre.shows" :key="show.id" :show="show" @update-card="updateShow"
                                    @delete-card="deleteShow" />
                                <!-- @delete-card="deleteShow" -->
                            </div>
                            <div v-show="theatre.shows.length == 0">
                                <br>
                                <h6 class="card-text"> No Shows! Add a New Show</h6>
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
    </div>
</template>
  
<script>
import axios from "../axios.js";
import Show from "../components/Show.vue";
import ErrorPopup from '../components/ErrorPopUp.vue';


export default {
    data() {
        return {
            theatres: null,
            searchQuery: "",
            errorPopupMessage: ''

        };
    },

    computed: {
        filteredTheatres() {
            if (!this.theatres) return null; 
            if (!this.searchQuery.trim()) return this.theatres; 

            const search = this.searchQuery.trim().toLowerCase();
            return this.theatres.filter((theatre) => {
                const locationMatch = theatre.location.toLowerCase().startsWith(search);
                const nameMatch = theatre.name.toLowerCase().startsWith(search);
                const placeMatch = theatre.place.toLowerCase().startsWith(search);
                const showMatch = theatre.shows.some((show) => show.name.toLowerCase().startsWith(search));
                return locationMatch || nameMatch || showMatch || placeMatch;
            });
        },
    },

    components: {
        Show,
        'error-popup': ErrorPopup,
    },

    methods: {
       
        searchTheatres() {

        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString("en-IN");
        },
        createTheatre() {
            this.$router.push({ name: "create_theatre" });
        },

        updateTheatre(theatre_id) {
            this.$router.push({ name: "update_theatre", params: { id: theatre_id } });
        },

        deleteTheatre(theatre_id) {
            const sure = confirm("Are you sure?");

            if (!sure) {
                return;
            }

            axios.get(`/api/show?theatre_id=${theatre_id}`)
                .then((res) => {
                    const shows = res.data;

                    
                    const deleteShowPromises = shows.map((show) => {
                        return axios.delete(`/api/show?show_id=${show.id}`);
                    });

                    
                    return Promise.all(deleteShowPromises);
                })
                .then(() => {
                    
                    return axios.delete(`/api/theatre?id=${theatre_id}`);
                })
                .then(() => {
                    alert("Successfully Deleted");
                    this.init_board();
                    this.$router.push({ name: "admin_board" });
                })
                .catch((err) => {
                    console.error("Error deleting theatre:", err);
                    const errorMessage = err.response?.data?.error_message || "Error while deleting Theatre";
                    this.showErrorPopup(errorMessage);
                });
        },



        createShow(theatre_id) {
            this.$router.push({ name: "create_show", params: { th_id: theatre_id } });
        },

        updateShow(ob) {
            this.$router.push({
                name: "update_show",
                params: { th_id: ob.theatre_id, s_id: ob.id },
            });
        },

        deleteShow(show_id) {
            const sure = confirm("Are you sure?");
            if (sure) {
                axios
                    .delete(`/api/show?show_id=${show_id}`)
                    .then(() => {
                        // alert("Successfully Deleted");
                        this.init_board();
                        this.$router.push({ name: "admin_board" });
                    })
                    .catch((err) => {
                        console.error("Error deleting Show:", err);
                        const errorMessage = err.response?.data?.error_message || "Error while deleting Show";
                        this.showErrorPopup(errorMessage);
                    });
            }
        },

        showErrorPopup(message) {
            this.errorPopupMessage = message;
        },

        closeErrorPopup() {
            this.errorPopupMessage = '';
        },

        async init_board() {
            this.theatres = null;
            var theatres_temp = null;

            await axios
                .get("/api/theatre")
                .then((res) => {
                    theatres_temp = res.data;
                })
                .catch((err) => {
                    console.log(err);
                });

            for (let i in theatres_temp) {
                await axios
                    .get(`/api/show?theatre_id=${theatres_temp[i].id}`)
                    .then((res) => {
                        if (res.data == undefined) {
                            theatres_temp[i].shows = [];
                        } else {
                            theatres_temp[i].shows = res.data;
                        }
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            }

            this.theatres = theatres_temp;
        },
    },

    async mounted() {
        await this.init_board();
        // console.log(this.theatres);
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

.add-theatre-btn i {
    margin-right: 5px;
}

.add-theatre-btn:hover {
    background-color: #2faaec;
    color: white;
}

.add-theatre-btn:focus {
    outline: none;
}
</style>
  