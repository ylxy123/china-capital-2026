"""Update research ledgers for the expansion; never change the compiled manuscript."""
from pathlib import Path
import csv, json, hashlib, math, re

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / 'research'
E = R / 'expansion'

def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        fields = list(dict.fromkeys(k for row in rows for k in row))
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

sources = json.loads((R/'sources/source_index.json').read_text())
by_id = {x['id']:x for x in sources}
access = {
    'MarxPrice':'第三卷第九章公开原文；用于生产价格命题',
    'Card2022':'原刊摘要与公开稿入口；工资设定机制',
    'Wright1985':'作者高校主页公开扫描章节；核对章首概念，未宣称逐页全文复现',
    'Chamon2010':'NBER公开摘要及版本信息；不外推历史系数',
    'Bai2016':'NBER公开摘要；历史财政扩张机制',
    'Migration2023':'NBER公开工作论文摘要及研究设计；局部效应',
    'Housing1998':'政府公开历史制度原文',
    'LiuTian2018':'公开研究回顾的摘要与分类比较段落；未逐项复核其全部引用',
    'MinWage2014':'研究机构摘要与作者公开说明；PDF直连受限',
    'ValueTrade2014':'正式版本书目信息；期刊入口受限；机制改用同作者NBER版本',
    'AIWork2025':'NBER页面确认正式版本书目信息；期刊入口受限；机制改用NBER版本',
    'TradeAdjust2016':'NBER公开摘要与版本信息；美国劳动市场比较机制',
    'Tax1994':'财政部公开历史制度原文',
    'InjuryJilin2026':'吉林省社会保险事业管理局实施说明正文',
    'AIWorkNBER':'NBER WP 31161，2023年11月修订公开摘要及正式版本信息',
    'ValueTradeNBER':'NBER WP 18579，2013年2月修订公开摘要及正式版本信息',
}
for item in json.loads((E/'added-sources.json').read_text()):
    row = dict(item)
    row['access'] = access.get(row['id'], row['locator'])
    row['limits'] = '按所列阅读层级使用；未重新运行调查、模型或因果估计；具体外推边界见正文及文献评议。'
    row['published'] = str(row['year'])
    row['geography'] = '中国大陆制度与经验；国外理论或样本的范围在正文单列'
    by_id[row['id']] = row
by_id['Injury2026']['access'] = '原稿使用的全国发布链接；扩充版复核返回验证页面'
by_id['Injury2026']['limits'] = '不作为扩充版全国实际覆盖判断依据；正文仅采用吉林实施说明支持省级事实'
by_id['WID2026']['limits'] = '原表均值、份额与倍数存在未解释冲突；仅作来源审计，不作精确比较或阶层规模估计'
sources = list(by_id.values())
save(R/'sources/source_index.json', sources)
write_csv(R/'sources/source_index.csv', sources)

issues = read_csv(R/'sources/issues.csv')
for item in issues:
    if item['id'] == 'WID-01':
        item['处置'] = '撤下精确比较图；所有原列数值仅用于来源审计；不自行修表'
    if item['id'] == 'LEGAL-01':
        item['相关来源'] = 'LandLaw;CompanyLaw;InjuryJilin2026'
new_issues = [
    {'id':'SOURCE-03','问题':'全国职业伤害保障发布页本次返回验证页','核查状态':'省级实施原文可读，全国实际覆盖未验证','处置':'原段改为吉林2026年7月启动；不从地区扩围推断全员全面保障','相关来源':'Injury2026;InjuryJilin2026'},
    {'id':'VERSION-01','问题':'AI与增加值贸易期刊入口访问受限','核查状态':'同作者NBER公开版本可读并确认正式版书目信息','处置':'引用公开版本；不混用不同版本效果量或假称阅读全文','相关来源':'AIWorkNBER;AIWork2025;ValueTradeNBER;ValueTrade2014'},
    {'id':'COUNT-01','问题':'源码长度、图表文字与正文篇幅不同','核查状态':'独立严格计数','处置':'排除标题、图表、公式、代码、附录与文献；报告正文汉字和含标题图表数两套指标','相关来源':'structural_validation.json'},
    {'id':'PROVENANCE-01','问题':'旧PDF与中断时扩写源码不对应','核查状态':'已重新内置编译并捕获匹配源码的真实PDF','处置':'以native_pdf_export.json的源码及PDF哈希对应为准','相关来源':'native_compile_result.json;native_pdf_export.json'},
]
issue_map = {x['id']:x for x in issues}
issue_map.update({x['id']:x for x in new_issues})
write_csv(R/'sources/issues.csv', list(issue_map.values()))

