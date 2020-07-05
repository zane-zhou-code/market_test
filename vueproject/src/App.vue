<template>
  <div id="app">
    <div class="ui vertical sc-main center aligned segment"
         style="border-color: rgba(248,248,255,0.7);background-color: #2c3e50">
      <img src="./assets/logo.png">
      <br>
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
      </sui-container>
    </div>
    <a is="sui-label" @click="buttoncli">
      <i class="arrows alternate black large icon" style="width: 100%"></i>
    </a>
    <a is="sui-label" @click="showsetting">
      <i class="wrench black large icon" style="width: 100%"></i>
    </a>
    <a is="sui-label" v-if="btnFlag" class="go-top" @click="backTop">
          <i class="angle double up orange large icon" style="width: 100%"></i>
    </a>
    <hr>
    <sui-sidebar-pushable>
      <!--setting菜单-->
      <sui-sidebar class="right thin labeled menu" :visible="visible">
        <sui-tab active-index="2">
          <sui-tab-pane icon="red rocketchat" title="">
            <sui-feed active>
              <h4 is="sui-header">question</h4>
              <sui-feed-event>
                <sui-feed-label><img src="src/style/images/background2.jpg"/></sui-feed-label>
                <sui-feed-content>
                  <sui-feed-date>3 days ago</sui-feed-date>
                  <sui-feed-summary>"you added to your work"</sui-feed-summary>
                </sui-feed-content>
              </sui-feed-event>
            </sui-feed>
          </sui-tab-pane>
          <sui-tab-pane icon="blue tiny cogs" title="">
            <sui-form>
              <sui-form-fields grouped>Connection Limited
                <sui-form-field>
                  <sui-checkbox radio name="connection" slider label="10 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox radio name="connection" slider label="20 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox radio name="connection" slider label="30 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox radio name="connection" slider label="40 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
            <sui-divider></sui-divider>
            <sui-form>
              <sui-form-fields grouped>Connection Limited
                <sui-form-field>
                  <sui-checkbox radio toggle name="connection" label="10 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox radio toggle name="connection" label="20 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox radio toggle name="connection" label="30 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox radio toggle name="connection" label="40 mbps max">
                    <sui-input checked>
                    </sui-input>
                  </sui-checkbox>
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
            <sui-divider></sui-divider>
          </sui-tab-pane>
        </sui-tab>
      </sui-sidebar>
      <sui-sidebar-pusher :dimmed="visible" style="width: 100%;height: 100%">
        <!--当前网页内容-->
        <router-view/>
      </sui-sidebar-pusher>
    </sui-sidebar-pushable>
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
        isFullscreen: false,
        visible: false,
        //定义置顶图标显示
        btnFlag: false
      }
    },
    // 定义页面置顶变化
    mounted() {
      window.addEventListener('scroll', this.handleScroll);
      this.activeli(); //加载执行
      //定义监听点击事件
      document.addEventListener('click', (e) => {
        let thisClassName = e.target.className;
        //若幕布已启动,调用showsetting函数关闭sidebar
        if (thisClassName == 'pusher dimmed') {
          this.showsetting();
        }
      });
      //监听置顶事件
      window.addEventListener('scroll', this.scrollToTop);
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
      //定义菜单栏
      showsetting: function () {
        if (this.visible == false) {
          this.visible = true
        } else (
          this.visible = false
        )
      },
      // 点击按钮回到顶部方法，加计时器是为了过渡顺滑
      backTop() {
        const that = this;
        let timer = setInterval(() => {
          let ispeed = Math.floor(-that.scrollTop / 5);
          document.documentElement.scrollTop = document.body.scrollTop = that.scrollTop + ispeed
          if (that.scrollTop === 0) {
            clearInterval(timer)
          }
        }, 16)
      },
      // 为了计算距离顶部的高度，当高度大于60显示回顶部图标，小于60则隐藏
      scrollToTop() {
        const that = this;
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
        that.scrollTop = scrollTop;
        if (that.scrollTop > 60) {
          that.btnFlag = true
        } else {
          that.btnFlag = false
        }
      }
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

