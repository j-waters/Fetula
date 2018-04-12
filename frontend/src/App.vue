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

html {
  /*overflow-y: hidden;*/
  width: 100vw;
}

/* Let's get this party started */
::-webkit-scrollbar {
    width: 7px;
    top: 64px;
}
 
/* Track */
::-webkit-scrollbar-track {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    /*display: none;*/
}
 
/* Handle */
::-webkit-scrollbar-thumb {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    background: grey; 
}
::-webkit-scrollbar-thumb:window-inactive {
	background: grey; 
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
