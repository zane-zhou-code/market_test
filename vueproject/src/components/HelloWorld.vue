<template>
  <div class="hello">
    <!--数据总览-->
    <sui-container>
      <sui-grid :columns="4" stackable centered>
        <!--搜索框-->
        <sui-grid-row>
          <sui-grid-column>
            <sui-form data-method="post">
              <h3 is="sui-header" text-align="center">分析维度</h3>
              <sui-form-fields fields="two">
                <sui-form-field>
                  <sui-input type="text" placeholder="2020-01" icon="spinner"></sui-input>
                </sui-form-field>
                <sui-form-field>
                  <sui-input type="text" placeholder="2020-07" icon="spinner"></sui-input>
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
      <!--财务数据-->
      <sui-grid :columns="2" stackable centered>
        <sui-grid-column>
          <sui-segment class="columnstyle">
            <sui-grid :columns="2" centered>
              <sui-grid-row>
                <sui-grid-column vertical-align="middle">
                  <h3 is="sui-header">财务分析</h3>
                </sui-grid-column>
              </sui-grid-row>
              <!--利润 毛利-->
              <sui-grid-row>
                <sui-grid-column vertical-align="middle">
                  <a style="position: relative">
                    <div slot="label">
                      <sui-label circular color="red" size="tiny" floating>万</sui-label>
                      <sui-button content="利润" size="tiny" compact>
                        <a is="sui-label" slot="label" basic class="counter">
                          <count-to :startVal='0' :endVal='13048' :duration='2500'></count-to>
                        </a>
                      </sui-button>
                    </div>
                  </a>
                </sui-grid-column>
                <sui-grid-column vertical-align="middle">
                  <a style="position: relative">
                    <div slot="label">
                      <sui-label circular color="teal" size="tiny" floating>
                        <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                      </sui-label>
                      <sui-button content="毛利" size="tiny" slot="label" compact>
                        <a is="sui-label" slot="label" basic>2.85%</a>
                      </sui-button>
                    </div>
                  </a>
                </sui-grid-column>
              </sui-grid-row>
              <!--季度公告利润 毛利-->
              <sui-grid-row>
                <sui-grid-column vertical-align="middle">
                  <a style="position: relative">
                    <div slot="label">
                      <sui-label circular color="red" size="tiny" floating>万</sui-label>
                      <sui-button content="季度利润" size="tiny" compact>
                        <a is="sui-label" slot="label" basic>
                          <count-to :startVal='0' :endVal='53048' :duration='2500'></count-to>
                        </a>
                      </sui-button>
                    </div>
                  </a>
                </sui-grid-column>
                <sui-grid-column vertical-align="middle">
                  <a style="position: relative">
                    <div slot="label">
                      <sui-label circular color="teal" size="tiny" floating>
                        <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                      </sui-label>
                      <sui-button content="季度毛利" size="tiny" slot="label" compact>
                        <a is="sui-label" slot="label" basic>5.85%</a>
                      </sui-button>
                    </div>
                  </a>
                </sui-grid-column>
              </sui-grid-row>
            </sui-grid>
          </sui-segment>
        </sui-grid-column>
        <sui-grid-column>
          <!--fi01图-->
          <sui-segment class="columnstyle">
            <div ref="fi01" style="width: 100%;height: 130%;"></div>
          </sui-segment>
        </sui-grid-column>
      </sui-grid>
      <!--总览数据-->
      <!--四列栏目-->
      <sui-grid :columns="4" stackable centered>
        <!--销售 人力 生产 库存-->
        <sui-grid-row id="allcol">
          <!--总览 销售-->
          <sui-grid-column id="sdcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">销售情况</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 销量/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>吨</sui-label>
                        <sui-button content="销量" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>2,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="teal" size="tiny" floating>
                          <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>2.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 金额/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>万</sui-label>
                        <sui-button content="金额" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>3,052</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>
                          <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>3.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 均价/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>¥/T</sui-label>
                        <sui-button content="均价" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>580</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>
                          <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>2.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
          <!--总览 人力-->
          <sui-grid-column id="hrcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">人员概览</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--人力 总人数/公司占比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-button content="总数" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>12,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--hr01图-->
                <sui-grid-row>
                  <div ref="hr01" style="width: 100%;height: 150px;"></div>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
          <!--总览 生产-->
          <sui-grid-column id="sccol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column>
                    <h3 is="sui-header">生产规模</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--生产 产量/装置分布-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-button content="产量" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>150,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--sc01图-->
                <sui-grid-row>
                  <div ref="sc01" style="width: 100%;height: 100%;"></div>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
          <!--总览 库存-->
          <sui-grid-column id="mmcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">库存分布</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--库存 内外贸库存-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>吨</sui-label>
                        <sui-button content="内贸成品" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>18,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>吨</sui-label>
                        <sui-button content="外贸成品" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>15,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--库存 库存天数-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>天</sui-label>
                        <sui-button content="库存天数" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>17.52</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>吨</sui-label>
                        <sui-button content="PTA" size="mini" slot="label" compact>
                          <a is="sui-label" slot="label" basic>98,580</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="mini" floating>吨</sui-label>
                        <sui-button content="MEG" size="mini" slot="label" compact>
                          <a is="sui-label" slot="label" basic>8,580</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
        </sui-grid-row>
        <!--安全 物资 质量 信息-->
        <sui-grid-row>
          <!--总览 安全-->
          <sui-grid-column id="aqcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">安全状况</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 销量/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>吨</sui-label>
                        <sui-button content="销量" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>2,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="teal" size="tiny" floating>
                          <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>2.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 金额/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>万</sui-label>
                        <sui-button content="金额" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>3,052</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>
                          <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>3.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 均价/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>¥/T</sui-label>
                        <sui-button content="均价" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>580</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>
                          <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>2.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
          <!--总览 物资-->
          <sui-grid-column id="wzcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">物资采购</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--物资 采购总量-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-button content="总量" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>12,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--物资 供应商分布-->
                <sui-divider></sui-divider>
                <sui-grid-row >

                    <sui-segments>
                      <sui-table aligned="left" class="segment" celled striped collapsing>
                        <!--表头-->
                        <sui-table-header>
                          <sui-table-row>
                            <sui-table-header-cell single-line>供应商</sui-table-header-cell>
                            <sui-table-header-cell>采购金额</sui-table-header-cell>
                            <sui-table-header-cell>采购数量</sui-table-header-cell>
                            <sui-table-header-cell>采购单价</sui-table-header-cell>
                          </sui-table-row>
                        </sui-table-header>
                        <!--表体-->
                        <!--第一行-->
                        <sui-table-body>
                          <sui-table-row>
                            <sui-table-cell>
                              <h4 is="sui-header" style="text-align: center">新凤鸣</h4>
                            </sui-table-cell>
                            <sui-table-cell single-line>10000</sui-table-cell>
                            <sui-table-cell>500</sui-table-cell>
                            <sui-table-cell>10.1</sui-table-cell>
                          </sui-table-row>
                        </sui-table-body>
                        <!--第二行-->
                        <sui-table-body>
                          <sui-table-row>
                            <sui-table-cell>
                              <h4 is="sui-header" style="text-align: center">桐昆</h4>
                            </sui-table-cell>
                            <sui-table-cell single-line>52000</sui-table-cell>
                            <sui-table-cell>3300</sui-table-cell>
                            <sui-table-cell>8.91</sui-table-cell>
                          </sui-table-row>
                        </sui-table-body>
                        <!--第三行-->
                        <sui-table-body>
                          <sui-table-row>
                            <sui-table-cell>
                              <h4 is="sui-header" style="text-align: center">恒力</h4>
                            </sui-table-cell>
                            <sui-table-cell single-line>9800</sui-table-cell>
                            <sui-table-cell>780</sui-table-cell>
                            <sui-table-cell>1.5</sui-table-cell>
                          </sui-table-row>
                        </sui-table-body>
                      </sui-table>
