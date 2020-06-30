<template>
  <div id="myChart" class="dimmer">
    <sui-button primary>Primary</sui-button>
    <sui-button secondary>Secondary</sui-button>
    <div style="width: 500px;height: 500px" ref="chart"></div>
    <sui-comment-group>
      <sui-comment>
        <sui-comment-avatar src="../xfm_dev/static/images/background1.jpg"/>
        <sui-comment-content>
          <a is="sui-comment-author">Christian Rocha</a>
          <sui-comment-metadata>
            <div>2 days ago</div>
          </sui-comment-metadata>
          <sui-comment-text
          >I'm very interested in this motherboard. Do you know if it'd work in
            an Intel LGA775 CPU socket?
          </sui-comment-text
          >
          <sui-comment-actions>
            <sui-comment-action>Reply</sui-comment-action>
          </sui-comment-actions>
        </sui-comment-content>
        <sui-comment-group >
          <sui-comment>
            <sui-comment-avatar src="../xfm_dev/static/images/background2.jpg"/>
            <sui-comment-content>
              <a is="sui-comment-author">Elliot Fu</a>
              <sui-comment-metadata>
                <div>1 day ago</div>
              </sui-comment-metadata>
              <sui-comment-text>
                No it won't.
              </sui-comment-text>
              <sui-comment-actions>
                <sui-comment-action>Reply</sui-comment-action>
              </sui-comment-actions>
            </sui-comment-content>
            <sui-comment-group>
              <sui-comment>
                <sui-comment-avatar src="../xfm_dev/static/images/background3.jpg"/>
                <sui-comment-content>
                  <a is="sui-comment-author">Me</a>
                  <sui-comment-metadata>
                    <div>20 minutes ago</div>
                  </sui-comment-metadata>
                  <sui-comment-text>
                    Maybe it would.
                  </sui-comment-text>
                  <sui-comment-actions>
                    <sui-comment-action>Reply</sui-comment-action>
                  </sui-comment-actions>
                </sui-comment-content>
              </sui-comment>
            </sui-comment-group>
          </sui-comment>
        </sui-comment-group>
      </sui-comment>
    </sui-comment-group>
  <count-to :startVal='startVal' :endVal='endVal' :duration='duration'></count-to>

<sui-button class="dimmer-wrapper" id="example2">
<li v-for="(item,index) in newList" v-on:click="addclass(index)" :class="{'active':index==current}">
     <router-link :to=item.src> {{item.name}}||{{index}}</router-link>
<sui-dimmer @click="dimmerfuc" :class="{active:dimmertext==1}" :inverted="false">
  最近访问页面
</sui-dimmer>
<!--  </sui-segment>-->

</li>
<!--<li class="active">qqqq</li>-->
<!--        <li>wwww</li>-->
<!--        <li>eeee</li>-->
    </sui-button>
  </div>

</template>

<script>
    import countTo from 'vue-count-to';
  export default {
    name: "Name",
    components: { countTo },
    data () {
      return {
        current:0,
          newList:[{src:'', name:'总览'}, {src:'',name:'生产'}, {src:'',name:'销售'}, {src:'',name:'财务'},
          {src:'',name:'市场'}, {src:'',name:'人力'}, {src:'',name:'质量'}, {src:'',name:'物资'}],
          dimmertext:1,
        // 需要滚动的时间
        duration: 5000,
        // 初始值
        startVal: 0,
        // 最终值
        endVal: 2018
      }},
    methods: {
      initCharts() {
        let myChart = this.$echarts.init(this.$refs.chart);
        console.log(this.$refs.chart)
        // 绘制图表
        myChart.setOption({
          title: {text: '在Vue中使用echarts'},
          tooltip: {},
          xAxis: {
            data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
          },
          yAxis: {},
          series: [{
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }]
        });
      },
      //增加幕布效果
      dimmerfuc() {
        document.addEventListener('click', function (e) {
          console.log(this.$refs)

        });
      },
      addclass: function (index) {
        this.current = index;
      }},
      mounted() {
        this.initCharts();
        document.addEventListener('click', (e) => {
          let thisClassName = e.target.className;
          if (thisClassName != 'ui dimmer active') {
            this.dimmertext = 0
          }
        });
      }
    }
</script>

<style scoped>
.ui.dimmer{
  top:50% !important;
  left:50% !important;
  transform: translate(-50%,-50%) !important;
  width: 50% !important;
  height: 50% !important;
  background-color: rgba(8,13,16,0.2) !important;
}
</style>
