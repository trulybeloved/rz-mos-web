<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>

  <div class="topbar">

    <div class="header-container">

      <div class="header-logo">
        <img
        alt="logo"
        class="logo"
        src="../assets/rz_mos_web_logo.svg"
        width="100%"
        height="100%"
      />
      </div>


      <div class="header-text">
        <h1 class="green">Re:ZERO MoS Web</h1>
        <h3>A beautified and searchable version of the WCT MoS.<br /></h3>
        <h4>
          Sourced from:
          <a
            href="https://docs.google.com/document/d/12Z5Jb61kz2QGQibnIukgEjK4oIgMYX45/edit"
            target="_blank"
            rel="noopener"
            >Manual of Style</a
          >
          and
          <a
            href="https://docs.google.com/spreadsheets/d/1NyI4xID75sY3UvjT9iQPLIJvMCh0luh0AJYsDdD2KJU/edit"
            target="_blank"
            rel="noopener"
            >Speaking Styles</a
          >
          <span style="font-weight: 200">(updates every 24 hours thanks to @kroatoan)</span>
        </h4>
      </div>
    </div>
  
    <div class="navigation">
      <nav>
        <RouterLink to="/">Characters</RouterLink>
        <RouterLink to="/words">Words and Phrases</RouterLink>
      </nav>
    </div>

  </div>
</template>


<style scoped>

.topbar {
  display: flex;
  flex-direction: column;
}

.header-container {
  display: flex;
  flex-direction: row;
}

.header-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-grow: 0;
  flex-shrink: 1;
  flex-basis: 8%;
}

.header-text {
  display: flex;
  flex-direction: column;
  flex-grow: 0;
  flex-shrink: 1;
  flex-basis: 92%;
  justify-content: start;
  align-items: start;
  padding-left: 1rem;
}

h1 {
  font-weight: 700;
  font-size: 2rem;
}

h3 {
  font-size: 1rem;
}

h4 {
  font-size: 1rem;
}




.header-text h1,
.header-text h3 {
  text-align: left;
}

.header-logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  display: flex;
  width: 75px;
  height: 75px;

}

nav {
  width: 100%;
  font-size: 1.2em;
  text-align: center;
  padding: 0.8rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
  background-color: #242424;
}

nav a {
  display: inline-block;
  padding: 0.5rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media screen and (max-width: 700px) {

h3, h4 {
  font-size: 0;
}

nav {
  font-size: 1rem;
}
}



</style>
