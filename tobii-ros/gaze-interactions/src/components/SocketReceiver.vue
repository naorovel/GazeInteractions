<template>
    <button @click="echo">Echo</button>
  </template>
  
  <script>
  import VueSocketIO from "vue-socket.io";
  export default {
    data() {
      return {
        socket: new VueSocketIO({
              debug: true,
              connection: 'http://localhost:3001'
        })
      }
    },
    methods: {
      async echo() {
        console.log(this.socket.io.connected); // prints true
      },
    },
  };
  </script>