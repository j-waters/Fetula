<template>
  <div id="app">
    <v-app>
      <transition name="fade" mode="out-in">
    <router-view/>
      </transition>
    </v-app>
  </div>
</template>

<script>

</script>

<style lang="css">

::-webkit-scrollbar { 
    display: none; 
}

.container {
    max-width: 95%;
}

.fade-enter-active, .fade-leave-active {
  transition-property: opacity;
  transition-duration: .25s;
}

.fade-enter-active {
  transition-delay: .25s;
}

.fade-enter, .fade-leave-active {
  opacity: 0
}

</style>
