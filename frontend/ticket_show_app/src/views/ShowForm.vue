


<template lang="">
<div>
    <error-popup :error-message="errorPopupMessage" @close="closeErrorPopup"></error-popup>

    <div class="box-show-form card-div ">
        <h3>Show</h3>

        <div>
        
            <!-- <div class="form-group">
                <label for="show-card">Lists</label>
                <select v-model="show_info.id" name="show-card" class="custom-select custom-dropdown custom-form-input">
                        <option v-for="theatre_list in theatre_lists" :value="theatre_list.id" :selected="theatre_list.id == show_info.theatre_id" >{{ theatre_list.name }}</option>
                </select>
            </div> -->

            <div>
                <label for="name_">Title </label>
                <input type="text" name="name_" placeholder="title" v-model="show_info.name" required="required" />
            </div>


            <div>
                <label for="rating">Rating</label>
                <input type="number" id="rating" name="rating" placeholder="Scale of 1-10" v-model="show_info.rating" min="1" max="10" step="0.5" />
            </div>


            <div>
                <label for="tags">Tags</label>
                <input type="text" name="tags" placeholder="action, family..." v-model="show_info.tags" />
            </div>
            
            <div>
                <label for="ticket_price">Ticket Price</label>
                <input type="number" name="ticket_price" placeholder="ticket-price" v-model="show_info.ticket_price" required />
            </div>

            <div>
                <label for="show_date">Show Date</label>
                <input type="date" name="show_date" v-model="show_info.show_date" 
                :min="t_date" required />
            </div>

            <div>
                <label for="start_time">Start Time</label>
                <input type="time" name="start_time" v-model="show_info.start_time" 
               required />
            </div>

            <div>
                <label for="end_time">End Time</label>
                <input type="time" name="end_time" v-model="show_info.end_time" required />
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
            show_info: {
                id: null,
                name: '',
                rating: null,
                tags: '',
                ticket_price: null,
                show_date: null,
                start_time: null,
                end_time: null,
                theatre_id: null,
            },

            theatre_lists: null,
            errorPopupMessage: ''

        }
    },

    components: {
        'error-popup': ErrorPopup
    },

    computed: {
        t_date() { return new Date().toLocaleDateString('en-ca') },
    },

    methods: {
        postData() {

            if (this.$route.params.s_id) {
                var baseUrl = `/api/show?theatre_id=${this.$route.params.th_id}&show_id=${this.$route.params.s_id}`

            } else {
                var baseUrl = `/api/show?theatre_id=${this.$route.params.th_id}`
            }
            this.show_info.theatre_id = this.$route.params.th_id
            axios({
                method: this.$route.params.s_id ? 'PUT' : 'POST',
                url: baseUrl,
                data: this.show_info,
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
        var my_theatres = null

        await axios.get('/api/theatre')
            .then((res) => {
                my_theatres = res.data

            })
            .catch((err) => {
                this.error = err.message
                console.log(err)
            })

        this.theatre_lists = my_theatres

        if (this.$route.params.s_id) {
            await axios.get(`/api/show?theatre_id=${this.$route.params.th_id}&show_id=${this.$route.params.s_id}`)
                .then((res) => {
                    this.show_info.id = res.data.id
                    this.show_info.name = res.data.name
                    this.show_info.rating = res.data.rating
                    this.show_info.tags = res.data.tags
                    this.show_info.show_date = (res.data.show_date).split(' ')[0]
                    this.show_info.ticket_price = res.data.ticket_price
                    this.show_info.start_time = res.data.start_time
                    this.show_info.end_time = res.data.end_time
                    this.show_info.theatre_id = res.data.theatre_id
                    console.log(this.show_info)
                    console.log(res.data)
                })
                .catch((err) => {
                    this.error = err.message
                    console.log(err)
                })
        }
    }

}
</script>
<style scoped>
    
</style>