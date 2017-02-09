<template>

   <ul>
       <li v-for="name in usernames">{{name}}</li>
   </ul>

</template>

<script>

export default {

    data() {

        return {

            usernames: ["max", "rimk", "madjid"]

        }

    }
}



</script>
