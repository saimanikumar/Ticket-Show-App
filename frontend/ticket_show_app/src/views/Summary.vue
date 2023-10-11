<template>
    <h6 class="card-text user-name mar-fix" style="display: inline-block; font-size: x-large; padding-left: 0px;">
        <span v-for="i in 178">&nbsp;</span>
    </h6>

    <div class="summary-page">
        <div class="summary-navigation fixed-navigation">
            <ul>
                <li v-for="(chart, index) in charts" :key="index" @click="currentChartIndex = index"
                    :class="{ active: index === currentChartIndex }">
                    {{ chart.name }}
                </li>

                <li @click="showTheaterBarCharts" :class="{ active: currentChartIndex === charts.length }"
                    class="theater-charts-item">
                    Shows Analysis
                </li>
            </ul>
        </div>


        <div class="summary-content">
            <div v-for="(chart, index) in charts" :key="index" class="summary-card" v-show="index === currentChartIndex">
                <h2>{{ chart.name }}</h2>

                <Bar v-if="chart.type === 'bar'" :data="chart.data" :options="chart.options" v-bind:key="index"></Bar>
                <Line v-if="chart.type === 'line'" :data="chart.data" :options="chart.options" v-bind:key="index"></Line>
                <Pie v-if="chart.type === 'pie'" :data="chart.data" :options="chart.options" class="pie-chart"
                    v-bind:key="index"></Pie>

            </div>

            <div v-if="theatres && currentChartIndex === charts.length">
                <div class="row">
                    <div v-for="(theater, index) in theatres" :key="index" class="col-md-6 mb-4">
                        <div class="card theater-card">
                            <div class="card-header">
                                <span><i class="bi bi-building"></i> {{ theater.name }}</span>
                            </div>
                            <div class="card-body">
                                <div v-if="theaterBarData[index].noData" class="no-shows">
                                    <p>No shows yet!</p>
                                </div>
                                <div v-else class="theater-card">
                                    <Bar :data="theaterBarData[index].data" :options="theaterBarData[index].options"></Bar>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>

<script>
import { Bar, Line, Pie } from 'vue-chartjs';
import Chart from 'chart.js/auto';
import axios from "../axios.js";


