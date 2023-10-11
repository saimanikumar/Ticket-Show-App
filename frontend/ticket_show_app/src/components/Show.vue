<template>
    <div>
        <div class="list-column col-lg-12">
            <div class="card card-card1">
                <div class="card-header">
                    <div class="dropdown">
                        <button type="button" class="btn btn-light dropdown-toggle" data-bs-toggle="dropdown">
                            <i class="bi bi-film"></i> {{ show.name }}
                        </button>
                        <ul class="dropdown-menu">
                            <li>
                                <a @click="updateEmit(show.id, show.theatre_id)"
                                    class="dropdown-item btn btn-outline-primary">
                                    <i class="bi bi-pencil"></i> Update
                                </a>
                            </li>
                            <li>
                                <a @click="$emit('delete-card', show.id)" class="dropdown-item btn btn-outline-danger">
                                    <i class="bi bi-trash"></i> Delete</a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="card-body">

                    <p class="card-text"><i class="bi bi-star"></i> {{ show.rating }}</p>
                    <p class="card-text"><i class="bi bi-cash"></i> Price - {{ show.ticket_price }}</p>
                    <p class="card-text"><i class="bi bi-calendar"></i> {{ show.show_date.split(' ')[0] }}</p>
                    <p class="card-text"><i class="bi bi-clock"></i> {{
                        show.start_time.slice(0, -3) }} - {{ show.end_time.slice(0, -3) }}
                    </p>
                    <p>{{ show.tags }}</p>
                    <span>Status: <b>{{ showStatus(show) }}</b></span>

                </div>
            </div>
        </div>
    </div>
</template>
  
<script>

function compareDateOnly(date1, date2) {
    const yearDiff = date1.getFullYear() - date2.getFullYear();
    const monthDiff = date1.getMonth() - date2.getMonth();
    const dayDiff = date1.getDate() - date2.getDate();

    if (yearDiff === 0 && monthDiff === 0 && dayDiff === 0) {
        return 0;
    } else if (yearDiff > 0 || (yearDiff === 0 && monthDiff > 0) || (yearDiff === 0 && monthDiff === 0 && dayDiff > 0)) {
        return 1;
    } else {
        return -1;
    }
}

export default {
    props: ["show"],
    data() {
        return {};
    },

    components: {},

    computed: {

    },

    methods: {


        showStatus(show) {
            const now = new Date();
            const showDate = new Date(show.show_date);
            const showStartTime = new Date(`${show.show_date}T${show.start_time}`);
            const showEndTime = new Date(`${show.show_date}T${show.end_time}`);
            var currentHour = now.getHours();
            const currentMinutes = String(now.getMinutes());
            const startHour = show.start_time.slice(0, 2);
            const startMinutes = show.start_time.slice(3, 5);
            const endHour = show.end_time.slice(0, 2);
            const endMinutes = show.end_time.slice(3, 5);
            currentHour = String(currentHour);


            if (compareDateOnly(showDate, now) === 1) {
                return 'Upcoming';
            } else if (compareDateOnly(showDate, now) === 0 && ((currentHour < startHour) || (currentHour == startHour && currentMinutes < startMinutes))) {
                return 'Upcoming';
            } else if (compareDateOnly(showDate, now) === 0) {

                if (
                    (currentHour > startHour || (currentHour === startHour && currentMinutes >= startMinutes)) &&
                    (currentHour < endHour || (currentHour === endHour && currentMinutes <= endMinutes))
                ) {
                    return 'Ongoing';
                }
                else {
                    console.log(String(currentHour), startHour, currentMinutes, startMinutes, show.start_time.slice(0, 2))
                    return 'Completed';
                }
            } else if (compareDateOnly(showDate, now) === -1 && now >= showEndTime) {
                return 'Completed';
            } else {
                return 'Unknown';
            }
        },


        updateEmit(show_id, theatre_id) {
            this.$emit("update-card", {
                id: show_id,
                theatre_id: theatre_id,
            });
        },
    },
};
</script>
  
<style scoped>
p {
    padding: 0.1px;
}
</style>
  