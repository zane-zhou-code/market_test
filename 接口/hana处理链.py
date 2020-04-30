from 接口.setting import get_connection,sql,fixed_params

def main():
    # 定义hana连接
    conn = get_connection().hana_connection()
    today = fixed_params().today
    yesterday = fixed_params().yesterday
    # 原料库存
    sel_sql1 = '''
    select distinct bukrs,gsjc,erdat,kc,wljc,licha
    from(select bukrs,
           gsjc,--公司简称
           '%s' as erdat,--日期
           (kc+ykc)as kc,--库存
           case when wllx='60018629'then 'MEG'
                when wllx='60018628'then 'PTA'end as wljc,--物料简称
           licha--批号描述
    from(select m.wllx,
                m.werks,
                t.gsjc,
                t.bukrs,
                m.charg,
                m.kc,--上月库存
                ifnull(n.kc,0)as ykc,--当月库存
                m.maktx,--物料描述
                m.licha--批号描述
    from(select distinct wllx,--物料类型	
           werks,--工厂
           charg,--批号
           year,--年
           month,--月
           kc,--库存
           maktx,--物料描述
           licha--批号描述
    from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.MM/HMXFMMM09"
    where year=left(to_char(add_months('%s',-1),'yyyymm'),4)
    and month=right(to_char(add_months('%s',-1),'yyyymm'),2)
    and charg<>'FHCHUANG')m
    left join
    (select wllx,--物料类型	
           werks,--工厂
           charg,--批号
           sum(kc)as kc--库存
    from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.MM/HMXFMMM10"
    where erdat between left('%s',6)||'01' and '%s'
    group by wllx,--物料类型	
           werks,--工厂
           charg--批号
        )n
    on m.wllx=n.wllx
    and m.werks=n.werks
    and m.charg=n.charg
    left join
    (select distinct gsjc,--公司简称
                    gc,--工厂
                    bukrs
    from"COMMON"."XFMPM_CJLX"
    union all
    select distinct'集团总公司'as gsjc,
           'HQM1'as gc,
           '1000'as bukrs
    from"COMMON"."XFMPM_CJLX")t
    on m.werks=t.gc))where kc<>0
    '''
    del_sql1 = '''delete from"COMMON"."XFMMM_KC"where erdat='%s' '''
    ins_sql1 = '''insert into"COMMON"."XFMMM_KC"values('%s','%s','%s',%s,'%s','%s')'''
    # PTA,PX库存
    sel_sql2 = '''
    select to_char(add_days('%s',-1),'yyyymmdd') as erdat,'PTA'as lx,round(sum(zcl/1000),2)as kc from(
    select budat,sum(stock_qty)as zcl
    from"_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.MM/MATDOC"
    where werks='DSC1'
    and bwart in('101','102','601','602')
    and budat between '20191101'and to_char(add_days('%s',-1),'yyyymmdd')
    group by budat
    order by budat)
    union all
    select to_char(add_days('%s',-1),'yyyymmdd') as erdat,'PX'as lx,round(sum(zcl/1000),2)as kc from(
    select budat,sum(stock_qty)as zcl
    from"_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.MM/MATDOC"
    where werks='DSM1'
    and right(matnr,8)='60053974'
    and left(lgort,1)<>'C'
    and budat <= to_char(add_days('%s',-1),'yyyymmdd')
    group by budat
    order by budat)
    '''
    ins_sql2 = '''insert into"COMMON"."XFMSC_CLKC"values('%s','%s',%s)'''
    # 取PTA负荷
    sel_sql3 = '''
    select '%s'as erdat,instr_vad_val as fh
    from"XFMMES30"."IF_INSTRDATA_T"
    where instr_id='26200193'
    and read_time in(select max(read_time)
    from"XFMMES30"."IF_INSTRDATA_T"
    where instr_id='26200193'
    and to_char(read_time,'yyyymmdd')<='%s'
    and instr_vad_val<>0)
    '''
    del_sql3 = '''delete from"COMMON"."XFM_PTA_FH"where erdat='%s' '''
    ins_sql3 = '''insert into"COMMON"."XFM_PTA_FH"values(%s,%s)'''
    # 生产管理报表大屏展示
    sel_sql4 = '''
        select '%s' as erdat,'%s' as crrq,'产量总览'as zb,'日计划'as ms,' 'as mx,zcl as sl1,rjh as sl2
        from(
        select round(sum(sl),2)as zcl,--总产量
               sum(clrjh)as rjh--日计划
        from(select distinct calday,xcxmc,clrjh,sum(sl)as sl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC05"
        group by calday,xcxmc,clrjh)
        where calday= '%s')
        union all
        select left('%s',6) as erdat,'%s' as crrq,'产量总览'as zb,'月计划'as ms,' 'as mx,zcl as sl1,yjh as sl2
        from(
        select round(sum(sl),2)as zcl,--总产量
               sum(clyjh) as yjh--月计划
        from(select distinct left(calday,6)as calmonth,xcxmc,clyjh,sum(sl)as sl	   
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC05"
        where calday between left('%s',6)||'01'and '%s'
        group by left(calday,6),xcxmc,clyjh)
        )
        union all
        select left('%s',4) as erdat,'%s' as crrq,'产量总览'as zb,'年计划'as ms,' 'as mx,zcl as sl1,njh as sl2
        from(
        select round(sum(sl),2)as zcl,--总产量
               sum(clnjh) as njh--年计划
        from(select distinct left(calday,4)as calyear,xcxmc,clnjh,sum(sl)as sl	   
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC05"
        where calday between left('%s',4)||'0101'and '%s'
        group by left(calday,4),xcxmc,clnjh)
        )
        union all
        select '%s' as erdat,'%s' as crrq,'公司间产量日对比'as zb,gsjc as ms,' 'as mx,cl as sl1,0 as sl2
        from(
        select gsjc,--公司简称
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by gsjc
        )
        union all
        select left('%s',6)as erdat,'%s' as crrq,'公司间产量月对比'as zb,gsjc as ms,' 'as mx,cl as sl1,0 as sl2
        from(
        select gsjc,--公司简称
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by gsjc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'装置间产量日对比'as zb,xcxmc as ms,' 'as mx,cl as sl1,0 as sl2
        from(
        select xcxmc,--装置号
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by xcxmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置间产量月对比'as zb,xcxmc as ms,' 'as mx,cl as sl1,0 as sl2
        from(
        select xcxmc,--装置号
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'产品类别日占比'as zb,wplx as ms,' 'as mx,zb as sl1,0 as sl2
        from(
        select wplx,--物品类型
               round(sum(sl)/zsl,3)as zb--占比
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s')
        where bzrq='%s'
        group by wplx,zsl
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'产品类别月占比'as zb,wplx as ms,' 'as mx,zb as sl1,0 as sl2
        from(
        select wplx,--物品类型
               round(sum(sl)/zsl,3)as zb--占比
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s')
        where bzrq between left('%s',6)||'01'and '%s'
        group by wplx,zsl
        )
        -------------------------------------------------------------------------------------------------------------产量（总览）
        union all
        select '%s' as erdat,'%s' as crrq,'公司产量日占比'as zb,gsjc as ms,' 'as mx,zb as sl1,0 as sl2
        from(
        select gsjc,--公司简称
               round(sum(sl)/zsl,3)as zb--占比
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s')
        where bzrq='%s'
        group by gsjc,zsl
        )
        union all
        select left('%s',6)as erdat,'%s' as crrq,'公司产量月占比'as zb,gsjc as ms,' 'as mx,zb as sl1,0 as sl2
        from(
        select gsjc,--公司简称
               round(sum(sl)/zsl,3)as zb--占比
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s')
        where bzrq between left('%s',6)||'01'and '%s'
        group by gsjc,zsl
        )
        union all
        select '%s' as erdat,'%s' as crrq,'单公司产品日占比'as zb,gsjc as ms,wplx as mx,cl as sl1,0 as sl2
        from(
        select gsjc,
               wplx,--公司简称
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by gsjc,wplx
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'单公司产品月占比'as zb,gsjc as ms,wplx as mx,cl as sl1,0 as sl2
        from(
        select gsjc,
               wplx,--公司简称
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by gsjc,wplx
        )
        union all
        select '%s' as erdat,'%s' as crrq,'公司日同环比'as zb,gsjc as ms,' 'as mx,hb as sl1,tb as sl2
        from(
        select a.gsjc,
               case when ifnull(b.cl,0)=0 then 1
               else round((a.cl-b.cl)/b.cl,3)end as hb,--环比
               case when ifnull(c.cl,0)=0 then 1
               else round((a.cl-c.cl)/c.cl,3)end as tb--同比
        from(
        select gsjc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by gsjc)a,
        (
        select gsjc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq=to_char(add_months('%s',-1),'yyyymmdd')
        group by gsjc)b,
        (select gsjc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq=to_char(add_years('%s',-1),'yyyymmdd')
        group by gsjc)c
        where a.gsjc=b.gsjc
        and a.gsjc=c.gsjc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'公司月同环比'as zb,gsjc as ms,' 'as mx,hb as sl1,tb as sl2
        from(
        select a.gsjc,
               case when ifnull(b.cl,0)=0 then 1
               else round((a.cl-b.cl)/b.cl,3)end as hb,--环比
               case when ifnull(c.cl,0)=0 then 1
               else round((a.cl-c.cl)/c.cl,3)end as tb--同比
        from(
        select gsjc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by gsjc)a,
        (
        select gsjc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left(to_char(add_months('%s',-1),'yyyymmdd'),6)||'01'and to_char(add_months('%s',-1),'yyyymmdd')
        group by gsjc)b,
        (select gsjc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left(to_char(add_years('%s',-1),'yyyymmdd'),6)||'01'and to_char(add_years('%s',-1),'yyyymmdd')
        group by gsjc)c
        where a.gsjc=b.gsjc
        and a.gsjc=c.gsjc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单公司产量日趋势'as zb,gsjc as ms,' 'as mx,cl as sl1,dqfh as sl2
        from(
        select bzrq, --日期
               a.gsjc,
               round(sum(sl),2)as cl,--产量
               round(dqfh,2)as dqfh--当前负荷
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"a,
            (select gsjc,sum(dqfh)as dqfh from"COMMON"."XFMSC_DQFH"group by gsjc)b
        where a.gsjc=b.gsjc
        and bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,dqfh,a.gsjc
        order by bzrq
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单公司产量月趋势'as zb,gsjc as ms,' 'as mx,cl as sl1,dqfh as sl2
        from(
        select left(bzrq,6)as bzrq, --月
               a.gsjc,
               round(sum(sl),2)as cl,--产量
               round(dqfh,2)as dqfh--当前负荷
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"a,
            (select gsjc,sum(dqfh)as dqfh from"COMMON"."XFMSC_DQFH"group by gsjc)b
        where a.gsjc=b.gsjc
        and bzrq between left(to_char(add_years('%s',-1),'yyyymmdd'),6)||'01'and '%s'
        group by left(bzrq,6),dqfh,a.gsjc
        )
        -----------------------------------------------------------------------------------------------------------产量（公司间）
        union all
        select '%s' as erdat,'%s' as crrq,'装置产量日占比'as zb,xcxmc as ms,' 'as mx,zb as sl1,0 as sl2
        from(
        select xcxmc,--装置名称
               round(sum(sl)/zsl,3)as zb
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s')
        where bzrq='%s'
        group by xcxmc,zsl
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置产量月占比'as zb,xcxmc as ms,' 'as mx,zb as sl1,0 as sl2
        from(
        select xcxmc,--装置名称
               round(sum(sl)/zsl,3)as zb
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s')
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zsl
        )
        union all
        select '%s' as erdat,'%s' as crrq,'单装置产量日占比'as zb,xcxmc as ms,wplx as mx,cl as sl1,0 as sl2
        from(
        select wplx,--物品类型
               xcxmc,
               round(sum(sl),2)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by wplx,xcxmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'单装置产量月占比'as zb,xcxmc as ms,wplx as mx,cl as sl1,0 as sl2
        from(
        select wplx,--物品类型
               xcxmc,
               round(sum(sl),2)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by wplx,xcxmc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'单装置日同环比'as zb,xcxmc as ms,' 'as mx,hb as sl1,tb as sl2
        from(
        select a.xcxmc,
               case when ifnull(b.cl,0)=0 then 1
               else round((a.cl-b.cl)/b.cl,3)end as hb,--环比
               case when ifnull(c.cl,0)=0 then 1
               else round((a.cl-c.cl)/c.cl,3)end as tb--同比
        from(
        select xcxmc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by xcxmc)a,
        (
        select xcxmc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq=to_char(add_months('%s',-1),'yyyymmdd')
        group by xcxmc)b,
        (select xcxmc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq=to_char(add_years('%s',-1),'yyyymmdd')
        group by xcxmc)c
        where a.xcxmc=b.xcxmc
        and a.xcxmc=c.xcxmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'单装置月同环比'as zb,xcxmc as ms,' 'as mx,hb as sl1,tb as sl2
        from(
        select a.xcxmc,
               case when ifnull(b.cl,0)=0 then 1
               else round((a.cl-b.cl)/b.cl,3)end as hb,--环比
               case when ifnull(c.cl,0)=0 then 1
               else round((a.cl-c.cl)/c.cl,3)end as tb--同比
        from(
        select xcxmc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc)a,
        (
        select xcxmc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left(to_char(add_months('%s',-1),'yyyymmdd'),6)||'01'and to_char(add_months('%s',-1),'yyyymmdd')
        group by xcxmc)b,
        (select xcxmc,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left(to_char(add_years('%s',-1),'yyyymmdd'),6)||'01'and to_char(add_years('%s',-1),'yyyymmdd')
        group by xcxmc)c
        where a.xcxmc=b.xcxmc
        and a.xcxmc=c.xcxmc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置产量日趋势'as zb,xcxmc as ms,' 'as mx,cl as sl1,dqfh as sl2
        from(
        select bzrq, --日期
               a.xcxmc,
               round(sum(sl),2)as cl,--产量
               round(dqfh,2)as dqfh--当前负荷
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"a,
            (select cxmc,sum(dqfh)as dqfh from"COMMON"."XFMSC_DQFH"group by cxmc)b
        where a.xcxmc=b.cxmc
        and bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,dqfh,a.xcxmc
        order by bzrq
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置产量月趋势'as zb,xcxmc as ms,' 'as mx,cl as sl1,dqfh as sl2
        from(
        select left(bzrq,6)as bzrq, --月
               a.xcxmc,
               round(sum(sl),2)as cl,--产量
               round(dqfh,2)as dqfh--当前负荷
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"a,
            (select cxmc,sum(dqfh)as dqfh from"COMMON"."XFMSC_DQFH"group by cxmc)b
        where a.xcxmc=b.cxmc
        and bzrq between left(to_char(add_years('%s',-1),'yyyymmdd'),6)||'01'and '%s'
        group by left(bzrq,6),dqfh,a.xcxmc
        )
        -----------------------------------------------------------------------------------------------------------产量（装置间）
        union all
        select '%s' as erdat,'%s' as crrq,'产品大类别日占比'as zb,wplx as ms,' 'as mx,zb as sl1,cl as sl2
        from(
        select wplx,--物品类型
               round(sum(sl)/zsl,3)as zb,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s')
        where bzrq='%s'
        group by wplx,zsl
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'产品大类别月占比'as zb,wplx as ms,' 'as mx,zb as sl1,cl as sl2
        from(
        select wplx,--物品类型
               round(sum(sl)/zsl,3)as zb,sum(sl)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01",
        (select sum(sl)as zsl from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s')
        where bzrq between left('%s',6)||'01'and '%s'
        group by wplx,zsl
        )
        union all
        select '%s' as erdat,'%s' as crrq,'单产品装置日分布'as zb,wplx as ms,xcxmc as mx,cl as sl1,0 as sl2
        from(
        select wplx,--物品类型
               xcxmc,
               round(sum(sl),2)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq='%s'
        group by wplx,xcxmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'单产品装置月分布'as zb,wplx as ms,xcxmc as mx,cl as sl1,0 as sl2
        from(
        select wplx,--物品类型
               xcxmc,
               round(sum(sl),2)as cl
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between left('%s',6)||'01'and '%s'
        group by wplx,xcxmc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单产品产量日趋势'as zb,wplx as ms,' 'as mx,cl as sl1,0 as sl2
        from(
        select bzrq, --日期
               wplx,
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,wplx
        order by bzrq
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单产品产量月趋势'as zb,wplx as ms,' 'as mx,cl as sl1,0 as sl2
        from(
        select left(bzrq,6)as bzrq, --月
               wplx,
               round(sum(sl),2)as cl--产量
        from"_SYS_BIC"."DASHBOARD_XFM.02_LOGICAL_LAYER.SC/HCXFMSC01"
        where bzrq between to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6),wplx
        )
        union all
        select '%s' as erdat,'%s' as crrq,'产品品种描述日占比'as zb,wplx as ms,wpmc as mx,zb as sl1,0 as sl2
        from(
        select a.wpmc,a.wplx,round(sum(sl/1000)/zsl,3)as zb
        from"_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SC/HCXFMSC09"a,
        (select wplx,sum(sl/1000)as zsl from"_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SC/HCXFMSC09"
        where bzrq='%s'group by wplx)b
        where a.wplx=b.wplx
        and bzrq='%s'
        group by wpmc,a.wplx,zsl
        )
        union all
        select left('%s',6)as erdat,'%s' as crrq,'产品品种描述月占比'as zb,wplx as ms,wpmc as mx,zb as sl1,0 as sl2
        from(
        select a.wpmc,a.wplx,round(sum(sl/1000)/zsl,3)as zb
        from"_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SC/HCXFMSC09"a,
        (select wplx,sum(sl/1000)as zsl from"_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SC/HCXFMSC09"
        where bzrq between left('%s',6)||'01'and '%s'group by wplx)b
        where bzrq between left('%s',6)||'01'and '%s'
        and a.wplx=b.wplx
        group by wpmc,a.wplx,zsl
        )
        ----------------------------------------------------------------------------------------------------------产量（产品大类）
        union all
        select '%s' as erdat,'%s' as crrq,'日优等率总览'as zb,wplx as ms,' 'as mx,ydl as sl1,khz as sl2
        from(
        select wplx,round(sum(ydsl)/sum(sl),4)as ydl,
               case when wplx='POY'then poy 
                    when wplx='FDY'then fdy
                    when wplx='DTY'then dty end as khz
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07",
        (select round(avg(case when poyudjh=0 then null else poyudjh end)/100,3)as poy,
                round(avg(case when fdyudjh=0 then null else fdyudjh end)/100,3)as fdy,
                round(avg(case when dtyudjh=0 then null else dtyudjh end)/100,3)as dty
        from"COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where bzrq='%s'
        group by wplx,poy,dty,fdy
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'月优等率总览'as zb,wplx as ms,' 'as mx,ydl as sl1,khz as sl2
        from(
        select wplx,round(sum(ydsl)/sum(sl),4)as ydl,
               case when wplx='POY'then poy 
                    when wplx='FDY'then fdy
                    when wplx='DTY'then dty end as khz
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07",
        (select round(avg(case when poyudjh=0 then null else poyudjh end)/100,3)as poy,
                round(avg(case when fdyudjh=0 then null else fdyudjh end)/100,3)as fdy,
                round(avg(case when dtyudjh=0 then null else dtyudjh end)/100,3)as dty
        from"COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where bzrq between left('%s',6)||'01'and '%s'
        group by wplx,poy,dty,fdy
        )
        union all
        select left('%s',4) as erdat,'%s' as crrq,'年优等率总览'as zb,wplx as ms,' 'as mx,ydl as sl1,khz as sl2
        from(
        select wplx,round(sum(ydsl)/sum(sl),4)as ydl,
               case when wplx='POY'then poy 
                    when wplx='FDY'then fdy
                    when wplx='DTY'then dty end as khz
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07",
        (select round(avg(case when poyudjh=0 then null else poyudjh end)/100,3)as poy,
                round(avg(case when fdyudjh=0 then null else fdyudjh end)/100,3)as fdy,
                round(avg(case when dtyudjh=0 then null else dtyudjh end)/100,3)as dty
        from"COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where bzrq between left('%s',4)||'0101'and '%s'
        group by wplx,poy,dty,fdy
        )
        union all
        select '%s' as erdat,'%s' as crrq,'品种日产销率'as zb,wplx as ms,' 'as mx,zcxl as sl1,0 as sl2
        from(
        select b.wplx,round((a.zxl)/(b.zcl),4) as zcxl 
        from(select zeiar,sum(zsum/1000) as zxl
        from  "_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SD/HCXFMSD02"
        where erdat='%s'
        group by zeiar)a,
        (select wplx,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq=to_char(add_days('%s',-1),'yyyymmdd')
        group by wplx)b
        where a.zeiar=b.wplx
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'品种月产销率'as zb,wplx as ms,' 'as mx,zcxl as sl1,0 as sl2
        from(
        select b.wplx,round((a.zxl)/(b.zcl),4) as zcxl 
        from(select zeiar,sum(zsum/1000) as zxl
        from  "_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SD/HCXFMSD02"
        where erdat between left('%s',6)||'01'and '%s'
        group by zeiar)a,
        (select wplx,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'          
        group by wplx)b
        where a.zeiar=b.wplx
        )
        union all
        select '%s' as erdat,'%s' as crrq,'品种日废丝'as zb,wplx as ms,' 'as mx,fs as sl1,fsl as sl2
        from(
        select wplx, --物品类型
        sum(fs) as fs, --废丝量
        round(sum(fs)/sum(sl),4) as fsl --废丝率
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by wplx 
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'品种月废丝'as zb,wplx as ms,' 'as mx,fs as sl1,fsl as sl2
        from(
        select wplx, --物品类型
        sum(fs) as fs, --废丝量
        round(sum(fs)/sum(sl),4) as fsl --废丝率
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by wplx 
        )
        union all
        select '%s' as erdat,'%s' as crrq,'吨飘丝断头日趋势'as zb,bzrq as ms,' 'as mx,ps as sl1,dt as sl2
        from(
        select bzrq,
               round(sum(ps)/sum(sl),4) as ps,--飘丝
               round(sum(dt)/sum(sl),4)as dt--断头
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between  to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'吨飘丝断头月趋势'as zb,bzrq as ms,' 'as mx,ps as sl1,dt as sl2
        from(
        select left(bzrq,6)as bzrq,
               round(sum(ps)/sum(sl),4) as ps,--飘丝
               round(sum(dt)/sum(sl),4)as dt--断头
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between  to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6)
        )
        union all
        select '%s' as erdat,'%s' as crrq,'单品种日装置间优等率'as zb,wplx as ms,zzh as mx,ydl as sl1,khz as sl2
        from(
        select a.zzh,wplx,a.ydl,
               case when wplx='POY'then poyudjh/100
                    when wplx='FDY'then fdyudjh/100
                    when wplx='DTY'then dtyudjh/100 end as khz
        from (select xcxmc,zzh,wplx,round(sum(ydsl)/sum(sl),3) as ydl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by xcxmc,zzh,wplx)a,
        (select zzmc,poyudjh,fdyudjh,dtyudjh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'单品种月装置间优等率'as zb,wplx as ms,zzh as mx,ydl as sl1,khz as sl2
        from(
        select a.zzh,wplx,a.ydl,
               case when wplx='POY'then poyudjh/100
                    when wplx='FDY'then fdyudjh/100
                    when wplx='DTY'then dtyudjh/100 end as khz
        from (select xcxmc,zzh,wplx,round(sum(ydsl)/sum(sl),3) as ydl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zzh,wplx)a,
        (select zzmc,poyudjh,fdyudjh,dtyudjh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'装置间优等率日分布'as zb,zzh as ms,' ' as mx,ydl as sl1,khz as sl2
        from(
        select a.zzh,a.ydl,pfdudjh/100 as khz
        from (select xcxmc,zzh,round(sum(ydsl)/sum(sl),3) as ydl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by xcxmc,zzh)a,
        (select zzmc,pfdudjh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置间优等率月分布'as zb,zzh as ms,' ' as mx,ydl as sl1,khz as sl2
        from(
        select a.zzh,a.ydl,pfdudjh/100 as khz
        from (select xcxmc,zzh,round(sum(ydsl)/sum(sl),3) as ydl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zzh)a,
        (select zzmc,pfdudjh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置优等率日趋势'as zb,zzh as ms,' ' as mx,ydl as sl1,khz as sl2
        from(
        select a.zzh,bzrq,a.ydl,pfdudjh/100 as khz
        from (select bzrq,xcxmc,zzh,round(sum(ydsl)/sum(sl),3) as ydl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,xcxmc,zzh)a,
        (select zzmc,pfdudjh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置优等率月趋势'as zb,zzh as ms,' ' as mx,ydl as sl1,khz as sl2
        from(
        select a.zzh,bzrq,a.ydl,pfdudjh/100 as khz
        from (select left(bzrq,6)as bzrq,xcxmc,zzh,round(sum(ydsl)/sum(sl),3) as ydl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6),xcxmc,zzh)a,
        (select zzmc,pfdudjh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'单品种日装置间废丝率'as zb,wplx as ms,zzh as mx,fsl as sl1,khz as sl2
        from(
        select a.zzh,wplx,a.fsl,fsljh/100 as khz
        from(select xcxmc,zzh,wplx,round(sum(fs)/sum(sl),3) as fsl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by xcxmc,zzh,wplx)a,
        (select zzmc,fsljh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'单品种月装置间废丝率'as zb,wplx as ms,zzh as mx,fsl as sl1,khz as sl2
        from(
        select a.zzh,wplx,a.fsl,fsljh/100 as khz
        from (select xcxmc,zzh,wplx,round(sum(fs)/sum(sl),3) as fsl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zzh,wplx)a,
        (select zzmc,fsljh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'装置间废丝率日分布'as zb,zzh as ms,' ' as mx,fsl as sl1,khz as sl2
        from(
        select a.zzh,a.fsl,fsljh/100 as khz
        from(select xcxmc,zzh,round(sum(fs)/sum(sl),3) as fsl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by xcxmc,zzh)a,
        (select zzmc,fsljh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置间废丝率月分布'as zb,zzh as ms,' ' as mx,fsl as sl1,khz as sl2
        from(
        select a.zzh,a.fsl,fsljh/100 as khz
        from (select xcxmc,zzh,round(sum(fs)/sum(sl),3) as fsl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zzh)a,
        (select zzmc,fsljh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置废丝率日趋势'as zb,zzh as ms,' ' as mx,fsl as sl1,khz as sl2
        from(
        select a.zzh,bzrq,a.fsl,fsljh/100 as khz
        from (select bzrq,xcxmc,zzh,round(sum(fs)/sum(sl),3) as fsl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,xcxmc,zzh)a,
        (select zzmc,fsljh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置废丝率月趋势'as zb,zzh as ms,' ' as mx,fsl as sl1,khz as sl2
        from(
        select a.zzh,bzrq,a.fsl,fsljh/100 as khz
        from (select left(bzrq,6)as bzrq,xcxmc,zzh,round(sum(fs)/sum(sl),3) as fsl
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6),xcxmc,zzh)a,
        (select zzmc,fsljh from "COMMON"."XFM_KHZB"
        where khrq=left('%s',4))b
        where a.xcxmc=b.zzmc
        )
        union all
        select '%s' as erdat,'%s' as crrq,'装置飘丝断头日分布'as zb,zzh as ms,' ' as mx,ps as sl1,dt as sl2
        from(
        select xcxmc,zzh,sum(ps)as ps,sum(dt)as dt
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by xcxmc,zzh
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置飘丝断头月分布'as zb,zzh as ms,' ' as mx,ps as sl1,dt as sl2
        from(
        select xcxmc,zzh,sum(ps)as ps,sum(dt)as dt
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zzh
        )
        union all
        select '%s' as erdat,'%s' as crrq,'装置切败日分布'as zb,zzh as ms,' ' as mx,qb as sl1,0 as sl2
        from(
        select xcxmc,zzh,sum(zgqb)as qb
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq='%s'
        group by xcxmc,zzh
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置切败月分布'as zb,zzh as ms,' ' as mx,qb as sl1,0 as sl2
        from(
        select xcxmc,zzh,sum(zgqb)as qb
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by xcxmc,zzh
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置断头日趋势'as zb,zzh as ms,' ' as mx,dt as sl1,0 as sl2
        from(
        select bzrq,xcxmc,zzh,sum(dt)as dt
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,xcxmc,zzh
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置断头月趋势'as zb,zzh as ms,' ' as mx,dt as sl1,0 as sl2
        from(
        select left(bzrq,6)as bzrq,xcxmc,zzh,sum(dt)as dt
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6),xcxmc,zzh
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置飘丝日趋势'as zb,zzh as ms,' ' as mx,ps as sl1,0 as sl2
        from(
        select bzrq,xcxmc,zzh,sum(ps)as ps
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,xcxmc,zzh
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置飘丝月趋势'as zb,zzh as ms,' ' as mx,ps as sl1,0 as sl2
        from(
        select left(bzrq,6)as bzrq,xcxmc,zzh,sum(ps)as ps
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6),xcxmc,zzh
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置切败日趋势'as zb,zzh as ms,' ' as mx,dt as sl1,0 as sl2
        from(
        select bzrq,xcxmc,zzh,sum(zgqb)as dt
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_months('%s',-1),'yyyymmdd')and '%s'
        group by bzrq,xcxmc,zzh
        )
        union all
        select bzrq as erdat,'%s' as crrq,'单装置切败月趋势'as zb,zzh as ms,' ' as mx,dt as sl1,0 as sl2
        from(
        select left(bzrq,6)as bzrq,xcxmc,zzh,sum(zgqb)as dt
        from"_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between to_char(add_years('%s',-1),'yyyymmdd')and '%s'
        group by left(bzrq,6),xcxmc,zzh
        )
        union all
        select '%s' as erdat,'%s' as crrq,'品种产销率日分布'as zb,wplx as ms,' 'as mx,zcxl as sl1,hb as sl2
        from(
        select m.wplx,m.zcxl,round((m.zcxl-n.zcxl)/n.zcxl,3) as hb
        from(select b.wplx,round((a.zxl)/(b.zcl),4) as zcxl 
        from(select zeiar,sum(zsum/1000) as zxl
        from  "_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SD/HCXFMSD02"
        where erdat='%s'
        group by zeiar)a,
        (select wplx,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq=to_char(add_days('%s',-1),'yyyymmdd')
        group by wplx)b
        where a.zeiar=b.wplx)m,
        (select b.wplx,round((a.zxl)/(b.zcl),4) as zcxl 
        from(select zeiar,sum(zsum/1000) as zxl
        from  "_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SD/HCXFMSD02"
        where erdat=to_char(add_months('%s',-1),'yyyymmdd')
        group by zeiar)a,
        (select wplx,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq=to_char(add_days('%s',-2),'yyyymmdd')
        group by wplx)b
        where a.zeiar=b.wplx)n
        where m.wplx=n.wplx
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'品种产销率月分布'as zb,wplx as ms,' 'as mx,zcxl as sl1,hb as sl2
        from(
        select m.wplx,m.zcxl,round((m.zcxl-n.zcxl)/n.zcxl,3) as hb
        from(select b.wplx,round((a.zxl)/(b.zcl),4) as zcxl 
        from(select zeiar,sum(zsum/1000) as zxl
        from  "_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SD/HCXFMSD02"
        where erdat between left('%s',6)||'01'and '%s'
        group by zeiar)a,
        (select wplx,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s' 
        group by wplx)b
        where a.zeiar=b.wplx)m,
        (select b.wplx,round((a.zxl)/(b.zcl),4) as zcxl 
        from(select zeiar,sum(zsum/1000) as zxl
        from  "_SYS_BIC"."XFMGROUP.EDW.02_LOGICAL_LAYER.SD/HCXFMSD02"
        where erdat between left(to_char(add_months('%s',-1),'yyyymmdd'),6)||'01'and to_char(add_months('%s',-1),'yyyymmdd')
        group by zeiar)a,
        (select wplx,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left(to_char(add_months('%s',-1),'yyyymmdd'),6)||'01'and to_char(add_months('%s',-1),'yyyymmdd')
        group by wplx)b
        where a.zeiar=b.wplx)n
        where m.wplx=n.wplx
        )
        union all
        select '%s' as erdat,'%s' as crrq,'公司库存天数分布'as zb,ms as ms,' 'as mx,zkc as sl1,kcts as sl2
        from(
        select ms,--公司名称
               zkc,--总库存
               case when rjcl=0 then 0 else round(zkc/rjcl,2)end as kcts
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.MM/HMXFMMM20"
        ('PLACEHOLDER' = ('$$IP_ID$$','2'),'PLACEHOLDER' = ('$$IP_CALDAY$$','%s'))
        )
        union all
        select '%s' as erdat,'%s' as crrq,'品种库存天数分布'as zb,ms as ms,' 'as mx,zkc as sl1,kcts as sl2
        from(
        select ms,--公司名称
               zkc,--总库存
               case when rjcl=0 then 0 else round(zkc/rjcl,2)end as kcts
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.MM/HMXFMMM20"
        ('PLACEHOLDER' = ('$$IP_ID$$','1'),'PLACEHOLDER' = ('$$IP_CALDAY$$','%s'))
        )
        union all
        select '%s' as erdat,'%s' as crrq,'装置产销率日分布'as zb,zzh as ms,' 'as mx,cxl as sl1,zcl as sl2
        from(
        select b.zzh,round(a.zxl/b.zcl,4)as cxl,b.zcl
        from(select sccj,sum(zsum/1000)as zxl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.SD/HMXFMSD35"
        where erdat='%s'
        group by sccj)a,
        (select zzh,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq=to_char(add_days('%s',-1),'yyyymmdd')
        group by zzh)b
        where a.sccj=b.zzh
        )
        union all
        select left('%s',6) as erdat,'%s' as crrq,'装置产销率月分布'as zb,zzh as ms,' 'as mx,cxl as sl1,zcl as sl2
        from(
        select b.zzh,round(a.zxl/b.zcl,4)as cxl,b.zcl
        from(select sccj,sum(zsum/1000)as zxl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.SD/HMXFMSD35"
        where erdat between left('%s',6)||'01'and '%s'
        group by sccj)a,
        (select zzh,sum(sl)as zcl
        from "_SYS_BIC"."DASHBOARD_XFM.03_DATAMART_LAYER.SC/HMXFMSC07"
        where bzrq between left('%s',6)||'01'and '%s'
        group by zzh)b
        where a.sccj=b.zzh
        )
        ----------------------------------------------------------------------------------------------------------指标
        union all
        select left('20190930',6) as erdat,'%s' as crrq,'月公司间利润分布'as zb,gsmc as ms,' 'as mx,lr as sl1,0 as sl2
        from(
        select gsmc,round(sum(lr/10000),2)as lr
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth=left('20190930',6)
        group by gsmc
        )
        union all
        select left('20190930',6) as erdat,'%s' as crrq,'月毛利润及毛利率'as zb,' ' as ms,' 'as mx,lr as sl1,lrl as sl2
        from(
        select round(sum(lr/10000),2)as lr,round(sum(lr/10000)/sum(sr/10000),3)as lrl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth=left('20190930',6)
        )
        union all
        select left('20190930',6) as erdat,'%s' as crrq,'年毛利润及毛利率'as zb,' ' as ms,' 'as mx,lr as sl1,lrl as sl2
        from(
        select round(sum(lr/10000),2)as lr,round(sum(lr/10000)/sum(sr/10000),3)as lrl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth between left('20190930',4)||'01'and left('20190930',6)
        )
        union all
        select calmonth as erdat,'%s' as crrq,'公司毛利润趋势'as zb,gsmc as ms,' 'as mx,lr as sl1,lrl as sl2
        from(
        select gsmc,calmonth,round(sum(lr/10000),2)as lr,round(sum(lr/10000)/sum(sr/10000),3)as lrl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth between left('20190930',4)||'01'and left('20190930',6)
        group by gsmc,calmonth
        )
        union all
        select calmonth as erdat,'%s' as crrq,'品种毛利润趋势'as zb,wlmc as ms,' 'as mx,lr as sl1,lrl as sl2
        from(
        select wlmc,calmonth,round(sum(lr/10000),2)as lr,round(sum(lr/10000)/sum(sr/10000),3)as lrl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth between left('20190930',4)||'01'and left('20190930',6)
        group by wlmc,calmonth
        )
        union all
        select left('20190930',6) as erdat,'%s' as crrq,'品种利润分布'as zb,wlmc as ms,' 'as mx,lr as sl1,lrl as sl2
        from(
        select wlmc,round(sum(lr/10000),2)as lr,round(sum(lr/10000)/sum(sr/10000),3)as lrl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth=left('20190930',6)
        group by wlmc
        )
        union all
        select calmonth as erdat,'%s' as crrq,'毛利润趋势分布'as zb,' ' as ms,' 'as mx,lrl as sl1,lre as sl2
        from(
        select calmonth,round(sum(lr/10000)/sum(sr/10000),3)as lrl,round(sum(lr/10000),2)as lre
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.FI/HMXFMFI04"
        where calmonth between left('20190930',4)||'01'and left('20190930',6)
        group by calmonth
        )
        ---------------------------------------------------------------------------------------------------------效益
        ----------------------------------------------------------------------------------------------------------设备
        union all
        select left('%s',6) as erdat,'%s' as crrq,'设备缺陷总览'as zb,ms as ms,' 'as mx,sl as sl1,wcsl as sl2
        from(
        select '当月情况'as ms,
               ifnull(sum(case when calmonth=left('%s',6)then jsq end),0)as sl,
               ifnull(sum(case when calmonth=left('%s',6)and APPROVESTATE='J'then jsq end),0)as wcsl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.PM/HMXFMPM06"
        union all
        select '当年情况'as ms,
               ifnull(sum(case when calmonth between left('%s',4)||'01'and left('%s',6)then jsq end),0)as sl,
               ifnull(sum(case when calmonth between left('%s',4)||'01'and left('%s',6)
                        and APPROVESTATE='J' then jsq end),0)as wcsl	   
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.PM/HMXFMPM06"
        )
        union all
        select calmonth as erdat,'%s' as crrq,'设备缺陷数目趋势'as zb,' ' as ms,' 'as mx,sl as sl1,0 as sl2
        from(
        select calmonth,
               sum(jsq)as sl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.PM/HMXFMPM06"
        where calmonth between left(add_years('%s',-1),6) and left('%s',6)
        group by calmonth
        )
        union all
        select left('%s',4) as erdat,'%s' as crrq,'当年设备缺陷类型总览'as zb,qxlx as ms,' 'as mx,sl as sl1,wcsl as sl2
        from(
        select qxlx,
               ifnull(sum(case when calmonth between left('%s',4)||'01'and left('%s',6)then jsq end),0)as sl,
               ifnull(sum(case when calmonth between left('%s',4)||'01'and left('%s',6)
               and APPROVESTATE='J' then jsq end),0)as wcsl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.PM/HMXFMPM06"
        where calmonth between left('%s',4)||'01' and left('%s',6)
        group by qxlx
        )
        union all
        select left('%s',4) as erdat,'%s' as crrq,'当年公司缺陷分布'as zb,gsjc as ms,' 'as mx,sl as sl1,0 as sl2
        from(
        select gsjc,
               sum(jsq)as sl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.PM/HMXFMPM06"
        where calmonth between left('%s',4)||'01' and left('%s',6)
        group by gsjc
        )
        union all
        select left('%s',4) as erdat,'%s' as crrq,'当年单公司缺陷类型分布'as zb,gsjc as ms,qxlx as mx,sl as sl1,0 as sl2
        from(
        select gsjc,
               qxlx,
               sum(jsq)as sl
        from"_SYS_BIC"."XFMGROUP.EDW.03_DATAMART_LAYER.PM/HMXFMPM06"
        where calmonth between left('%s',4)||'01' and left('%s',6)
        group by gsjc,qxlx
        )
        ----------------------------------------------------------------------------------------------------------设备缺陷台账
         '''
    del_sql4 = '''delete from"COMMON"."XFM_SC"where crrq='%s' '''
    ins_sql4 = '''insert into"COMMON"."XFM_SC"values('%s','%s','%s','%s','%s',%s,%s)'''
    # 取合同负盈亏
    sel_sql5 = '''
        select distinct n.vbeln,
           n.bukrs_vf,
           n.vkorg,
           n.kondm,
           n.kunnr,
           n.name1,
           n.zeiar,
           n.matnr,
           erdat,
           kbetr*zxsl as zdtje,
           zxsje as zhtje
    from(select a.vkorg,a.matnr,a.kondm,a.datab,a.datbi,kbetr,kpein,kmein 
    from          "_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.SD/A801" a,
                  "_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.SD/KONP" c
    where a.kschl = 'ZC01'
    and a.knumh = c.knumh 
    and to_char(add_days('%s',-1),'yyyymmdd') between a.datab and a.datbi) m,
    (select vbeln,
            vkorg,
            kondm,
            erdat, 
            bukrs_vf, 
            kunnr, 
            name1, 
            matnr, 
            zeiar,
            sum(kzwi1) as zxsje,
            sum(zsum) as zxsl
     from(select   a.vbeln, --订单号
                   a.vkorg,
                   b.kondm,
                   a.erdat, --订单日期
                   a.bukrs_vf, --公司代码
                   a.kunnr, --客户代码
                   c.name1, --客户名称
                   b.matnr, --物料编号
                   CASE WHEN e.zeiar = '' THEN 'QT'
                   ELSE e.zeiar end zeiar, --物料类型
                   b.KZWI1, --销售总价
                   CASE
                     WHEN b.zieme = 'TO' THEN
                      b.kwmeng * b.umziz * 1000
                     ELSE
                      b.kwmeng * b.umziz
                   END AS ZSUM -- 总销量
              from "_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.SD/VBAK" a,
                   "_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.SD/VBAP" b,
                   "_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.SD/KNA1" c,
                   "_SYS_BIC"."XFMGROUP.EDW.01_BASAL_LAYER.ZSJ.PUBLIC/MARA" e
             where a.vbeln = b.vbeln
               and a.kunnr = c.kunnr
               and b.matnr = e.matnr
               and a.auart = 'ZC05')
    group by vbeln,vkorg,kondm,erdat,bukrs_vf,kunnr,name1,matnr,zeiar) n
     where m.vkorg = n.vkorg
     and m.matnr = n.matnr
     and m.kondm = n.kondm
     and erdat = to_char(add_days('%s',-1),'yyyymmdd')
        '''
    ins_sql5 = '''insert into"COMMON"."XFMSD_HTFYK"values('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s)'''

    for item in([sel_sql1, del_sql1, ins_sql1, today],
                [sel_sql2, ins_sql2, today],
                [sel_sql3, del_sql3, ins_sql3, yesterday],
                [sel_sql4, del_sql4, ins_sql4, yesterday],
                [sel_sql5, ins_sql5, today]):
        if len(item) ==4:
            res = sql().sql_req(conn, str(item[3]), sql=str(item[0]))
            sql().sql_req(conn, str(item[3]), sql=str(item[1]))
            sql().sql_req(conn, res, sql=str(item[2]))
        else:
            res = sql().sql_req(conn, str(item[2]), sql=str(item[0]))
            sql().sql_req(conn, res, sql=str(item[1]))

    get_connection().close_connection(conn)

if __name__ == '__main__':
    main()