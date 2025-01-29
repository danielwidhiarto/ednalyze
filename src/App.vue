<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">EDnalyze</a>
        <div class="navbar-nav ms-auto">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/watchlist" class="nav-link">⭐ Watchlist</router-link>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  setup() {
    return {}
  },
}
</script>

<style>
/* Styling Navbar */
.navbar-nav .nav-link {
  font-weight: 500;
  padding: 0.5rem 1rem;
}

.navbar-nav .nav-link:hover {
  text-decoration: underline;
}
</style>
