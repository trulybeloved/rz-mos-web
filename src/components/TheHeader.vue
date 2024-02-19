<script setup>
</script>

<template>
  <div class="greetings">
    <h1 class="green">Re:ZERO MoS Web</h1>
    <h3>
      A beautified and searchable version of the WCT MoS.<br>
    </h3>
    <h4>
      Sourced from: 
      <a href="https://docs.google.com/document/d/12Z5Jb61kz2QGQibnIukgEjK4oIgMYX45/edit" target="_blank" rel="noopener">Manual of Style</a>
      and
      <a href="https://docs.google.com/spreadsheets/d/1NyI4xID75sY3UvjT9iQPLIJvMCh0luh0AJYsDdD2KJU/edit" target="_blank" rel="noopener">Speaking Styles</a>
      <span style="font-weight: 200;">(updates every 24 hours thanks to @kroatoan)</span>
    </h4>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 700;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