data = read_csv(R/'data/key_data.csv')
for row in data:
    if row['source_id'] == 'WID2026':
        row['kind'] = '原来源声称的研究估计；仅作审计'
        row['processing'] = '保留原列数值以审计版本；已撤下精确比较图，不用于分配结论、阶层规模或政策测算'
write_csv(R/'data/key_data.csv', data)
checks = json.loads((R/'data/calculation_checks.json').read_text())
checks['wid_internal_check'].update({
    'bottom_mean_wealth':5447, 'full_mean_wealth':86462,
    'published_bottom_wealth_share':6.3,
    'bottom_wealth_share_implied_by_means':.5*5447/86462*100,
    'disposition':'Audit only; published values are not silently corrected and are not used for precise distribution conclusions.'})
checks['expansion_examples'] = {
    'classification':'All scenarios below are hypothetical teaching examples, not observed China data or forecasts.',
    'task_hours_before':10, 'task_hours_after':6,
    'task_volume_ratio_for_constant_total_hours':10/6,
    'energy_intensity_ratio':.9, 'output_ratio':1.2, 'total_energy_ratio':.9*1.2,
    'care_setup_cost_in_10k_yuan':100, 'annual_operations_in_10k_yuan':60,
    'care_five_year_operations_in_10k_yuan':5*60,
    'debt_after_5_periods_growth5_interest3':100*(1.03/1.05)**5,
    'debt_after_5_periods_growth2_interest5':100*(1.05/1.02)**5,
    'profit_rate':20/200, 'profit_share':20/100, 'capital_productivity':100/200}
assert math.isclose(checks['expansion_examples']['total_energy_ratio'],1.08)
assert math.isclose((20/100)*(100/200),20/200)
assert all(checks['checks'].values())
save(R/'data/calculation_checks.json', checks)

appraisal = read_csv(R/'sources/literature_appraisal.csv')
items = [
    ('MarxPrice','价值与生产价格','避免把严格劳动价格比例冒充原典全部命题','原典理论不是当期计量验证','投入产出、资本估值与价格资料','准确重述原命题后限定强版本'),
    ('Card2022','工资设定与雇主权力','把可行替代和工资设定纳入劳动关系','企业与地区异质性；不能由集中度直接推出全部因果','雇主、流动、工资与退出条件','作为竞争解释与机制来源'),
    ('Wright1985','中间阶级位置','讨论部分控制与劳动依赖并存','概念框架不等于中国人口分类已验证','管理权限、资产收益、劳动关系','多轴关系分析，不估计规模'),
    ('LiuTian2018','中国社会分层研究回顾','区分等级描述与关系分类','研究回顾不是2026微观样本','职业、权限、保障和家庭资料','比较框架；不全盘接受任何作者立场'),
    ('Chamon2010','家庭不确定性与储蓄','历史机制帮助提出保障问题','历史期与当期不同，住房人口为竞争解释','收入风险、资产、消费与保障','不外推历史系数'),
    ('Bai2016','财政扩张与地方融资','解释历史融资组织的延续','不能用历史机制估算2026债务规模','项目、融资、公共账户','机制支持与边界并列'),
    ('Migration2023','保障与迁移','权益可携带影响流动的研究路径','改革和样本范围限制外推','迁移、待遇与就业','局部证据不直接全国化'),
    ('AIWorkNBER','生成式AI与任务','实际采用与异质性经验案例','特定客服场景，非中国就业预测','审核、质量、任务、工时与工资','只引用已核对机制，不搬用效果量'),
    ('ValueTradeNBER','毛贸易与增加值','分解重复计数与增加值来源','没有2026投入产出重算','投入产出、贸易来源与收入归属','提供核算框架，拒绝伪造当期比例'),
    ('TradeAdjust2016','贸易调整','总量收益与地区损失可以并存','美国经验不能直接移植中国幅度与年限','地区、职业、收入与转岗','作为调整速度的竞争机制'),
]
ap_map = {x['source_id']:x for x in appraisal}
for key,topic,value,limit,test,handling in items:
    ap_map[key] = dict(zip(['source_id','主题','采用价值','限制或竞争解释','可检验资料','本文处理'],[key,topic,value,limit,test,handling]))