<!--                        </sui-segment sui-ta>-->
                    </sui-segments>

                </sui-grid-row>
                <!--wz01图-->
                <sui-grid-row>
                  <div ref="wz01" style="width: 100%;height: 150px;"></div>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
          <!--总览 质量-->
          <sui-grid-column id="qmcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">质量中心</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 销量/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>吨</sui-label>
                        <sui-button content="销量" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>2,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="teal" size="tiny" floating>
                          <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>2.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 金额/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>万</sui-label>
                        <sui-button content="金额" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>3,052</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>
                          <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>3.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--销售 均价/同比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>¥/T</sui-label>
                        <sui-button content="均价" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>580</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating>
                          <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-button content="同比" size="tiny" slot="label" compact>
                          <a is="sui-label" slot="label" basic>2.85%</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
          <!--总览 信息-->
          <sui-grid-column id="ifcol">
            <sui-segment class="columnstyle">
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">信息管理</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--人力 总人数/公司占比-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a style="position: relative">
                      <div slot="label">
                        <sui-button content="总数" size="tiny" compact>
                          <a is="sui-label" slot="label" basic>12,048</a>
                        </sui-button>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--if01图-->
                <sui-grid-row>
                  <div ref="if01" style="width: 100%;height: 150px;"></div>
                </sui-grid-row>
              </sui-grid>
            </sui-segment>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
    </sui-container>
  </div>