export default {

    components: {
        Bar,
        Line,
        Pie
    },

    data() {
        return {
            currentChartIndex: 0,
            theatres: null,

            charts: [
                {
                    name: 'Revenue by Theatre',
                    type: 'bar',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: 'Revenue',
                                data: [],
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1,
                            },
                        ],
                    },
                    options: {},
                },
                {
                    name: 'Revenue by Show',
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: 'Revenue',
                                data: [],
                                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                                borderColor: 'rgba(255, 159, 64, 1)',
                                borderWidth: 1,
                            },
                        ],
                    },
                    options: {},
                },
                {
                    name: 'Revenue Over Time',
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: 'Revenue',
                                data: [],
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1,
                            },
                        ],
                    },
                    options: {},
                },
                {
                    name: 'Revenue by Location',
                    type: 'bar',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: 'Revenue',
                                data: [],
                                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                borderColor: 'rgba(153, 102, 255, 1)',
                                borderWidth: 1,
                            },
                        ],
                    },
                    options: {},
                },
                {
                    name: 'Revenue Share by Theatre',
                    type: 'pie',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: 'Revenue',
                                data: [],
                                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                borderColor: 'rgba(153, 102, 255, 1)',
                                borderWidth: 1,
                            },
                        ],
                    },
                    options: {},
                },
            ],

            theaterBarData: [],
        };
    },
    async mounted() {
        await this.fetchRevenueData();
        await this.init_board();
        // console.log(this.theatres)
    },
    methods: {
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString("en-IN");
        },
        formatDateCompact(dateString) {
            const date = new Date(dateString);
            const options = { month: 'short', day: 'numeric' };
            return date.toLocaleDateString("en-IN", options);
        },
        async showTheaterBarCharts() {
            this.currentChartIndex = this.charts.length;
            // console.log(this.currentChartIndex, this.charts.length)
            if (this.theatres) {
                this.theaterBarData = this.theatres.map((theater) => {
                    if (theater.shows.length === 0) {
                        return {
                            noData: true,
                        };
                    }
                    
                    const showNames = theater.shows.map(item => item.name);
                    const ticketCounts = theater.shows.map(item => item.capacity - item.available_tickets);

                    return {
                        data: {
                            labels: showNames,
                            datasets: [
                                {
                                    label: 'Number of Tickets Booked',
                                    data: ticketCounts,
                                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1,
                                },
                            ],
                        },
                        options: {
                            scales: {
                                y: {
                                    ticks: {
                                        beginAtZero: true, 
                                        stepSize: 1,     
                                        precision: 0,    
                                    },
                                },
                            },
                        },
                    };
                });
                // console.log(this.theaterBarData)
            }
            else{

            }

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


        async fetchRevenueData() {

            await axios
                .get('/api/revenue')
                .then((response) => {

                    var revenue_by_theatre = response.data.revenue_by_theatre;
                    var revenue_by_show = response.data.revenue_by_show;
                    var revenue_over_time = response.data.revenue_over_time;
                    var revenue_by_location = response.data.revenue_by_location;
                    var revenue_share_by_theatre = response.data.revenue_share_by_theatre;

                    var x = [];
                    var y = [];
                    if (revenue_by_theatre) {
                        var x = revenue_by_theatre.map(item => item.name);
                        var y = revenue_by_theatre.map(item => item.revenue);
                    }

                    const chartData = {
                        labels: x,
                        datasets: [
                            {
                                label: 'Revenue',
                                data: y,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1,
                            },
                        ],
                    };

                    this.charts[0].data = chartData;


                    if (revenue_by_show) {
                        this.charts[1].data = {
                            labels: revenue_by_show.map((item) => item.name),
                            datasets: [
                                {
                                    label: 'Revenue',
                                    data: revenue_by_show.map((item) => item.revenue),
                                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                                    borderColor: 'rgba(255, 159, 64, 1)',
                                    borderWidth: 1,
                                },
                            ],
                        };
                    }

                    // chart data for Revenue Over Time
                    if (revenue_over_time) {
                        this.charts[2].data = {
                            labels: revenue_over_time.map((item) => item.date),
                            datasets: [
                                {
                                    label: 'Revenue',
                                    data: revenue_over_time.map((item) => item.revenue),
                                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    borderWidth: 1,
                                },
                            ],
                        };
                    }

                    // chart data for Revenue by Location
                    if (revenue_by_location) {
                        this.charts[3].data = {
                            labels: revenue_by_location.map((item) => item.location),
                            datasets: [
                                {
                                    label: 'Revenue',
                                    data: revenue_by_location.map((item) => item.revenue),
                                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                    borderColor: 'rgba(153, 102, 255, 1)',
                                    borderWidth: 1,
                                },
                            ],
                        };
                    }

                    // chart data for Revenue Share by Theatre
                    if (revenue_share_by_theatre) {
                        this.charts[4].data = {
                            labels: revenue_share_by_theatre.map((item) => item.name),
                            datasets: [
                                {
                                    label: 'Revenue Share',
                                    data: revenue_share_by_theatre.map((item) => item.revenue_share),
                                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                    borderColor: 'rgba(255, 99, 132, 1)',
                                    borderWidth: 1,
                                },
                            ],
                        };
                    }


                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
};
</script>

<style scoped>

.theater-card {
    height: 380px;
    width: 100%;
}

.summary-page {
    display: flex;
}

.summary-navigation {
    width: 200px;
    padding: 20px;
}

.summary-navigation ul {
    list-style-type: none;
    margin: 0;
    padding: 0px;
}

.summary-navigation li {
    cursor: pointer;
    padding: 10px;
}

.summary-navigation li:hover {
    background-color: #a0c8de76;
    border-radius: 8px;

}

.summary-navigation li.active {
    background-color: #8bcff4;
    border-radius: 10px;
}

.summary-content {
    flex-grow: 1;
    padding: 15px;
    padding-left: 35px;
}

.summary-card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    height: 550px;
    width: 75%;
    align-items: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.theater-charts-item {
    cursor: pointer;
    width: 160px;
}

.no-shows {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-size: 18px;
    color: gray;
}

h2 {
    font-size: 20px;
    margin-bottom: 10px;
}

canvas {
    width: 300px;
    height: 300px;
}

</style>


