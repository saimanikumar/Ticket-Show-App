<template lang="">
    <div>
        <error-popup :error-message="errorPopupMessage" @close="closeErrorPopup"></error-popup>

        <div class="box-theatre-form card-div">
        <h1>Theatre</h1>
            <div>
                <div>
                    <label for="name_">Name  </label>
                    <input type="text" name="name_" placeholder="name" v-model="theatre_info.name" required="required" />
                </div>
                
                <div>
                    <label for="place">Place    </label>
                    <input type="text" name="place" placeholder="place" v-model="theatre_info.place" required="required" />
                </div>

                <div>
                    <label for="location">Location    </label>
                    <input type="text" name="location" placeholder="location" v-model="theatre_info.location" required="required" />
                </div>

                <div>
                    <label for="capacity">Capacity    </label>
                    <input type="number" name="capacity" placeholder="capacity" v-model="theatre_info.capacity" required="required" />
                </div>

                <button @click="postData" type="submit" class="btn btn-primary btn-block btn-large">Submit</button>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "../axios.js";
import ErrorPopup from '../components/ErrorPopUp.vue';

export default {

    data() {
        return {
            theatre_info: {
                name: null,
                place: null,
                location: null,
                capacity: null,
            },
            errorPopupMessage: ''
        }
    },

    components: {
        'error-popup': ErrorPopup
    },


    methods: {
        postData() {
            if (this.$route.params.id) {
                var baseUrl = `/api/theatre?id=${this.$route.params.id}`;
            } else {
                var baseUrl = '/api/theatre';
            }

            axios({
                method: this.$route.params.id ? 'PUT' : 'POST',
                url: baseUrl,
                data: this.theatre_info,
            })
                .then(() => {
                    // alert('data successfully Inserted')
                    this.$router.push({ name: 'admin_board' })
                })
                .catch((err) => {
                    const errorMessage = err.response?.data?.error_message || err.message;
                    this.showErrorPopup(errorMessage);
                })
        },
        showErrorPopup(message) {
            this.errorPopupMessage = message;
        },

        closeErrorPopup() {
            this.errorPopupMessage = '';
        },
    },

    async mounted() {
        if (this.$route.params.id) {
            await axios.get(`/api/theatre?id=${this.$route.params.id}`)
                .then((res) => {
                    this.theatre_info.name = res.data.name,
                        this.theatre_info.place = res.data.place,
                        this.theatre_info.location = res.data.location,
                        this.theatre_info.capacity = res.data.capacity,
                        console.log(res.data)
                })
                .catch((err) => {
                    this.error = err.message
                    console.log(err)
                })
        }
    },
}
</script>
<style scoped>
.box-theatre-form {
    position: absolute;
    top: 50%;
    left: 49%;
    margin: -150px 0 0 -150px;
    width: 300px;
    height: 300px;
}
</style>