<template>
    <div id="User">
      {{ page_info }}
      <br>
      {{ django_message }}
      <br>
      {{ django_message.zlsd01xl}}
      {{ django_message.zlsd01xltb}}
      <table border="1">
        <tr>
          <th>user</th>
        </tr>
        <tr v-for="user in user_list" :key="user">
          <td>{{ user }}</td>
        </tr>
      </table>
<!--      <iframe src="http://www.baidu.com" style="width: 2000px;height: 500px">-->
<!--    IE：你们都看我干吗，我现在也是支持的-->
<!--</iframe>-->

    </div>
</template>

<script>
    export default {
        name: "User",
      data(){
          return{
            page_info: "this User page",
            django_message:'',
            user_list:''
          }
      },
      created() {
            this.$axios.get('/dashboard/overallview')
        .then(response =>{
          this.django_message = response.data
        })
      },
    }
</script>

<style scoped>

</style>