</template>

<script>
  import countTo from 'vue-count-to'

  const colors = ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf', '#9192ab', '#7898e1',
    '#efa666', '#eddd86', '#9987ce', '#63b2ee', '#76da91'];
  export default {
    name: 'HelloWorld',
    components: {countTo},
    data() {
      return {
        msg: 'Welcome to Your Vue.js App',
        message: 'learn vue',
        news: 'this is my own place'
      }
    },
    methods: {
      initCharts() {
        let myChartfi01 = this.$echarts.init(this.$refs.fi01);
        console.log(this.$refs.fi01);
        // 绘制图表
        myChartfi01.setOption({
          title: {text: '同类公司财务分析', textstyle: {fontSize: 15,}},
          tooltip: [{
            trigger: 'axis',
            formatter(value) {
              // console.log(value);
              let str = value[0].name + '<br/>';
              // console.log(str);
              value.forEach(item => {
                // console.log(item);
                var i = item.seriesIndex + 1;
                if (item.seriesType == 'line') {
                  str += item.marker + item.seriesName + '利润:' + item.data[i] + '<br/>';
                } else if (item.seriesType == 'bar') {
                  str += item.marker + item.seriesName + '毛利率%:' + item.data[i] + '<br/>';
                }
              });
              return str
            }
          }],
          legend: [{data: ['新凤鸣', '桐昆', '恒力']}],
          dataset: {
            source: [['quarter', "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1"],
              ['新凤鸣', 5, 20, 36, 10, 10, 20],
              ['桐昆', 15, 25, 40, 20, 25, 36],
              ['恒力', 80, 110, 210, 210, 21, 136],
              ['新凤鸣', 5, 6, 7, 8, 9, 4],
              ['桐昆', 10, 12, 15, 13, 11, 9],
              ['恒力', 15, 12, 11, 16, 18, 20],]
          },
          xAxis: {
            data: ["2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1"],
            show: true,
            axisTick: {show: false},
            axisLine: {show: false},
          },
          grid: [{x: '7%', y: '30%', width: '86%', height: '60%'}],
          yAxis: [{
            type: 'value',
            name: '利润(柱状)',
            scale: true,
            splitLine: {show: false},
            axisLine: {show: false},
            axisTick: {show: false},
            show: true,
          },
            {
              type: 'value',
              name: '毛利率(折线)',
              scale: true,
              splitLine: {show: false},
              axisLine: {show: false},
              axisTick: {show: false},
              show: true
            }],
          series: [{
            name: '新凤鸣', type: 'line', smooth: true, seriesLayoutBy: 'row', symbolSize: 5,
            itemStyle: {normal: {color: colors[0]},},
          },
            {
              name: '桐昆', type: 'line', smooth: true, seriesLayoutBy: 'row', symbolSize: 5,
              itemStyle: {color: colors[1]},
            },
            {
              name: '恒力', type: 'line', smooth: true, seriesLayoutBy: 'row', symbolSize: 5,
              itemStyle: {color: colors[2]},
            },
            {
              name: '新凤鸣', type: 'bar', yAxisIndex: 1, smooth: true, seriesLayoutBy: 'row', symbolSize: 5,
              itemStyle: {normal: {label: {show: true}, color: colors[0],},},
            },
            {
              name: '桐昆', type: 'bar', yAxisIndex: 1, smooth: true, seriesLayoutBy: 'row', symbolSize: 5,
              itemStyle: {color: colors[1]},
            },
            {
              name: '恒力', type: 'bar', yAxisIndex: 1, smooth: true, seriesLayoutBy: 'row', symbolSize: 5,
              itemStyle: {color: colors[2]},
            },
          ]
        });
      },
      initCharts2() {
        let myCharthr01 = this.$echarts.init(this.$refs.hr01);
        // 绘制图表
        myCharthr01.setOption({
          title: {text: '人员公司分布', textstyle: {fontSize: 15,}},
          tooltip: [{
            trigger: 'item',
            formatter(value) {
              let str = value.value[0] + ":" + value.value[1] + "(" + value.percent + "%)";
              return str
            },
          }],
          dataset: {
            source: [['公司名称', "中辰", "中盈", "中维", "中辰", "中石"],
              ['人数', 335, 310, 234, 135, 1548,]],
          },
          series: [{
            type: 'pie', smooth: true, seriesLayoutBy: 'row',
            itemStyle: {
              normal: {
                color: function (params) {
                  return colors[params.dataIndex]
                }
              },
            },
          }]
        });
      },
      initCharts3() {
        let myChartsc01 = this.$echarts.init(this.$refs.sc01);
        // 绘制图表
        myChartsc01.setOption({
          title: {text: '产量装置分布', textstyle: {fontSize: 15,}},
          grid: [{x: '10%', y: '25%', width: '90%', height: '70%'},],
          tooltip: [{
            trigger: 'axis',
            formatter(value) {
              let str = '';
              value.forEach(item => {
                str += item.value[0] + ":" + item.value[1];
              });
              return str
            },
          }],
          dataset: {
            source: [['装置名称', "ZCP01", "ZCP02", "ZCP03", "ZCP04", "ZCP05", "ZCP06", 'ZCP07', 'ZCP08', 'HCP01',
              'HCP02', 'HCP03', 'HCP04', 'HCP05', 'HCP06'],
              ['产量', 40, 20, 35, 60, 55, 10, 11, 21, 5, 19, 28, 4, 9, 111]],
          },
          xAxis: {
            data: ["ZCP01", "ZCP02", "ZCP03", "ZCP04", "ZCP05", "ZCP06", 'ZCP07', 'ZCP08', 'HCP01',
              'HCP02', 'HCP03', 'HCP04', 'HCP05', 'HCP06'],
            show: true,
            axisTick: {show: false},
            axisLine: {show: false},
          },
          yAxis: [{scale: true, splitLine: {show: false}, show: false}],
          series: [{
            name: '产量', type: 'line', smooth: true, seriesLayoutBy: 'row',
            itemStyle: {normal: {label: {show: true}, color: colors[0]}},
          }]
        });
      }
    },
    mounted() {
      this.initCharts();
      this.initCharts2();
      this.initCharts3();
      //实现自适应
      this.resizefun = () => {
        this.$echarts.init(this.$refs.fi01).resize();
        this.$echarts.init(this.$refs.hr01).resize();
        this.$echarts.init(this.$refs.sc01).resize();
      };
      window.addEventListener('resize', this.resizefun);
    },
    //移除事件监听，避免内存泄漏
    beforeDestroy() {
      window.removeEventListener('resize', this.resizefun)
      this.resizefun = null
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
