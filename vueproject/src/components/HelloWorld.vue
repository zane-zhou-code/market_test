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
          <sui-segment id="0" class="columnstyle" @mouseenter="seen_enter($event)" @mouseleave="seen_leave($event)">
            <a class="compact downimgfi" v-show="seen[0].seen_val"
               @click="saveimage('dbfi01', '财务分析')">
              <sui-button class="downimg_buttom" animated="" tab-index="0">
                <sui-button-content class="downimg_buttom" visible>
                  <i class="caret square large down icon grey"></i>
                </sui-button-content>
                <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
              </sui-button>
            </a>
            <div ref='dbfi01'>
              <sui-grid :columns="2" centered>
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <h3 is="sui-header">财务分析</h3>
                  </sui-grid-column>
                </sui-grid-row>
                <!--利润 毛利-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a>
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating style="left:50%">万</sui-label>
                        <sui-list-item>
                          <sui-label color="grey" horizontal>利润</sui-label>
                          <sui-button class="dashboard_buttom">
                            <count-to :startVal='0' :endVal='13048' :duration='2500'></count-to>
                          </sui-button>
                        </sui-list-item>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a>
                      <div slot="label">
                        <sui-label circular color="teal" size="tiny" floating style="left:50%">
                          <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-list-item>
                          <sui-label color="grey" horizontal>毛利</sui-label>
                          <sui-button class="dashboard_buttom">2.85%</sui-button>
                        </sui-list-item>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
                <!--季度公告利润 毛利-->
                <sui-grid-row>
                  <sui-grid-column vertical-align="middle">
                    <a>
                      <div slot="label">
                        <sui-label circular color="red" size="tiny" floating style="left:50%">万</sui-label>
                        <sui-list-item>
                          <sui-label color="grey" horizontal>季度利润</sui-label>
                          <sui-button class="dashboard_buttom">
                            <count-to :startVal='0' :endVal='53048' :duration='2500'></count-to>
                          </sui-button>
                        </sui-list-item>
                      </div>
                    </a>
                  </sui-grid-column>
                  <sui-grid-column vertical-align="middle">
                    <a>
                      <div slot="label">
                        <sui-label circular color="teal" size="tiny" floating style="left:50%">
                          <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                        </sui-label>
                        <sui-list-item>
                          <sui-label color="grey" horizontal>季度毛利</sui-label>
                          <sui-button class="dashboard_buttom">5.85%</sui-button>
                        </sui-list-item>
                      </div>
                    </a>
                  </sui-grid-column>
                </sui-grid-row>
              </sui-grid>
            </div>
          </sui-segment>
          <!--          </div>-->
        </sui-grid-column>
        <sui-grid-column>
          <!--fi01图-->
          <sui-segment id="1" class="columnstyle" v-on:mouseenter="seen_enter($event)"
                       v-on:mouseleave="seen_leave($event)">
            <a class="compact downimgfi" v-show="seen[1].seen_val"
               @click="saveimage('fi01', '同类公司财务分析')">
              <sui-button class="downimg_buttom" animated="" tab-index="0">
                <sui-button-content class="downimg_buttom" visible>
                  <i class="caret square large down icon grey"></i>
                </sui-button-content>
                <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
              </sui-button>
            </a>
            <div ref="fi01" style="width: 100%;height: 150px;"></div>
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
            <sui-segment id='2' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[2].seen_val"
                 @click="saveimage('dbsd01', '销售情况')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref='dbsd01'>
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">销售情况</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 销量/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>销量</sui-label>
                            <sui-button class="dashboard_buttom">{{ data1['dbsd01_sales'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="teal" size="tiny" floating style="left:50%">
                            <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">{{ data1['dbsd01_salesyoy'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 金额/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">万</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>金额</sui-label>
                            <sui-button class="dashboard_buttom">{{ data1['dbsd01_money'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">
                            <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">{{ data1['dbsd01_moneyyoy'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 均价/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">¥/T</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>均价</sui-label>
                            <sui-button class="dashboard_buttom">{{ data1['dbsd01_price'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">
                            <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">{{ data1['dbsd01_priceyoy'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
          <!--总览 人力-->
          <sui-grid-column id="hrcol">
            <sui-segment id='3' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[3].seen_val"
                 @click="saveimage('dbhr01', '人力概览')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref='dbhr01'>
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">人员概览</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--人力 总人数/公司占比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-list-item>
                            <sui-label color="grey" horizontal>总数</sui-label>
                            <sui-button class="dashboard_buttom">{{ data2['dbhr01_amount'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--hr01图-->
                  <sui-grid-row>
                    <div ref="hr01" style="width: 100%;height: 150px;"></div>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
          <!--总览 生产-->
          <sui-grid-column id="sccol">
            <sui-segment id='4' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[4].seen_val"
                 @click="saveimage('dbsc01', '生产规模')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref="dbsc01">
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column>
                      <h3 is="sui-header">生产规模</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--生产 产量/装置分布-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-list-item>
                            <sui-label color="grey" horizontal>产量</sui-label>
                            <sui-button class="dashboard_buttom">{{ data3['dbsc01_product'] }}</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--sc01图-->
                  <sui-grid-row>
                    <div ref="sc01" style="width: 100%;height: 150px;"></div>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
          <!--总览 库存-->
          <sui-grid-column id="mmcol">
            <sui-segment id='5' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[5].seen_val"
                 @click="saveimage('dbmm01', '库存分布')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref="dbmm01">
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">库存分布</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--库存 内外贸库存-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>内贸成品</sui-label>
                            <sui-button class="dashboard_buttom">18,048</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>外贸成品</sui-label>
                            <sui-button class="dashboard_buttom">15,048</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--库存 库存天数-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">天</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>库存天数</sui-label>
                            <sui-button class="dashboard_buttom">17.52</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>PTA</sui-label>
                            <sui-button class="dashboard_buttom">98,580</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>MEG</sui-label>
                            <sui-button class="dashboard_buttom">8,580</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
        </sui-grid-row>
        <!--安全 物资 质量 信息-->
        <sui-grid-row>
          <!--总览 安全-->
          <sui-grid-column id="aqcol">
            <sui-segment id='6' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[6].seen_val"
                 @click="saveimage('dbaq01', '安全状况')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref="dbaq01">
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">安全状况</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 销量/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>销量</sui-label>
                            <sui-button class="dashboard_buttom">2,048</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="teal" size="tiny" floating style="left:50%">
                            <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">2.85%</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 金额/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">万</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>金额</sui-label>
                            <sui-button class="dashboard_buttom">3,052</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">
                            <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">3.85%</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 均价/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">¥/T</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>均价</sui-label>
                            <sui-button class="dashboard_buttom">580</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">
                            <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">3.85%</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
          <!--总览 物资-->
          <sui-grid-column id="wzcol">
            <sui-segment id='7' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[7].seen_val"
                 @click="saveimage('dbwz01', '物资采购')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref="dbwz01">
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">物资采购</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--物资 采购总量-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>总量</sui-label>
                            <sui-button class="dashboard_buttom">12,048</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--物资 供应商分布-->
                  <sui-divider></sui-divider>
                  <sui-grid-row>

                    <sui-segments>
                      <sui-table aligned="left" class="segment" celled striped collapsing>
                        <!--表头-->
                        <sui-table-header>
                          <sui-table-row>
                            <sui-table-header-cell>供应商</sui-table-header-cell>
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
                            <sui-table-cell>10000</sui-table-cell>
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
                            <sui-table-cell>52000</sui-table-cell>
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
                            <sui-table-cell>9800</sui-table-cell>
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
              </div>
            </sui-segment>
          </sui-grid-column>
          <!--总览 质量-->
          <sui-grid-column id="qmcol">
            <sui-segment id='8' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[8].seen_val"
                 @click="saveimage('dbqm01', '质量中心')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref="dbqm01">
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">质量中心</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 销量/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>销量</sui-label>
                            <sui-button class="dashboard_buttom">2,048</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="teal" size="tiny" floating style="left:50%">
                            <i class="arrow down icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">2.85%</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 金额/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">万</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>金额</sui-label>
                            <sui-button class="dashboard_buttom">3,052</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">
                            <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">3.85%</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--销售 均价/同比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">¥/T</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>均价</sui-label>
                            <sui-button class="dashboard_buttom">580</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">
                            <i class="arrow up icon" style="margin: 0.25em 0 0"></i>
                          </sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>同比</sui-label>
                            <sui-button class="dashboard_buttom">3.85%</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
          <!--总览 信息-->
          <sui-grid-column id="ifcol">
            <sui-segment id='9' class="columnstyle" v-on:mouseenter="seen_enter($event)"
                         v-on:mouseleave="seen_leave($event)">
              <a class="compact downimg" v-show="seen[9].seen_val"
                 @click="saveimage('dbif01', '信息管理')">
                <sui-button class="downimg_buttom" animated="" tab-index="0">
                  <sui-button-content class="downimg_buttom" visible>
                    <i class="caret square large down icon grey"></i>
                  </sui-button-content>
                  <sui-button-content class="downimg_buttom" hidden>下载</sui-button-content>
                </sui-button>
              </a>
              <div ref="dbif01">
                <sui-grid :columns="2" centered>
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <h3 is="sui-header">信息管理</h3>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--人力 总人数/公司占比-->
                  <sui-grid-row>
                    <sui-grid-column vertical-align="middle">
                      <a>
                        <div slot="label">
                          <sui-label circular color="red" size="tiny" floating style="left:50%">吨</sui-label>
                          <sui-list-item>
                            <sui-label color="grey" horizontal>总数</sui-label>
                            <sui-button class="dashboard_buttom">12,048</sui-button>
                          </sui-list-item>
                        </div>
                      </a>
                    </sui-grid-column>
                  </sui-grid-row>
                  <!--if01图-->
                  <sui-grid-row>
                    <div ref="if01" style="width: 100%;height: 150px;"></div>
                  </sui-grid-row>
                </sui-grid>
              </div>
            </sui-segment>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
    </sui-container>
  </div>

</template>

<script>
  import countTo from 'vue-count-to'
  import html2canvas from "html2canvas";
  import {saveImage} from "../style/demo1";

  const colors = ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf', '#9192ab', '#7898e1',
    '#efa666', '#eddd86', '#9987ce', '#63b2ee', '#76da91'];
  export default {
    name: 'HelloWorld',
    components: {countTo},
    data() {
      return {
        //定义十个seen参数
        seen: [{seen_val: false}, {seen_val: false}, {seen_val: false}, {seen_val: false}, {seen_val: false},
          {seen_val: false}, {seen_val: false}, {seen_val: false}, {seen_val: false}, {seen_val: false}],
        data1: [{}],
        data2: [{}],
        data3: [{}]
      }
    },
    created() {
      this.$axios.get('/dashboard/overallviewsd').then(
        response => {
          this.data1 = response.data
        });
    },
    methods: {
      //定义移入移出函数
      seen_enter(e) {
        let id = e.currentTarget.id;
        this.seen[id].seen_val = true;
      },
      seen_leave(e) {
        let id = e.currentTarget.id;
        this.seen[id].seen_val = false;
      },
      //定义保存图片函数
      saveimage: function (divText, imgText) {
        saveImage(divText, imgText)
      },
      initCharts() {
        let myChartfi01 = this.$echarts.init(this.$refs.fi01);
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
          grid: [{x: '7%', y: '40%', width: '86%', height: '48%'}],
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
        const optionhr = {
          title: {text: '人员公司分布', textstyle: {fontSize: 15,}},
          tooltip: [{
            trigger: 'item',
            formatter(value) {
              let str = value.value[0] + ":" + value.value[1] + "(" + value.percent + "%)";
              return str
            },
          }],
          dataset: {source: []},
          series: [{
            type: 'pie', smooth: true, seriesLayoutBy: 'row', center:['50%', '60%'],
            itemStyle: {
              normal: {
                color: function (params) {
                  return colors[params.dataIndex]
                }
              },
            },
          }]
        };
        myCharthr01.showLoading({
          text: 'loading',
          color: '#f2711c',
          textColor: '#000',
          maskColor: 'rgba(255, 255, 255, 0.7)',
        });
        myCharthr01.setOption(optionhr);
        this.$axios.get('/dashboard/overallviewhr').then(
          response => {
            this.data2 = response.data;
            optionhr.dataset.source = [this.data2['dbhr01_bukrs']
              , this.data2['dbhr01_bukrs_amonut']];
            myCharthr01.hideLoading();
            myCharthr01.setOption(optionhr, true)
          })
      },
      initCharts3() {
        let myChartsc01 = this.$echarts.init(this.$refs.sc01);
        // 绘制图表
        var optionsc = {
          title: {text: '产量装置分布', textstyle: {fontSize: 15,}},
          grid: [{x: '5%', y: '25%', width: '90%', height: '70%'},],
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
          dataset: {source: [],},
          xAxis: {
            data: [],
            show: true,
            axisTick: {show: false},
            axisLine: {show: false},
          },
          yAxis: [{scale: true, splitLine: {show: false}, show: false}],
          series: [{
            name: '产量', type: 'line', smooth: true, seriesLayoutBy: 'row',
            itemStyle: {normal: {label: {show: true}, color: colors[0]}},
          }]
        };
        myChartsc01.showLoading({
          text: 'loading',
          color: '#f2711c',
          textColor: '#000',
          maskColor: 'rgba(255, 255, 255, 0.7)',
        });
        myChartsc01.setOption(optionsc);
        this.$axios.get('/dashboard/overallviewsc').then(
          response => {
            this.data3 = response.data;
            optionsc.dataset.source = [this.data3['dbsc01_zzh']
              , this.data3['dbsc01_zzh_product']];
            optionsc.xAxis.data = this.data3['dbsc01_zzho'];
            myChartsc01.hideLoading();
            myChartsc01.setOption(optionsc, true)
          })
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
      //定义给window定义this和canvas函数
      window.this = this;
      window.html2canvas = html2canvas;
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
