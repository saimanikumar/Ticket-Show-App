<template>
  <div class="star-rating">
    <span
      v-for="star in stars"
      :key="star"
      @click="handleClick(star)"
      :class="{ 'filled': star <= (disabled ? rating : currentRating) }"
    >
      ★
    </span>
  </div>
</template>

<script>
export default {
  props: {
    rating: {
      type: Number,
      default: 0,
      validator: (value) => value >= 0 && value <= 5,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      stars: [1, 2, 3, 4, 5],
      currentRating: this.rating,
    };
  },
  methods: {
    handleClick(rating) {
      if (!this.disabled) {
        this.currentRating = rating;
        this.$emit("change", this.currentRating);
      }
    },
  },
};
</script>

<style scoped>
.star-rating {
  font-size: 24px;
  cursor: pointer;
}

.filled {
  color: gold;
}
</style>
