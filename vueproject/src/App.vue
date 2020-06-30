<template>
  <div id="app">

    <div class="ui vertical sc-main center aligned segment"
         style="border-color: rgba(248,248,255,0.7);background-color: #2c3e50">
      <img src="./assets/logo.png"><br>
      <sui-container><!--创建ui容器-->
        <sui-container id="backg">
          <nav class="ui large secondary inverted pointing fixed menu main_nav align-items-center"
               style="border: white;display: flex !important;background-color: #2c3e50" id="header-fixed">
            <!--创建一个抬头标签-->
            <a class="toc item">
              <i class="sidebar icon"></i>
            </a>
            <div class="logo"><a href="index">Data</a></div>
            <ul id='fixed_menulist' class="right item d-flex">
              <!--遍历li标签-->
              <li v-for="item in activelist" @click="activeli" :class="{active:item.src==pathli}">
                <router-link class='item' :to=item.src>{{ item.name }}</router-link>
              </li>
              <sui-dropdown text="更多">
                <sui-dropdown-menu style="background-color: #2c3e50">
                  <sui-dropdown-item>
                    <router-link to="/name">信息</router-link>
                  </sui-dropdown-item>
                  <sui-dropdown-item>
                    <router-link to="/user">系统</router-link>
                  </sui-dropdown-item>
                </sui-dropdown-menu>
              </sui-dropdown>

            </ul>
          </nav>
        </sui-container>
        >
      </sui-container>
      >
    </div>
    <a is="sui-label" @click="buttoncli">
      <i class="arrows alternate large icon" style="width: 100%"></i>
    </a>
    <hr>
    <router-view/>

  </div>
</template>

<script>
  export default {
    name: 'App',
    data() {
      return {
        //定义加载标签明亮显示
        pathli: '/',
        activelist: [{src: '/', name: '总览'}, {src: '/user', name: '生产'}, {src: '/name', name: '销售'}, {
          src: '/fi',
          name: '财务'
        },
          {src: '/market', name: '市场'}, {src: '/hr', name: '人力'}, {src: '/qm', name: '质量'}, {src: '/mm', name: '物资'}],
        isFullscreen: false
      }
    },
    // 定义页面置顶变化
    mounted() {
      window.addEventListener('scroll', this.handleScroll);
      this.activeli(); //加载执行
    },
    methods: {
      handleScroll() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
        let offsetTop = document.querySelector('#backg').offsetTop;

        // console.log(scrollTop);
        scrollTop > 200 ? this.searchBarFixed = false : this.searchBarFixed = true
        // console.log(this.searchBarFixed);
      },
      //定义页面激活标签
      activeli() {
        let lipath = this.$route.path;
        if (lipath != '/') {
          this.pathli = lipath
        } else {
          this.pathli = '/'
        }
      },
      //定义全屏
      buttoncli() {
        this.$screenfull.toggle();
      },
    },
    destroyed() {
      window.removeEventListener('scroll', this.handleScroll)
    },
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>