write_csv(R/'sources/literature_appraisal.csv', list(ap_map.values()))

claims = [
    ('H1','产权与公众收益传递','公共资产形成收益但治理与分配路径不同','治理—预算—服务—家庭获得','行业景气、财力、选择进入改革','治理与传递信息不能提高资产规模之外的解释力','Grossman1986;CompanyLaw;Zhou2007','P076-P095;P244-P246;P258-P261'),
    ('H2','再生产与生产扩张','家庭的时间、收入或保障构成实际约束','服务与保障—就业和家庭时间—需求与持续能力','人口、偏好、住房与独立收入冲击','服务实际改善后预期中间环节仍未出现','Chamon2010;Migration2023;TimeUse2024','P137-P158;P229-P237;P250-P257'),
    ('H3','控制与最终损失责任','决策收益与损失承担分离且缺少有效约束','救助预期—事前行为—冲击—损失分担','问责、声誉、不同项目风险','责任分离不增加所述冒险，或由其他约束完全解释','Kornai2003;Minsky1992;Bai2016','P096-P115;P235-P246;P262-P265'),
    ('H4','平台依赖与风险','入口难替代、退出昂贵、申诉不透明','规则—收费与任务—商家劳动者承担—退出','服务质量、欺诈风险、需求变化与样本退出','高依赖仍存在有效协商且收益广泛传递','Rochet2003;ILO2025;InjuryJilin2026','P181-P201'),
    ('H5','多轴社会位置','单一收入或职业不能覆盖控制与缓冲差异','劳动依赖、控制、收益、风险与家庭条件—冲击结果','收入教育既有解释、生命周期、个人偏好','新增维度不能改善对选定结果的解释或预测','Wright1985;LiuTian2018;PYZ2019','P159-P180'),
]
write_csv(E/'claim-register.csv',[dict(zip(['id','命题','前提','机制','竞争解释','反证或支持不足条件','来源','段落锚点'],x),**{'证据状态':'候选命题或理论综合；无新增因果估计'}) for x in claims])
positions = [
    ('公共资源配置者','授权预算和资源用途','监督、决策与公共责任','P173','公共管理资产不是私人净财富'),
    ('大型资本所有者与企业控制者','收益权与组织控制','经营、担保与竞争','P173','股权、控制与当期收入分别记录'),
    ('中小雇主','局部用工控制与上游依赖','回款、租金、个人担保','P173','规模小不取消雇主责任'),
    ('自雇与个体经营者','本人劳动与客户工具','停工、任务与保障','P173','登记身份不等于定价自主'),
    ('稳定受薪者','劳动依赖与收入连续性','岗位、支付、照护','P173','单位性质不等于资源配置权'),
    ('专业技术与市场化白领','技能、资格、部分管理权限','技能转换、绩效、负债','P173','文凭与工资不等于永久安全'),
    ('产业与服务业劳动者','岗位合同、工时与退出条件','工资、伤害、迁移','P173','农民工不等于纯农业职业'),
    ('平台劳动者','入口、任务规则与工具投入','账号、等待、事故','P173;P196-P200','自备车辆不等于完全自主'),
    ('不同经营方式的农村家庭','土地、经营、务工和转移组合','农业、城市就业、养老照护','P173','农村居住不是同质阶级'),
]
write_csv(E/'class-relations.csv',[dict(zip(['位置','关系重点','风险重点','正文锚点','分类边界'],x),**{'交叉维度':'住房、负债、迁移、年龄、照护与家庭积累','规模声明':'分析位置可重叠；未估计人口比例，不可直接相加'}) for x in positions])

source = (ROOT/'china-capital-2026.tex').read_text()
used = {k for group in re.findall(r'\\cite\{([^}]+)\}',source) for k in group.split(',')}
assert not used - by_id.keys(), used - by_id.keys()
summary = {'source_registry_entries':len(sources),'cited_sources':len(used),'literature_appraisals':len(ap_map),
           'issues':len(issue_map),'key_data_rows':len(data),'claims':len(claims),'class_positions':len(positions),
           'publication_cutoff':'2026-10-14','expansion_recheck_date':'2026-10-15',
           'new_microdata_or_causal_regressions':False,
           'source_sha256':hashlib.sha256((ROOT/'china-capital-2026.tex').read_bytes()).hexdigest()}
save(E/'research-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
