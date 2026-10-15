from pathlib import Path
import csv,json,math,re
from fractions import Fraction
R=Path(__file__).resolve().parents[1]; P=R.parent
sources={x['id']:x for x in json.loads((R/'sources/source_index.json').read_text())}
rows=[]
def rec(id,label,value,unit,period,source,scope,kind='观察值',note='原值；未季调'):
 z=sources[source]
 rows.append(dict(id=id,indicator=label,value=value,unit=unit,period=period,release=z['published'],source_id=source,locator=z['locator'],url=z['url'],scope=scope,kind=kind,processing=note))
rec('gdp25','GDP',1401879,'亿元','2025','NBS2025','中国大陆','初步核算')
rec('gdpg25','GDP实际增长',5.0,'同比%','2025','NBS2025','中国大陆','初步核算')
for id,name,v in [('primary','第一产业',6.7),('secondary','第二产业',35.6),('tertiary','第三产业',57.7)]:rec(id,name+'增加值占比',v,'%','2025','NBS2025','中国大陆','初步核算')
for id,name,v,unit in [('age60','60岁及以上占比',23.0,'%'),('age65','65岁及以上占比',15.9,'%'),('birth25','出生人口',792,'万人'),('death25','死亡人口',1131,'万人')]:rec(id,name,v,unit,'2025','NBS2025','中国大陆；人口统计口径')
for id,name,v in [('mean','全国平均',22981),('median','全国中位',19036),('urban','城镇平均',30126),('rural','农村平均',12699)]:rec(id,'人均可支配收入：'+name,v,'元/人','2026上半年','Income2026','全体居民；相应分组')
for id,name,v in [('wage','工资性',57.9),('business','经营净',15.8),('property','财产净',8.0),('transfer','转移净',18.3)]:rec(id,name+'收入占比',v,'%','2026上半年','Income2026','居民可支配收入来源；非国民收入要素份额')
rec('mean_premium','平均数高于中位数',round((22981/19036-1)*100,5),'%','2026上半年','Income2026','全国居民','本文计算','(22981/19036-1)*100；不能当基尼系数')
for id,name,v in [('migrantout','外出农民工',5774),('migrantlocal','本地农民工',4376)]:rec(id,name+'月均收入',v,'元/从业月','2025','Migrant2025','符合农民工调查定义；非全年12个月均值')
rec('cpi','CPI',0.9,'同比%','2026-09','CPI2026','全国居民消费价格')
for id,name,v in [('ppi','PPI出厂总指数',5.0),('ppiinput','工业购进价格',6.9),('ppiproduction','PPI生产资料',6.5),('ppiconsumption','PPI生活资料',-0.1)]:rec(id,name,v,'同比%','2026-09','PPI2026','规模以上工业相关价格调查口径')
for id,name,v in [('fiscallocal','地方一般公共预算本级收入',3.1),('land','土地使用权出让收入',-28.6),('interest','全国一般公共预算债务付息支出',5.4)]:rec(id,name,v,'累计同比%','2026年1—8月','Fiscal2026','预算范围分别列明；不加总')
rec('tsf','社会融资规模存量',464.8,'万亿元','2026-08末','Money2026','实体经济从金融体系融资；含股权','初步统计')
rec('govbond','社融内政府债券余额',103.69,'万亿元','2026-08末','Money2026','社融组成；存量','初步统计')
rec('loanhouse','住户人民币贷款净增减',-1.03,'万亿元','2026年1—8月','Money2026','人民币贷款分部门；流量','初步统计')
rec('loanfirm','企事业单位人民币贷款净增减',11.26,'万亿元','2026年1—8月','Money2026','非金融企业及机关团体；流量','初步统计')
for id,name,v in [('caremen','男性',112),('carewomen','女性',209)]:rec(id,name+'无酬劳动参与者平均时间',v,'分钟/日','2024调查','TimeUse2024','6岁及以上参与该活动人群；非全人口均值')
for id,name,v in [('widincome','收入前10%份额',43.3),('widwealth','财富前10%份额',67.9)]:rec(id,name,v,'%','2024','WID2026','中国CN国别表；分别排序；税前国民收入/净个人财富','研究估计','照录份额；同表底部均值与份额不一致，降低置信度，不用于精确政策测算')
for id,name,v in [('export','货物出口',23.20),('import','货物进口',16.74),('tradeall','进出口总额',39.94)]:rec(id,name,v,'万亿元人民币','2026年前三季度','Trade2026','大陆货物海关口径；名义值')
for id,name,v in [('exportg','货物出口增速',16.4),('importg','货物进口增速',22.3)]:rec(id,name,v,'累计同比%','2026年前三季度','Trade2026','大陆货物海关口径；人民币名义值')
rec('tradebalance','货物进出口差额',6.46,'万亿元人民币','2026年前三季度','Trade2026','货物；不是经常账户','本文计算','23.20-16.74；原数据按0.01万亿元取整')
for id,name,v in [('industrial','规模以上工业增加值',5.3),('retail','社会消费品零售总额',1.1),('realestate','房地产开发投资',-19.9)]:rec(id,name,v,'累计同比%','2026年1—8月','Current2026','中国大陆；三项覆盖不同','观察值','工业为实际增速；零售及投资为名义；不得相减形成供需缺口')
with (R/'data/key_data.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
D={x['id']:x['value'] for x in rows}
checks={
 '产业份额合计':math.isclose(sum(D[k] for k in ['primary','secondary','tertiary']),100),
 '居民来源份额合计':math.isclose(sum(D[k] for k in ['wage','business','property','transfer']),100),
 '货物总额恒等式':math.isclose(D['export']+D['import'],D['tradeall']),
 '货物差额恒等式':math.isclose(D['export']-D['import'],D['tradebalance']),
 '风险分担守恒':sum([4,3,2,1])==sum([4,1,2,3])==10,
}
la=Fraction(5,10)/(1-Fraction(2,10));lb=Fraction(4,10)*la+Fraction(25,100)
pa=Fraction(5,10)/(1-Fraction(12,10)*Fraction(2,10));pb=Fraction(12,10)*Fraction(4,10)*pa+Fraction(25,100)
calc={'checks':checks,'price_example':{'labour_A':float(la),'labour_B':float(lb),'labour_ratio':float(la/lb),'price_A':float(pa),'price_B':float(pb),'price_ratio':float(pa/pb)},'wid_internal_check':{'source_id':'WID2026','locator':'China, Table 1, printed page 166','bottom_mean_income':1988,'full_population_mean_income':14396,'bottom_population_fraction':0.5,'published_bottom_share':13.7,'bottom_share_implied_by_means':1988*.5/14396*100,'published_top_bottom_mean_ratio':31.4,'mean_ratio_implied_by_shares':(43.3/.1)/(13.7/.5),'status':'UNRESOLVED_SOURCE_INCONSISTENCY; not silently repaired'},'no_new_microdata_regression':True}
assert all(checks.values())
(R/'data/calculation_checks.json').write_text(json.dumps(calc,ensure_ascii=False,indent=2))
paths=[]
for t in range(6):paths.append({'period':t,'growth5_interest3':100*(1.03/1.05)**t,'growth2_interest5':100*(1.05/1.02)**t,'kind':'假设示例，非预测'})
with (R/'data/debt_scenarios.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=paths[0].keys());w.writeheader();w.writerows(paths)
base=r'''\pgfplotsset{bookplot/.style={width=.88\textwidth,height=55mm,axis lines=left,ymajorgrids=true,grid style={gray!18},tick label style={font=\small},label style={font=\small},xtick=data,enlarge x limits=.22,scaled y ticks=false,yticklabel style={/pgf/number format/1000 sep={}},bar width=15pt,nodes near coords,nodes near coords style={font=\footnotesize},every axis plot/.append style={fill=teal!65,draw=teal!85!black}}}
'''
charts={}
def bars(name,ids,labels,ylabel,ymin=0,ymax=None):
 vals=[D[x] for x in ids]; ymax=max(vals)*1.22 if ymax is None else ymax
 coord=' '.join(f'({i+1},{v})' for i,v in enumerate(vals))
 charts[name]=r'\begin{tikzpicture}\begin{axis}[bookplot,ybar,ymin='+str(ymin)+',ymax='+str(ymax)+r',ylabel={'+ylabel+r'},xticklabels={'+','.join(labels)+r'}]\addplot coordinates {'+coord+r'};\end{axis}\end{tikzpicture}'
bars('sector',['primary','secondary','tertiary'],['第一产业','第二产业','第三产业'],r'占比（\%）',ymax=70)
bars('prices',['cpi','ppi','ppiinput','ppiproduction','ppiconsumption'],['CPI','PPI','购进价格','生产资料','生活资料'],r'同比（\%）',-1.5,9)
bars('migrantpay',['migrantout','migrantlocal'],['外出农民工','本地农民工'],'元／从业月',ymax=7000)
bars('credit',['loanhouse','loanfirm'],['住户','企事业单位'],'万亿元',-3,14)
bars('fiscal',['fiscallocal','land','interest'],['地方一般预算','土地出让','全国付息'],r'同比（\%）',-36,12)
bars('care',['caremen','carewomen'],['男性参与者','女性参与者'],'分钟／日',ymax=250)
bars('income',['mean','median','urban','rural'],['全国平均','全国中位','城镇平均','农村平均'],'元／人（半年）',ymax=36500)
bars('wid',['widincome','widwealth'],['收入前10\\%','财富前10\\%'],r'各自总量占比（\%）',ymax=100)
bars('trade',['export','import','tradebalance'],['货物出口','货物进口','货物差额'],'万亿元人民币',ymax=28)
charts['rights']=r'''\begin{tikzpicture}[every node/.style={draw=teal!65,rounded corners,align=center,text width=29mm,minimum height=15mm,font=\small}]
\node (a) at (0,0) {法律归属\\公共资产};\node (b) at (3.5,0) {治理与用途\\投资、服务};\node (c) at (7,0) {分配制度\\预算、定价};\node (d) at (10.5,0) {居民实际获得\\现金、质量、保障};
\draw[->,thick] (a)--(b);\draw[->,thick] (b)--(c);\draw[->,thick] (c)--(d);
\end{tikzpicture}'''
charts['risk']=r'''\begin{tikzpicture}\begin{axis}[bookplot,ybar stacked,nodes near coords={},ymin=0,ymax=12,ylabel={损失单位},xtick={1,2},xticklabels={初始分担,最终分担},legend style={at={(.5,-.2)},anchor=north,legend columns=4,font=\small,draw=none},enlarge x limits=.7]
\addplot+[fill=teal!80] coordinates {(1,4)(2,4)};\addplot+[fill=blue!45] coordinates {(1,3)(2,1)};\addplot+[fill=orange!60] coordinates {(1,2)(2,2)};\addplot+[fill=gray!50] coordinates {(1,1)(2,3)};\legend{股东,银行,供应商,财政}
\end{axis}\end{tikzpicture}'''
ca=' '.join(f"({x['period']},{x['growth5_interest3']:.6f})" for x in paths)
cb=' '.join(f"({x['period']},{x['growth2_interest5']:.6f})" for x in paths)
charts['debt']=r'''\begin{tikzpicture}\begin{axis}[bookplot,ymin=85,ymax=120,xlabel={期数},ylabel={债务／收入（\%）},xtick={0,1,2,3,4,5},enlarge x limits=.05,nodes near coords={},legend style={at={(.02,.97)},anchor=north west,legend columns=1,font=\small,draw=none}]
\addplot+[fill=none,thick,mark=*] coordinates {'''+ca+r'''};\addplot+[fill=none,draw=orange!80!black,thick,mark=square*] coordinates {'''+cb+r'''};\legend{名义增长5\%、利率3\%,名义增长2\%、利率5\%}
\end{axis}\end{tikzpicture}'''
block=base+'\n'.join(r'\expandafter\def\csname chart@'+k+r'\endcsname{'+v+'}\n' for k,v in charts.items())
p=P/'china-capital-2026.tex';text=p.read_text();text=re.sub(r'% CHART_DEFINITIONS_BEGIN.*?% CHART_DEFINITIONS_END',lambda m:'% CHART_DEFINITIONS_BEGIN\n'+block+'% CHART_DEFINITIONS_END',text,flags=re.S);p.write_text(text)
print('Data rows',len(rows),'charts',len(charts),'checks',checks)
