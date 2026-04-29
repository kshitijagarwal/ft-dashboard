"""
FT Polling Dashboard — 5 panels in a single HTML file.
Data: Mar 1 – Apr 27, 2026  (all FT cohorts, DISTINCT-fixed).
Tab 2 is the Cohort AOV Pivot Table (latest data through Apr 29, 2026).
"""
import json, datetime, os
from collections import defaultdict

# Base directory = folder containing this script (works from any working dir)
_HERE = os.path.dirname(os.path.abspath(__file__))

# ── Panel 1: Daily Revenue by Amount ─────────────────────────────────────────
# (date, amount, completions, revenue)  — only rows with completions > 0
daily_raw = [
    ("2026-03-01",699,16,11184),("2026-03-02",699,12,8388),
    ("2026-03-03",5,2,10),("2026-03-03",699,25,17475),
    ("2026-03-04",699,20,13980),("2026-03-05",699,13,9087),
    ("2026-03-06",699,32,22368),("2026-03-07",699,52,36348),
    ("2026-03-08",699,57,39843),("2026-03-09",699,55,38445),
    ("2026-03-10",699,16,11184),("2026-03-11",699,25,17475),
    ("2026-03-12",699,30,20970),("2026-03-13",5,1,5),
    ("2026-03-13",699,49,34251),("2026-03-14",699,77,53823),
    ("2026-03-15",699,130,90870),("2026-03-16",699,118,82482),
    ("2026-03-17",10,2,20),("2026-03-17",199,1,199),
    ("2026-03-17",699,176,123024),("2026-03-18",199,1,199),
    ("2026-03-18",699,203,141897),("2026-03-19",10,3,30),
    ("2026-03-19",699,187,130713),("2026-03-20",699,183,127917),
    ("2026-03-21",10,3,30),("2026-03-21",199,1,199),
    ("2026-03-21",699,191,133509),("2026-03-22",699,194,135606),
    ("2026-03-23",199,2,398),("2026-03-23",699,202,141198),
    ("2026-03-24",199,4,796),("2026-03-24",699,219,153081),
    ("2026-03-25",249,3,747),("2026-03-25",699,230,160770),
    ("2026-03-26",199,2,398),("2026-03-26",699,244,170556),
    ("2026-03-27",199,1,199),("2026-03-27",699,285,199215),
    ("2026-03-28",249,1,249),("2026-03-28",699,252,176148),
    ("2026-03-29",699,368,257232),("2026-03-30",249,1,249),
    ("2026-03-30",699,322,225078),("2026-03-31",699,377,263523),
    ("2026-04-01",699,370,258630),("2026-04-02",699,378,264222),
    ("2026-04-03",249,1,249),("2026-04-03",699,382,267018),
    ("2026-04-04",249,1,249),("2026-04-04",699,319,222981),
    ("2026-04-05",699,437,305463),("2026-04-06",199,1,199),
    ("2026-04-06",399,81,32319),("2026-04-06",699,382,267018),
    ("2026-04-07",199,2,398),("2026-04-07",399,148,59052),
    ("2026-04-07",699,407,284493),("2026-04-08",199,9,1791),
    ("2026-04-08",399,101,40299),("2026-04-08",699,357,249543),
    ("2026-04-09",199,15,2985),("2026-04-09",399,136,54264),
    ("2026-04-09",699,377,263523),("2026-04-10",199,94,18706),
    ("2026-04-10",249,2,498),("2026-04-10",399,111,44289),
    ("2026-04-10",699,361,252339),("2026-04-11",199,470,93530),
    ("2026-04-11",699,377,263523),("2026-04-12",199,344,68456),
    ("2026-04-12",699,401,280299),("2026-04-13",199,388,77212),
    ("2026-04-13",699,322,225078),("2026-04-14",199,441,87759),
    ("2026-04-14",699,344,240456),("2026-04-15",199,387,77013),
    ("2026-04-15",699,368,257232),("2026-04-16",199,511,101689),
    ("2026-04-16",699,346,241854),("2026-04-17",199,456,90744),
    ("2026-04-17",499,1,499),("2026-04-17",699,383,267717),
    ("2026-04-18",199,535,106465),("2026-04-18",699,372,260028),
    ("2026-04-19",199,477,94923),("2026-04-19",249,1,249),
    ("2026-04-19",699,379,264921),("2026-04-20",199,569,113231),
    ("2026-04-20",699,327,228573),("2026-04-21",29,413,11977),
    ("2026-04-21",49,26,1274),("2026-04-21",69,13,897),
    ("2026-04-21",99,9,891),("2026-04-21",102,84,8568),
    ("2026-04-21",149,28,4172),("2026-04-21",199,522,103878),
    ("2026-04-21",249,18,4482),("2026-04-21",449,6,2694),
    ("2026-04-21",699,355,248145),("2026-04-22",29,1889,54781),
    ("2026-04-22",49,109,5341),("2026-04-22",69,100,6900),
    ("2026-04-22",99,70,6930),("2026-04-22",102,71,7242),
    ("2026-04-22",149,203,30247),("2026-04-22",199,80,15920),
    ("2026-04-22",249,72,17928),("2026-04-22",299,18,5382),
    ("2026-04-22",449,156,70044),("2026-04-22",699,223,155877),
    ("2026-04-23",29,748,21692),("2026-04-23",49,97,4753),
    ("2026-04-23",69,114,7866),("2026-04-23",99,93,9207),
    ("2026-04-23",149,199,29651),("2026-04-23",198,1,198),
    ("2026-04-23",199,26,5174),("2026-04-23",249,2,498),
    ("2026-04-23",250,9,2250),("2026-04-23",299,102,30498),
    ("2026-04-23",449,417,187233),("2026-04-23",489,1,489),
    ("2026-04-23",499,2,998),("2026-04-23",689,2,1378),
    ("2026-04-24",29,639,18531),("2026-04-24",49,94,4606),
    ("2026-04-24",69,70,4830),("2026-04-24",99,59,5841),
    ("2026-04-24",102,9,918),("2026-04-24",149,182,27118),
    ("2026-04-24",198,2,396),("2026-04-24",199,31,6169),
    ("2026-04-24",250,32,8000),("2026-04-24",299,77,23023),
    ("2026-04-24",449,367,164783),("2026-04-24",499,3,1497),
    ("2026-04-25",29,590,17110),("2026-04-25",49,69,3381),
    ("2026-04-25",69,68,4692),("2026-04-25",99,66,6534),
    ("2026-04-25",102,6,612),("2026-04-25",149,175,26075),
    ("2026-04-25",198,5,990),("2026-04-25",199,13,2587),
    ("2026-04-25",250,37,9250),("2026-04-25",299,78,23322),
    ("2026-04-25",449,373,167477),("2026-04-25",499,1,499),
    ("2026-04-26",29,601,17429),("2026-04-26",49,93,4557),
    ("2026-04-26",69,73,5037),("2026-04-26",99,69,6831),
    ("2026-04-26",102,4,408),("2026-04-26",149,194,28906),
    ("2026-04-26",198,5,990),("2026-04-26",199,23,4577),
    ("2026-04-26",249,4,996),("2026-04-26",250,52,13000),
    ("2026-04-26",299,106,31694),("2026-04-26",449,416,186784),
    ("2026-04-26",699,1,699),("2026-04-27",29,198,5742),
    ("2026-04-27",49,15,735),("2026-04-27",69,16,1104),
    ("2026-04-27",99,20,1980),("2026-04-27",149,61,9089),
    ("2026-04-27",198,1,198),("2026-04-27",199,5,995),
    ("2026-04-27",299,35,10465),("2026-04-27",449,111,49839),
    ("2026-04-27",689,2,1378),
]

# att1 daily conversion data: (date, att1_total_attempts, att1_completions)
att1_daily = {
    "2026-03-01":(201,16),"2026-03-02":(230,11),"2026-03-03":(386,26),
    "2026-03-04":(323,19),"2026-03-05":(295,7),"2026-03-06":(721,26),
    "2026-03-07":(1061,46),"2026-03-08":(921,49),"2026-03-09":(829,34),
    "2026-03-10":(158,5),"2026-03-11":(359,14),"2026-03-12":(351,17),
    "2026-03-13":(938,45),"2026-03-14":(1653,66),"2026-03-15":(2535,116),
    "2026-03-16":(2329,96),"2026-03-17":(3208,155),"2026-03-18":(4219,175),
    "2026-03-19":(3920,164),"2026-03-20":(3176,143),"2026-03-21":(3121,159),
    "2026-03-22":(3276,155),"2026-03-23":(3456,154),"2026-03-24":(4087,177),
    "2026-03-25":(4076,170),"2026-03-26":(4231,177),"2026-03-27":(4651,216),
    "2026-03-28":(4448,193),"2026-03-29":(5867,253),"2026-03-30":(5419,197),
    "2026-03-31":(6662,255),"2026-04-01":(6549,225),"2026-04-02":(6676,240),
    "2026-04-03":(6953,242),"2026-04-04":(6990,207),"2026-04-05":(7599,297),
    "2026-04-06":(7682,256),"2026-04-07":(8572,316),"2026-04-08":(8084,296),
    "2026-04-09":(8652,323),"2026-04-10":(8040,307),"2026-04-11":(7607,346),
    "2026-04-12":(8087,379),"2026-04-13":(7387,305),"2026-04-14":(7874,315),
    "2026-04-15":(8875,340),"2026-04-16":(9643,333),"2026-04-17":(10408,365),
    "2026-04-18":(9042,343),"2026-04-19":(9884,346),"2026-04-20":(9102,288),
    "2026-04-21":(9299,339),"2026-04-22":(9459,342),"2026-04-23":(11283,437),
    "2026-04-24":(10530,381),"2026-04-25":(9673,383),"2026-04-26":(11160,430),
    "2026-04-27":(5276,144),
}

# Bucket amounts for clean chart
CHART_AMTS  = [699, 449, 399, 299, 199, 149, 99, 69, 49, 29]
BUCKET_MAP  = {102:99, 198:199, 249:199, 250:199}
AMT_COLORS  = {
    699:"#6366f1", 449:"#8b5cf6", 399:"#a855f7", 299:"#ec4899",
    199:"#ef4444", 149:"#f97316",  99:"#f59e0b",  69:"#84cc16",
     49:"#22c55e",  29:"#14b8a6",
}

def bucket_amt(a):
    if a in CHART_AMTS: return a
    return BUCKET_MAP.get(a)

# Aggregate by date × bucket
by_date      = defaultdict(lambda: defaultdict(int))   # date → {amount → revenue}
comp_by_date = defaultdict(lambda: defaultdict(int))   # date → {amount → completions}
total_comp_d = defaultdict(int)
total_rev_d  = defaultdict(int)

for d, amt, comp, rev in daily_raw:
    if d == "2026-04-28" or not comp: continue
    b = bucket_amt(amt)
    if b:
        by_date[d][b]    += (rev or 0)
        comp_by_date[d][b] += (comp or 0)
    total_comp_d[d] += (comp or 0)
    total_rev_d[d]  += (rev or 0)

DATES = sorted(by_date.keys())
lbl   = [d[5:] for d in DATES]   # "MM-DD"

p1_labels   = json.dumps(lbl)
p1_datasets = []
for a in CHART_AMTS:
    data = [by_date[d].get(a, 0) for d in DATES]
    if sum(data) == 0: continue
    p1_datasets.append({
        "label": f"₹{a}",
        "data": data,
        "backgroundColor": AMT_COLORS[a],
        "stack": "rev",
        "borderWidth": 0,
    })
p1_datasets_js = json.dumps(p1_datasets)
p1_completions = json.dumps([total_comp_d[d] for d in DATES])

# ── Panel 1 data table ────────────────────────────────────────────────────────
# Shows: date | # per bucket | total # | total rev | AOV | % att1 comp
active_amts = [a for a in CHART_AMTS if sum(comp_by_date[d].get(a,0) for d in DATES)>0]

def pct_str(n,d): return f"{n/d*100:.1f}%" if d else "—"

tbl_rows = []
for d in DATES:
    tc   = total_comp_d[d]
    tr   = total_rev_d[d]
    aov  = round(tr/tc) if tc else 0
    a1t, a1c = att1_daily.get(d, (0,0))
    a1pct = f"{a1c/a1t*100:.1f}%" if a1t else "—"
    cells = [f'<td class="dt">{d[5:]}</td>']
    for a in active_amts:
        n = comp_by_date[d].get(a,0)
        cells.append(f'<td class="{"n-pos" if n else "n-zero"}">{n if n else "—"}</td>')
    cells += [
        f'<td class="n total-c">{tc:,}</td>',
        f'<td class="n total-r">₹{tr:,.0f}</td>',
        f'<td class="n aov">₹{aov:,}</td>',
        f'<td class="{"att1-hi" if a1t and a1c/a1t>=0.04 else "att1-med" if a1t and a1c/a1t>=0.025 else "att1-lo"}">{a1pct}</td>',
    ]
    tbl_rows.append(f"<tr>{''.join(cells)}</tr>")

amt_headers = "".join(f'<th>₹{a}#</th>' for a in active_amts)
p1_table = f"""
<div class="tbl-scroll">
  <table class="dtable">
    <thead><tr>
      <th class="dt-hdr">Date</th>
      {amt_headers}
      <th>Total #</th><th>Total Revenue</th><th>AOV</th><th>att1 Conv%</th>
    </tr></thead>
    <tbody>{"".join(tbl_rows)}</tbody>
  </table>
</div>"""

# ── Panel 2: Cohort AOV Pivot Table ──────────────────────────────────────────
# Rows: (cohort_date, att1_amount) with cohort_size >= 1000, att1_amount in [699, 449]
# Cols: (att_num, att_amount) pairs with >= 20 total completions
# Cells: rev_per_user = (comp_count / cohort_size) × att_amount ; conv% = comp/cohort_size

# Cohort-level stats: [cohort_date, att1_amount, cohort_size, total_done, total_revenue]
pivot_cohort_raw = [
    ["2026-02-27",699,1352,111,59022],["2026-02-28",699,1246,75,44555],
    ["2026-03-01",699,343,33,19047],["2026-03-02",699,387,39,21971],
    ["2026-03-03",699,545,52,31018],["2026-03-04",699,459,41,20729],
    ["2026-03-05",699,384,27,15523],["2026-03-06",699,914,91,43529],
    ["2026-03-07",699,1240,124,62106],["2026-03-08",699,1047,100,51520],
    ["2026-03-09",699,905,77,46193],["2026-03-10",699,198,12,8088],
    ["2026-03-11",699,406,48,26032],["2026-03-12",699,509,47,25353],
    ["2026-03-13",699,1111,112,60918],["2026-03-14",699,1853,158,73785],
    ["2026-03-15",699,2788,253,135240],["2026-03-16",699,2530,237,117596],
    ["2026-03-17",699,3520,346,170947],["2026-03-18",699,4324,357,184476],
    ["2026-03-19",699,3911,344,173279],["2026-03-20",699,3090,289,149691],
    ["2026-03-21",699,3043,298,155155],["2026-03-22",699,3206,326,157200],
    ["2026-03-23",699,3418,319,167711],["2026-03-24",699,4096,440,217966],
    ["2026-03-25",699,4061,460,211280],["2026-03-26",699,4176,415,196725],
    ["2026-03-27",699,4623,571,269012],["2026-03-28",699,4392,506,226140],
    ["2026-03-29",699,5852,678,285228],["2026-03-30",699,5396,591,239935],
    ["2026-03-31",699,6648,697,290561],["2026-04-01",699,6487,684,268228],
    ["2026-04-02",699,6737,746,273769],["2026-04-03",699,6921,656,256743],
    ["2026-04-04",699,6838,708,251584],["2026-04-05",699,7444,797,312711],
    ["2026-04-06",699,7361,832,276958],["2026-04-07",699,8168,930,325242],
    ["2026-04-08",699,7584,913,293571],["2026-04-09",699,8154,1015,318561],
    ["2026-04-10",699,7643,973,311928],["2026-04-11",699,7303,980,328840],
    ["2026-04-12",699,7612,991,346248],["2026-04-13",699,6969,909,290505],
    ["2026-04-14",699,7892,883,299067],["2026-04-15",699,8083,911,308274],
    ["2026-04-16",699,9161,986,316203],["2026-04-17",699,10020,1011,339732],
    ["2026-04-18",699,8697,853,317357],["2026-04-19",699,9521,756,316854],
    ["2026-04-20",699,8853,657,268788],["2026-04-21",699,9025,635,285421],
    ["2026-04-22",699,6612,449,198701],["2026-04-22",449,2579,194,67278],
    ["2026-04-23",449,10560,734,254785],["2026-04-24",449,9920,603,216135],
    ["2026-04-25",449,9262,575,219150],["2026-04-26",449,10412,488,210574],
    ["2026-04-27",699,3009,70,48930],["2026-04-27",449,7405,281,126169],
    ["2026-04-28",699,3188,50,34950],
]

# Load per-attempt breakdown from query result file (sits next to this script)
_piv_file = os.path.join(_HERE, 'pivot_att_data.json')
_piv_raw = json.loads(open(_piv_file).read())
piv_att_data = {}
piv_pair_totals = {}
for _r in _piv_raw['rows']:
    _cd, _a1, _an, _aa, _cc = _r
    _a1 = int(_a1); _an = int(_an); _aa = int(_aa); _cc = int(_cc)
    piv_att_data[(_cd, _a1, _an, _aa)] = _cc
    piv_pair_totals[(_an, _aa)] = piv_pair_totals.get((_an, _aa), 0) + _cc

PIVOT_PAIRS = sorted([k for k, v in piv_pair_totals.items() if v >= 20], key=lambda x: (x[0], -x[1]))

# Build cohort index (only >=1000 cohorts with att1 in [699,449])
MAIN_AMTS = {699, 449}
piv_cohort = {}
for row in pivot_cohort_raw:
    cd, a1, cs, td, tr_ = row
    a1 = int(a1); cs = int(cs); td = int(td); tr_ = int(tr_) if tr_ else 0
    if a1 in MAIN_AMTS and cs >= 1000:
        piv_cohort[(cd, a1)] = {'cohort_size': cs, 'total_done': td, 'total_revenue': tr_}

piv_rows_sorted = sorted(piv_cohort.keys(), key=lambda x: (x[0], -x[1]))

# Group pairs by att_num for column headers
from collections import defaultdict as _ddict
piv_att_groups = _ddict(list)
for an, aa in PIVOT_PAIRS:
    piv_att_groups[an].append(aa)
piv_att_nums = sorted(piv_att_groups.keys())

# Totals
piv_total_cs = sum(piv_cohort[k]['cohort_size'] for k in piv_rows_sorted)
piv_total_td = sum(piv_cohort[k]['total_done'] for k in piv_rows_sorted)
piv_total_tr = sum(piv_cohort[k]['total_revenue'] for k in piv_rows_sorted)

def _piv_cell_class(rpu):
    if rpu <= 0:   return 'pe'
    if rpu < 0.5:  return 'pd1'
    if rpu < 2.0:  return 'pd2'
    if rpu < 5.0:  return 'pd3'
    if rpu < 15.0: return 'pd4'
    return 'pd5'

def _piv_fmt_date(d):
    dt = datetime.date.fromisoformat(d)
    return dt.strftime('%-d %b')

def _piv_fmt_rev(r):
    if r >= 1_000_000: return f'₹{r/1_000_000:.1f}M'
    if r >= 1000:      return f'₹{r//1000}k'
    return f'₹{r}'

def _piv_cell(comp, cs, aa):
    if cs == 0 or comp == 0: return '<td class="pe">—</td>'
    rpu = comp * aa / cs
    pct_ = comp / cs * 100
    cls = _piv_cell_class(rpu)
    return f'<td class="{cls}" title="{comp:,} comps | {pct_:.2f}%">₹{rpu:.1f}<small>{pct_:.2f}%</small></td>'

# Build thead
def _piv_thead():
    r1 = ['<td class="pfh pfh1" rowspan="2">Date</td>',
           '<td class="pfh pfh1" rowspan="2">Att1<br>Amt</td>',
           '<td class="pfh pfh1" rowspan="2">Cohort</td>',
           '<td class="pfh pfh1" rowspan="2">Rev</td>',
           '<td class="pfh pfh1 ptot-col" rowspan="2">Cohort<br>AOV</td>']
    for an in piv_att_nums:
        r1.append(f'<td class="pgh" colspan="{len(piv_att_groups[an])}">Att {an}</td>')
    r2 = []
    for an in piv_att_nums:
        for aa in piv_att_groups[an]:
            r2.append(f'<td class="pah">₹{aa}</td>')
    return f'<tr>{"".join(r1)}</tr>\n<tr>{"".join(r2)}</tr>'

# Build data rows
def _piv_data_rows():
    out = []
    prev_month = None
    for k in piv_rows_sorted:
        cd, a1 = k
        info = piv_cohort[k]
        cs = info['cohort_size']; td = info['total_done']; tr_ = info['total_revenue']
        month = cd[:7]
        if month != prev_month:
            prev_month = month
            mdt = datetime.date.fromisoformat(cd)
            ncols = 5 + len(PIVOT_PAIRS)
            out.append(f'<tr class="pms"><td colspan="{ncols}">{mdt.strftime("%B %Y").upper()}</td></tr>')
        aov = tr_ / cs if cs else 0
        cells = [f'<td class="pfd">{_piv_fmt_date(cd)}</td>',
                 f'<td class="pfa">₹{a1}</td>',
                 f'<td class="pfn">{cs:,}<small>{td:,} done</small></td>',
                 f'<td class="pfr">{_piv_fmt_rev(tr_)}</td>',
                 f'<td class="ptot-col">₹{aov:.1f}</td>']
        for an, aa in PIVOT_PAIRS:
            comp = piv_att_data.get((cd, a1, an, aa), 0)
            cells.append(_piv_cell(comp, cs, aa))
        out.append(f'<tr>{"".join(cells)}</tr>')
    return '\n'.join(out)

# Build totals row
def _piv_totals_row():
    taov = piv_total_tr / piv_total_cs if piv_total_cs else 0
    cells = [f'<td class="pfd ptot-row">TOTAL</td>',
             '<td class="pfa ptot-row">—</td>',
             f'<td class="pfn ptot-row">{piv_total_cs:,}<small>{piv_total_td:,} done</small></td>',
             f'<td class="pfr ptot-row">{_piv_fmt_rev(piv_total_tr)}</td>',
             f'<td class="ptot-col ptot-row">₹{taov:.1f}</td>']
    for an, aa in PIVOT_PAIRS:
        total_comp = sum(piv_att_data.get((cd, a1, an, aa), 0) for (cd, a1) in piv_rows_sorted)
        cells.append(_piv_cell(total_comp, piv_total_cs, aa))
    return f'<tr>{"".join(cells)}</tr>'

TODAY_STR = datetime.date.today().strftime('%-d %b %Y')
p2_pivot_thead = _piv_thead()
p2_pivot_rows  = _piv_data_rows()
p2_pivot_total = _piv_totals_row()
NUM_PIVOT_COLS = len(PIVOT_PAIRS)

# ── Panel 3: First Attempt Failure Reasons by Cohort Date ────────────────────
# Abandoned + Other Failed merged → Cancellations
# (cohort_date, attempted, completed, insuff_funds, abandoned, other_failed, avg_amt)
cohort_raw = [
    ("03-01",351,25,98,3,225,695),("03-02",402,21,156,2,223,691),
    ("03-03",551,30,205,8,308,696),("03-04",469,21,174,0,274,695),
    ("03-05",389,11,142,0,236,697),("03-06",923,31,334,5,553,697),
    ("03-07",1249,53,415,3,778,698),("03-08",1060,53,345,2,660,698),
    ("03-09",910,35,309,3,563,698),("03-10",203,8,80,3,112,690),
    ("03-11",414,21,169,4,220,694),("03-12",511,28,193,2,288,696),
    ("03-13",1124,53,390,2,679,697),("03-14",1868,69,637,3,1159,698),
    ("03-15",2824,126,903,2,1793,698),("03-16",2545,105,831,9,1600,697),
    ("03-17",3584,161,1167,10,2246,697),("03-18",4350,176,1342,7,2825,698),
    ("03-19",3912,159,1173,3,2577,698),("03-20",3104,133,984,4,1983,699),
    ("03-21",3052,156,901,1,1994,699),("03-22",3233,151,970,5,2107,698),
    ("03-23",3464,155,1095,1,2213,696),("03-24",4146,173,1384,3,2586,694),
    ("03-25",4111,170,1432,2,2507,695),("03-26",4219,174,1335,5,2705,697),
    ("03-27",4654,214,1559,3,2878,698),("03-28",4439,192,1563,3,2681,697),
    ("03-29",5876,248,2066,2,3560,698),("03-30",5439,196,1855,2,3386,697),
    ("03-31",6700,262,1988,14,4436,697),("04-01",6550,228,2202,5,4115,697),
    ("04-02",6747,238,2271,11,4227,698),("04-03",6949,240,2231,7,4471,698),
    ("04-04",6845,212,2239,8,4386,698),("04-05",7449,287,2298,4,4860,698),
    ("04-06",7413,249,2347,2,4815,697),("04-07",8259,308,2392,6,5553,696),
    ("04-08",7946,292,2314,366,4974,689),("04-09",8433,319,2561,79,5474,684),
    ("04-10",7799,302,2319,3,5175,687),("04-11",7496,343,2221,3,4929,686),
    ("04-12",7973,374,2313,2,5284,676),("04-13",7275,297,2351,4,4623,677),
    ("04-14",8315,331,2421,418,5145,683),("04-15",8342,328,2478,89,5447,684),
    ("04-16",9472,328,2884,11,6249,682),("04-17",10356,365,3271,3,6717,683),
    ("04-18",8950,339,2821,9,5781,683),("04-19",9796,345,2982,9,6460,683),
    ("04-20",8995,288,2764,18,5925,688),("04-21",9246,340,2833,13,6060,686),
    ("04-22",9380,333,2826,9,6212,618),("04-23",11175,433,3295,2765,4682,447),
    ("04-24",10420,379,3041,4252,2748,444),("04-25",9590,382,2849,3893,2466,447),
    ("04-26",11038,428,3100,4799,2711,441),("04-27",4672,114,491,1613,2454,493),
]

p3_labels    = json.dumps([r[0] for r in cohort_raw])
p3_attempted = json.dumps([r[1] for r in cohort_raw])
p3_avgamt    = json.dumps([r[6] for r in cohort_raw])

def pct(n, total): return round(n/total*100, 1) if total else 0

p3_comp   = json.dumps([pct(r[2], r[1]) for r in cohort_raw])
p3_ins    = json.dumps([pct(r[3], r[1]) for r in cohort_raw])
# Cancellations = Abandoned + Other Failed
p3_cancel = json.dumps([pct(r[4]+r[5], r[1]) for r in cohort_raw])
# Raw values for tooltip
p3_comp_n   = json.dumps([r[2] for r in cohort_raw])
p3_ins_n    = json.dumps([r[3] for r in cohort_raw])
p3_cancel_n = json.dumps([r[4]+r[5] for r in cohort_raw])

# ── Panel 4: Amount by Attempt + Cohort Remaining % ──────────────────────────
cohort_remaining = {
    1:307565, 2:274046, 3:87705, 4:63355,
    5:51857,  6:44780,  7:39328, 8:34806,
}
BASE = cohort_remaining[1]

# (att_num, amount, resolved, completions, conv_pct, rev_pu)
amt_by_att = [
    (1,199,4722,225,4.76,9.48),(1,449,36455,1371,3.76,16.89),
    (1,499,401,7,1.75,8.71),(1,699,252800,9767,3.86,27.01),
    (2,199,4300,45,1.05,2.08),(2,250,206,65,31.55,78.88),
    (2,299,35586,279,0.78,2.34),(2,449,10577,125,1.18,5.31),
    (2,699,217565,1463,0.67,4.70),
    (3,149,9477,317,3.34,4.98),(3,199,26644,989,3.71,7.39),
    (3,249,2374,84,3.54,8.81),(3,299,2150,23,1.07,3.20),
    (3,449,2497,19,0.76,3.42),(3,699,53460,554,1.04,7.24),
    (4,149,8383,233,2.78,4.14),(4,199,20467,603,2.95,5.86),
    (4,299,2798,21,0.75,2.24),(4,399,206,3,1.46,5.81),
    (4,449,1391,9,0.65,2.91),(4,699,41289,405,0.98,6.86),
    (5,149,8097,195,2.41,3.59),(5,199,19157,592,3.09,6.15),
    (5,249,277,5,1.81,4.49),(5,299,882,5,0.57,1.70),
    (5,399,4934,91,1.84,7.36),(5,449,591,3,0.51,2.28),
    (5,699,22464,218,0.97,6.78),
    (6,99,5074,215,4.24,4.19),(6,149,2237,61,2.73,4.06),
    (6,199,17557,460,2.62,5.21),(6,249,236,5,2.12,5.28),
    (6,299,938,5,0.53,1.59),(6,399,4617,87,1.88,7.52),
    (6,449,300,2,0.67,2.99),(6,699,18998,183,0.96,6.73),
    (7,69,4732,258,5.45,3.76),(7,99,1194,64,5.36,5.31),
    (7,149,874,15,1.72,2.56),(7,199,16256,357,2.20,4.37),
    (7,299,352,2,0.57,1.70),(7,399,4063,50,1.23,4.91),
    (7,699,13714,131,0.96,6.68),
    (8,49,4173,266,6.37,3.12),(8,69,1093,77,7.04,4.86),
    (8,149,833,13,1.56,2.33),(8,199,15313,319,2.08,4.15),
    (8,299,359,2,0.56,1.67),(8,399,3578,46,1.29,5.13),
    (8,699,11941,92,0.77,5.39),
]

OUTLIERS = {(2,250)}
MIN_RES_WIN = 1000

from collections import defaultdict as ddict
by_att = ddict(list)
for row in amt_by_att:
    by_att[row[0]].append(row)
for k in by_att:
    by_att[k].sort(key=lambda x: x[5], reverse=True)

def conv_color(c):
    if c>=5: return "#16a34a"
    if c>=3: return "#3b82f6"
    if c>=1: return "#f59e0b"
    return "#ef4444"

def size_badge(n):
    if n>=50000: return f"<span class='sz xl'>{n:,}</span>"
    if n>=10000: return f"<span class='sz lg'>{n:,}</span>"
    if n>=2000:  return f"<span class='sz md'>{n:,}</span>"
    return              f"<span class='sz sm'>{n:,}</span>"

p4_cards = []
for att in sorted(by_att.keys()):
    rows = by_att[att]
    cr   = cohort_remaining.get(att)
    cr_pct = f"{cr/BASE*100:.1f}%" if cr else "—"
    cr_str = f"{cr:,} users ({cr_pct} of att1)" if cr else "—"
    valid  = [r for r in rows if (att,r[1]) not in OUTLIERS]
    max_rev  = max((r[5] for r in valid if r[2]>=MIN_RES_WIN), default=0)
    max_conv = max(r[4] for r in rows) if rows else 1
    trs = []
    for r in rows:
        is_out = (att,r[1]) in OUTLIERS
        is_win = (not is_out) and r[5]==max_rev and max_rev>0 and r[2]>=MIN_RES_WIN
        bw  = max(3, int(r[4]/max_conv*80))
        bc  = conv_color(r[4])
        rc  = "win-row" if is_win else ("out-row" if is_out else "")
        ico = "🏆 " if is_win else ""
        out_t = "<span class='flag'>outlier</span>" if is_out else ""
        sm_t  = "<span class='sm-note'>small n</span>" if not is_out and r[2]<1000 else ""
        trs.append(f"""<tr class="{rc}">
          <td class="amt">₹{r[1]}</td>
          <td>{size_badge(r[2])}</td>
          <td><div class="bw"><div class="bar" style="width:{bw}px;background:{bc};"></div><span>{r[4]:.2f}%</span></div></td>
          <td class="rv">{ico}₹{r[5]:.2f}{out_t}{sm_t}</td>
        </tr>""")
    p4_cards.append(f"""
    <div class="att-card">
      <div class="att-hdr">Attempt {att}</div>
      <div class="att-meta">Cohort at this stage: {cr_str}</div>
      <table>
        <thead><tr><th>Amount</th><th>Resolved</th><th>Conv %</th><th>Rev/user</th></tr></thead>
        <tbody>{"".join(trs)}</tbody>
      </table>
    </div>""")
p4_html = "\n".join(p4_cards)

# ── Panel 5: Multi-Charge Impact (DISTINCT-corrected) ─────────────────────────
# (first_amount, comp_rank, base_users, users_reached, pct_of_base,
#  total_rev, avg_amt, avg_days, rev_per_bu)
multi_raw = [
    (699,2,12327,2,0.02,898,449,3.5,0.07),
    (449,2,1846,138,7.48,33692,244,1.9,18.25),
    (299,2,407,12,2.95,3138,262,2.2,7.71),
    (249,2,101,10,9.90,1940,194,3.7,19.21),
    (199,2,4171,1518,36.39,206842,136,4.7,49.59),
    (199,3,4171,575,13.79,76504,133,6.5,18.34),
    (199,4,4171,226,5.42,18867,83,8.7,4.52),
    (199,5,4171,11,0.26,343,31,11.9,0.08),
    (149,2,954,46,4.82,5584,121,2.3,5.85),
    (149,3,954,1,0.10,149,149,3.0,0.16),
    (99,2,332,22,6.63,1848,84,2.1,5.57),
    (69,2,376,27,7.18,1303,48,2.6,3.47),
    (69,3,376,2,0.53,98,49,3.5,0.26),
    (49,2,388,19,4.90,871,46,1.8,2.24),
    (49,3,388,1,0.26,29,29,4.0,0.07),
    (29,2,3890,435,11.18,12615,29,2.3,3.24),
    (29,3,3890,39,1.00,1131,29,3.5,0.29),
]

def ordinal(n): return {2:"2nd",3:"3rd",4:"4th",5:"5th"}.get(n,f"{n}th")

from collections import defaultdict as ddict2
m_groups = ddict2(list)
m_base   = {}
for row in multi_raw:
    m_groups[row[0]].append(row)
    m_base[row[0]] = row[2]

total_rep = sum(r[5] for r in multi_raw)

m_cards = []
for fa in sorted(m_groups.keys(), reverse=True):
    rows = m_groups[fa]
    bu   = m_base[fa]
    tot  = sum(r[5] for r in rows)
    epbu = round(tot/bu, 2) if bu else 0
    max_pct = max(r[4] for r in rows)
    trs = []
    for r in rows:
        _,cr,_,ur,pob,tr2,aca,adp,rpbu = r
        bw = max(2, int(pob/max(max_pct,0.01)*80))
        days_s = "same day" if adp<=0.05 else f"{adp}d later"
        flag = ""
        if adp<=0.1: flag = "<span class='tag tbug'>same-day</span>"
        elif pob>=20: flag = "<span class='tag thigh'>polling continues post-success</span>"
        elif pob>=5:  flag = "<span class='tag twarn'>notable repeat rate</span>"
        rc = "rv-high" if rpbu>=20 else ("rv-med" if rpbu>=5 else "rv-low")
        trs.append(f"""<tr>
          <td class="rank">{ordinal(cr)} charge</td>
          <td class="n">{ur:,}</td>
          <td><div class="bw"><div class="bar" style="width:{bw}px;background:#3b82f6;"></div><span>{pob:.2f}%</span></div></td>
          <td>₹{aca:,}</td><td class="days">{days_s}</td>
          <td class="n">₹{tr2:,.0f}</td>
          <td class="{rc}">₹{rpbu:.2f}</td>
          <td>{flag}</td>
        </tr>""")
    extra_badge = (f'<span class="extra-note">+₹{tot:,.0f} repeat revenue &nbsp;·&nbsp; ₹{epbu:.2f}/base user</span>'
                   if tot>0 else '<span class="extra-note zero">No repeat charges</span>')
    first_tr = f"""<tr class="first-row">
      <td class="rank">1st charge</td>
      <td class="n">{bu:,}</td>
      <td><div class="bw"><div class="bar" style="width:80px;background:#6366f1;"></div><span>base</span></div></td>
      <td>₹{fa:,}</td><td class="days">—</td>
      <td class="n">₹{bu*fa:,.0f} <span class="approx">~</span></td>
      <td class="rv-high">₹{fa:.2f}</td><td></td>
    </tr>"""
    m_cards.append(f"""
    <div class="mc-card">
      <div class="mc-hdr">
        <span class="amt-badge">First charge: ₹{fa}</span>
        <span class="base-note">{bu:,} users</span>
        {extra_badge}
      </div>
      <table>
        <thead><tr>
          <th>Charge</th><th>Users</th><th>% of base</th>
          <th>Avg amount</th><th>Avg gap</th>
          <th>Total revenue</th><th>Rev/base user</th><th></th>
        </tr></thead>
        <tbody>{first_tr}{"".join(trs)}</tbody>
      </table>
    </div>""")
p5_html = "\n".join(m_cards)

# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────
CHART_W = max(900, len(DATES)*14)

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>FT Polling Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Inter',Arial,sans-serif;background:#f1f5f9;color:#0f172a;font-size:13px;}}

/* Header */
.hdr{{background:#1e293b;color:#fff;padding:18px 24px;}}
.hdr h1{{font-size:20px;font-weight:700;}}
.hdr p{{font-size:12px;color:#94a3b8;margin-top:4px;}}

/* Tabs */
.tabs{{background:#fff;border-bottom:2px solid #e2e8f0;display:flex;padding:0 24px;gap:0;position:sticky;top:0;z-index:10;}}
.tab{{padding:13px 18px;cursor:pointer;font-size:13px;font-weight:600;color:#64748b;
      border-bottom:3px solid transparent;white-space:nowrap;user-select:none;}}
.tab.active{{color:#3b82f6;border-bottom-color:#3b82f6;}}
.tab:hover:not(.active){{color:#334155;}}

/* Panels */
.panel{{display:none;padding:24px;}}
.panel.active{{display:block;}}

/* Section titles */
.sec-title{{font-size:14px;font-weight:700;color:#1e293b;margin-bottom:6px;}}
.sec-sub{{font-size:12px;color:#64748b;margin-bottom:16px;line-height:1.5;}}

/* Chart scroll container */
.chart-scroll{{overflow-x:auto;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;}}
.chart-wrap{{min-width:{CHART_W}px;height:360px;position:relative;}}

/* ── Panel 1 data table ───────────────────────────────────────────────── */
.tbl-scroll{{overflow-x:auto;background:#fff;border:1px solid #e2e8f0;border-radius:10px;
             margin-top:18px;}}
.dtable{{width:100%;border-collapse:collapse;font-size:12px;white-space:nowrap;}}
.dtable th{{background:#f8fafc;color:#64748b;font-size:10px;font-weight:700;
            padding:6px 8px;text-align:right;border-bottom:2px solid #e2e8f0;
            text-transform:uppercase;letter-spacing:.04em;}}
.dtable th.dt-hdr{{text-align:left;position:sticky;left:0;background:#f8fafc;z-index:2;}}
.dtable td{{padding:5px 8px;border-bottom:1px solid #f1f5f9;text-align:right;font-variant-numeric:tabular-nums;}}
.dtable td.dt{{text-align:left;font-weight:600;position:sticky;left:0;background:#fff;z-index:1;}}
.dtable tr:hover td{{background:#f8fafc;}}
.dtable tr:hover td.dt{{background:#f8fafc;}}
.n-pos{{color:#1e40af;font-weight:600;}}
.n-zero{{color:#cbd5e1;}}
.total-c{{font-weight:700;color:#0f172a;border-left:2px solid #e2e8f0;}}
.total-r{{font-weight:700;color:#0f172a;}}
.aov{{color:#7c3aed;font-weight:600;}}
.att1-hi{{color:#166534;font-weight:700;background:#dcfce7;}}
.att1-med{{color:#92400e;font-weight:600;background:#fef9c3;}}
.att1-lo{{color:#64748b;}}

/* General tables */
table{{width:100%;border-collapse:collapse;}}
th{{background:#f8fafc;color:#64748b;font-size:11px;font-weight:700;
    padding:7px 10px;text-align:left;border-bottom:2px solid #e2e8f0;
    text-transform:uppercase;letter-spacing:.04em;white-space:nowrap;}}
td{{padding:7px 10px;border-bottom:1px solid #f1f5f9;vertical-align:middle;}}
tr:last-child td{{border-bottom:none;}}
.first-row td{{background:#eff6ff;font-weight:600;}}
.win-row{{background:#f0fdf4;}}
.out-row{{background:#fefce8;}}
.rank,.days{{white-space:nowrap;font-weight:600;font-size:12px;}}
.n{{font-variant-numeric:tabular-nums;white-space:nowrap;}}
.pct{{white-space:nowrap;}}
.cum{{color:#7c3aed;font-weight:600;white-space:nowrap;}}
.rv-high{{color:#166534;font-weight:700;}}
.rv-med{{color:#92400e;font-weight:600;}}
.rv-low{{color:#64748b;}}
.approx{{color:#94a3b8;font-size:11px;}}
.bw{{display:flex;align-items:center;gap:6px;}}
.bar{{height:10px;border-radius:3px;min-width:3px;}}
.amt{{font-weight:700;white-space:nowrap;}}
.rv{{font-weight:700;white-space:nowrap;}}
.flag{{font-size:10px;font-weight:700;color:#b45309;background:#fef9c3;
       padding:1px 5px;border-radius:3px;margin-left:4px;}}
.sm-note{{font-size:10px;color:#94a3b8;margin-left:4px;}}
.sz{{font-size:12px;font-weight:600;padding:2px 6px;border-radius:4px;}}
.sz.xl{{background:#dbeafe;color:#1e40af;}}
.sz.lg{{background:#dcfce7;color:#166534;}}
.sz.md{{background:#f1f5f9;color:#334155;}}
.sz.sm{{background:#fef9c3;color:#854d0e;}}

/* ── Panel 2 Cohort AOV Pivot ─────────────────────────────────────────── */
.pivot-wrap{{overflow:auto;background:#fff;border:1px solid #e2e8f0;border-radius:10px;
             max-height:78vh;position:relative;box-shadow:0 1px 8px rgba(0,0,0,.06);}}
.pivot-tbl{{border-collapse:collapse;white-space:nowrap;font-size:11px;}}
.pivot-tbl td{{padding:4px 8px;text-align:center;border-right:1px solid #e2e8f0;
    border-bottom:1px solid #e2e8f0;vertical-align:middle;background:#ffffff}}
.pivot-tbl small{{font-size:8px;display:block;opacity:.75;margin-top:1px}}
/* Sticky header rows */
.pivot-tbl thead tr:first-child td{{position:sticky;top:0;z-index:20;background:#f1f5f9;
    border-bottom:2px solid #cbd5e1}}
.pivot-tbl thead tr:last-child td{{position:sticky;top:29px;z-index:19;background:#f8fafc;
    border-bottom:2px solid #e2e8f0}}
/* Fixed left columns */
.pfd,.pfa,.pfn,.pfr,.ptot-col{{position:sticky;background:#ffffff;z-index:10;text-align:left}}
.pfd{{left:0;min-width:54px;font-weight:600;color:#64748b}}
.pfa{{left:54px;min-width:44px;font-weight:700;color:#0f172a}}
.pfn{{left:98px;min-width:76px;color:#64748b;font-size:10px}}
.pfr{{left:174px;min-width:56px;font-weight:700;color:#2563eb}}
.ptot-col{{left:230px;min-width:58px;font-weight:700;
    border-right:2px solid #93c5fd!important;text-align:center}}
/* Sticky header fixed cells */
.pfh{{position:sticky;z-index:30!important;background:#f1f5f9!important;
    font-size:9px;text-transform:uppercase;letter-spacing:.5px;color:#64748b;
    text-align:center;padding:6px 8px;font-weight:600}}
.pfh1:nth-child(1){{left:0}}.pfh1:nth-child(2){{left:54px}}
.pfh1:nth-child(3){{left:98px}}.pfh1:nth-child(4){{left:174px}}
.pfh1:nth-child(5){{left:230px;border-right:2px solid #93c5fd!important}}
/* Attempt group headers */
.pgh{{background:#eff6ff;font-size:8.5px;font-weight:700;text-transform:uppercase;
       letter-spacing:.6px;color:#2563eb;border-right:2px solid #bfdbfe;
       border-left:1px solid #dbeafe}}
.pah{{background:#f8fafc;font-size:9px;color:#94a3b8;font-weight:600}}
/* Month separator */
.pms td{{background:#f1f5f9!important;color:#94a3b8;font-size:9px;font-weight:700;
          text-transform:uppercase;letter-spacing:.8px;padding:5px 8px;
          text-align:left;border-top:2px solid #cbd5e1}}
/* Colour scale */
.pe  {{color:#cbd5e1;background:#f8fafc}}
.pd1 {{color:#94a3b8;background:#f8fafc}}
.pd2 {{color:#92400e;background:#fffbeb}}
.pd3 {{color:#b45309;background:#fef3c7}}
.pd4 {{color:#166534;background:#f0fdf4}}
.pd5 {{color:#14532d;background:#dcfce7;font-weight:700}}
.pivot-tbl tr:hover td{{background-color:rgba(219,234,254,.35)!important}}
/* Totals row */
.ptot-row{{background:#eff6ff!important;border-top:2px solid #93c5fd;
    font-weight:700;font-size:11px}}
.pfd.ptot-row{{color:#2563eb;letter-spacing:.5px;font-size:9px;text-transform:uppercase}}
/* Legend */
.plegend{{display:flex;gap:10px;margin-bottom:10px;align-items:center;font-size:10px;color:#475569;flex-wrap:wrap}}
.plbox{{width:28px;height:14px;border-radius:3px;display:inline-block;vertical-align:middle;
        border:1px solid #e2e8f0}}

/* Panel 4 */
.att-grid{{display:flex;flex-wrap:wrap;gap:18px;}}
.att-card{{background:#fff;border:1px solid #e2e8f0;border-radius:10px;
           padding:14px 16px;min-width:360px;flex:1;}}
.att-hdr{{font-size:12px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:.06em;}}
.att-meta{{font-size:11px;color:#64748b;margin:4px 0 10px;}}

/* Panel 5 */
.mc-card{{background:#fff;border:1px solid #e2e8f0;border-radius:10px;margin-bottom:18px;overflow:hidden;}}
.mc-hdr{{background:#f8fafc;padding:12px 16px;border-bottom:1px solid #e2e8f0;
         display:flex;align-items:center;gap:12px;flex-wrap:wrap;}}
.amt-badge{{font-weight:700;font-size:15px;}}
.base-note{{font-size:12px;color:#64748b;}}
.extra-note{{font-size:12px;font-weight:600;color:#166534;background:#dcfce7;
             padding:2px 8px;border-radius:4px;margin-left:auto;}}
.extra-note.zero{{color:#64748b;background:#f1f5f9;}}
.tag{{font-size:10px;font-weight:700;padding:2px 6px;border-radius:3px;white-space:nowrap;margin-right:3px;}}
.tbug{{background:#fee2e2;color:#991b1b;}}
.thigh{{background:#fef9c3;color:#854d0e;}}
.twarn{{background:#f1f5f9;color:#475569;}}

/* Note / summary boxes */
.note-box{{background:#fefce8;border:1px solid #fde047;border-radius:8px;
           padding:12px 16px;font-size:13px;color:#713f12;margin-bottom:20px;line-height:1.6;}}
code{{background:#fef9c3;padding:1px 4px;border-radius:3px;font-size:12px;}}
.stats-row{{display:flex;gap:14px;margin-bottom:20px;flex-wrap:wrap;}}
.stat-box{{background:#fff;border:1px solid #e2e8f0;border-radius:10px;
           padding:14px 20px;flex:1;min-width:180px;}}
.stat-box.hi{{border-left:4px solid #3b82f6;}}
.stat-val{{font-size:22px;font-weight:700;}}
.stat-lbl{{font-size:12px;color:#64748b;margin-top:4px;}}
.legend{{display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:#64748b;margin-bottom:14px;align-items:center;}}
.ldot{{width:12px;height:12px;border-radius:3px;display:inline-block;flex-shrink:0;}}
.ann{{font-size:11px;color:#64748b;margin-top:8px;line-height:1.5;}}
</style>
</head>
<body>

<div class="hdr">
  <h1>FT Polling Dashboard</h1>
  <p>All Cashfree FT cohorts &nbsp;·&nbsp; DISTINCT paid_plan_id applied throughout &nbsp;·&nbsp; Data through {TODAY_STR}</p>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab(0)">1. Daily Revenue</div>
  <div class="tab" onclick="switchTab(1)">2. Cohort AOV Pivot</div>
  <div class="tab" onclick="switchTab(2)">3. Cohort Failures</div>
  <div class="tab" onclick="switchTab(3)">4. Amount by Attempt</div>
  <div class="tab" onclick="switchTab(4)">5. Repeat Charges</div>
</div>

<!-- ═══ PANEL 1 — Daily Revenue ════════════════════════════════════════════ -->
<div class="panel active" id="p0">
  <p class="sec-title">Daily Revenue by Charge Amount</p>
  <p class="sec-sub">
    Stacked bar = revenue by amount bucket each day. Line = daily completions (right axis).
    Key inflections: <b>Apr 6</b> ₹399 att3 experiment &nbsp;|&nbsp; <b>Apr 11</b> ₹199 att3 broadly &nbsp;|&nbsp;
    <b>Apr 21</b> full step-down launches &nbsp;|&nbsp; <b>Apr 23</b> ₹449 att1 strategy
  </p>
  <div class="legend">
    {"".join(f'<span><span class="ldot" style="background:{AMT_COLORS[a]};"></span>₹{a}</span>' for a in CHART_AMTS if sum(by_date[d].get(a,0) for d in DATES)>0)}
    <span style="margin-left:8px;"><span class="ldot" style="background:#1e293b;"></span>Completions (line)</span>
  </div>
  <div class="chart-scroll">
    <div class="chart-wrap"><canvas id="p1chart"></canvas></div>
  </div>

  <p class="sec-title" style="margin-top:24px;">Daily Breakdown Table</p>
  <p class="sec-sub">
    # per amount bucket · Total completions · Total revenue · AOV ·
    att1 Conv% = (att1 completions on that day) / (att1 total attempts on that day).
    <span style="color:#166534;font-weight:600;">Green ≥4%</span> &nbsp;
    <span style="color:#92400e;font-weight:600;">Amber 2.5–4%</span> &nbsp;
    <span style="color:#64748b;">Grey &lt;2.5%</span>
  </p>
  {p1_table}
</div>

<!-- ═══ PANEL 2 — Cohort AOV Pivot ══════════════════════════════════════════ -->
<div class="panel" id="p1">
  <p class="sec-title">FT Cohort — Revenue Contribution per Cohort User &nbsp;·&nbsp; Feb–Apr 2026 (to {TODAY_STR})</p>
  <p class="sec-sub">
    Each cell: <strong>Cohort AOV contribution = (Completions at this slot / Cohort Size) × Amount</strong>, with conv% below.
    Cell values across all att columns sum to the Cohort AOV column. Hover for exact completion counts.
    Only columns with ≥ 20 total completions shown ({NUM_PIVOT_COLS} columns). Cohorts &lt; 1,000 users excluded.
  </p>
  <div class="plegend">
    Revenue contribution per cohort user:
    <span><span class="plbox" style="background:#f8fafc;border:1px solid #e2e8f0"></span> &lt;₹0.5</span>
    <span><span class="plbox" style="background:#fffbeb"></span> ₹0.5–2</span>
    <span><span class="plbox" style="background:#fef3c7"></span> ₹2–5</span>
    <span><span class="plbox" style="background:#f0fdf4"></span> ₹5–15</span>
    <span><span class="plbox" style="background:#dcfce7"></span> &gt;₹15</span>
    <span style="color:#94a3b8">— = no conversion</span>
  </div>
  <div class="pivot-wrap">
    <table class="pivot-tbl"><thead>
      {p2_pivot_thead}
    </thead><tbody>
      {p2_pivot_rows}
      {p2_pivot_total}
    </tbody></table>
  </div>
</div>

<!-- ═══ PANEL 3 — Cohort Failures ══════════════════════════════════════════ -->
<div class="panel" id="p2">
  <p class="sec-title">First Attempt (att1) Failure Reasons — by FT Cohort Date</p>
  <p class="sec-sub">
    Each bar = all users whose FT plan started on that date who reached att1.
    100% stacked. "Cancellations" = Abandoned (UPI rejected by user) + Other Failed (mandate revoked, subscription cancelled, etc.).
    Apr 23+ spike in Cancellations driven by ₹449 att1 cohorts with ~40% UPI abandonment.
  </p>
  <div class="legend">
    <span><span class="ldot" style="background:#16a34a;"></span>Completed</span>
    <span><span class="ldot" style="background:#ef4444;"></span>Insufficient Funds</span>
    <span><span class="ldot" style="background:#94a3b8;"></span>Cancellations (Abandoned + Other Failed)</span>
  </div>
  <div class="chart-scroll">
    <div class="chart-wrap" style="height:320px;"><canvas id="p3chart"></canvas></div>
  </div>
  <div class="ann">
    Avg att1 amount by cohort: ₹698–699 through Apr 22 (pure ₹699 strategy) → drops to ₹440s from Apr 23 (₹449 att1 launched).
    Insuff Funds rate is remarkably stable at ~28–33% of att1 attempts throughout — indicating a persistent segment of
    users whose bank balances are consistently insufficient for any charge amount.
  </div>
</div>

<!-- ═══ PANEL 4 — Amount by Attempt ════════════════════════════════════════ -->
<div class="panel" id="p3">
  <p class="sec-title">Amount Performance by Attempt — All FT Users Combined</p>
  <p class="sec-sub">
    All Cashfree FT cohorts from Mar 1, 2026. Only amounts with ≥200 resolved shown.
    🏆 = highest rev/user among amounts with ≥1,000 resolved.
    "Cohort at this stage" shows how many total plans had a non-Initiated attempt at this att_num.
  </p>
  <div class="stats-row">
    {"".join(f'<div class="stat-box hi"><div class="stat-val">{cohort_remaining[a]:,}</div><div class="stat-lbl">Users reaching att{a} ({cohort_remaining[a]/BASE*100:.1f}% of att1)</div></div>' for a in sorted(cohort_remaining.keys())[:4])}
  </div>
  <div class="stats-row">
    {"".join(f'<div class="stat-box"><div class="stat-val">{cohort_remaining[a]:,}</div><div class="stat-lbl">Users reaching att{a} ({cohort_remaining[a]/BASE*100:.1f}% of att1)</div></div>' for a in sorted(cohort_remaining.keys())[4:])}
  </div>
  <div class="legend">
    Conv % colour:
    <span><span class="ldot" style="background:#16a34a;"></span>≥5%</span>
    <span><span class="ldot" style="background:#3b82f6;"></span>3–5%</span>
    <span><span class="ldot" style="background:#f59e0b;"></span>1–3%</span>
    <span><span class="ldot" style="background:#ef4444;"></span>&lt;1%</span>
    &nbsp;
    <span><span class="ldot" style="background:#f0fdf4;border:1px solid #86efac;"></span>Winner</span>
    <span><span class="ldot" style="background:#fefce8;border:1px solid #fde047;"></span>Outlier</span>
  </div>
  <div class="att-grid">{p4_html}</div>
</div>

<!-- ═══ PANEL 5 — Repeat Charges ═══════════════════════════════════════════ -->
<div class="panel" id="p4">
  <p class="sec-title">Repeat Charges — Users with 2nd, 3rd, 4th, 5th Completions</p>
  <div class="note-box">
    <b>Data correction applied:</b> Earlier analysis had a join fan-out bug (users with multiple FT records caused charge
    attempts to appear N times). After adding <code>DISTINCT</code> on paid_plan_id: max completions/user dropped
    46 → 5, ₹699 "same-day duplicate" eliminated (was artifact), total repeat revenue ₹12.2L → ₹3.65L.
    The ₹199 group's 36.4% 2nd-charge rate is real — polling continues after a step-down success.
  </div>
  <div class="stats-row">
    <div class="stat-box hi">
      <div class="stat-val">₹{total_rep:,.0f}</div>
      <div class="stat-lbl">Total repeat revenue (2nd–5th completions, all cohorts)</div>
    </div>
    <div class="stat-box">
      <div class="stat-val">₹2,06,842</div>
      <div class="stat-lbl">₹199 cohort 2nd-charge revenue — 1,518 users @ avg ₹136, 4.7 days later</div>
    </div>
    <div class="stat-box">
      <div class="stat-val">36.4%</div>
      <div class="stat-lbl">₹199 first-charge users getting a 2nd charge — polling doesn't stop at step-down</div>
    </div>
  </div>
  {p5_html}
</div>

<script>
// ── Tab switching ──────────────────────────────────────────────────────────
const panels = document.querySelectorAll('.panel');
const tabs   = document.querySelectorAll('.tab');
function switchTab(i) {{
  panels.forEach((p,j) => p.classList.toggle('active', j===i));
  tabs.forEach((t,j)   => t.classList.toggle('active', j===i));
}}

// ── Panel 1 Chart ────────────────────────────────────────────────────────
(function() {{
  const ctx = document.getElementById('p1chart').getContext('2d');
  const datasets = {p1_datasets_js};
  datasets.push({{
    label: 'Completions',
    data: {p1_completions},
    type: 'line',
    yAxisID: 'yComp',
    borderColor: '#1e293b',
    backgroundColor: 'transparent',
    borderWidth: 2,
    pointRadius: 0,
    pointHoverRadius: 4,
    tension: 0.3,
    order: 0,
  }});
  new Chart(ctx, {{
    type: 'bar',
    data: {{ labels: {p1_labels}, datasets }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          mode: 'index', intersect: false,
          callbacks: {{
            label: (ctx) => {{
              if (ctx.dataset.type === 'line') return `Completions: ${{ctx.raw.toLocaleString()}}`;
              return `₹${{ctx.dataset.label.replace('₹','')}} rev: ₹${{ctx.raw.toLocaleString()}}`;
            }},
          }}
        }}
      }},
      scales: {{
        x: {{ stacked:true, ticks:{{ font:{{size:10}}, maxRotation:60, autoSkip:true, maxTicksLimit:30 }} }},
        y: {{
          stacked:true, position:'left',
          ticks:{{ callback: v => v>=100000 ? `₹${{(v/100000).toFixed(1)}}L` : `₹${{(v/1000).toFixed(0)}}K`, font:{{size:11}} }},
          title:{{ display:true, text:'Daily Revenue (₹)', font:{{size:11}} }},
        }},
        yComp: {{
          position:'right', grid:{{ drawOnChartArea:false }},
          ticks:{{ font:{{size:11}} }},
          title:{{ display:true, text:'Completions', font:{{size:11}} }},
        }},
      }},
    }},
  }});
}})();

// ── Panel 3 Chart — 3-bucket stacked (Completed / Insuff / Cancellations) ─
(function() {{
  const ctx = document.getElementById('p3chart').getContext('2d');
  const attempted = {p3_attempted};
  const compN = {p3_comp_n};
  const insN  = {p3_ins_n};
  const canN  = {p3_cancel_n};
  new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels: {p3_labels},
      datasets: [
        {{ label:'Completed',         data:{p3_comp},   backgroundColor:'#16a34a', stack:'s' }},
        {{ label:'Insufficient Funds',data:{p3_ins},    backgroundColor:'#ef4444', stack:'s' }},
        {{ label:'Cancellations',     data:{p3_cancel}, backgroundColor:'#94a3b8', stack:'s' }},
      ],
    }},
    options: {{
      responsive:true, maintainAspectRatio:false,
      plugins: {{
        legend:{{ position:'top', labels:{{font:{{size:12}}}} }},
        tooltip:{{
          mode:'index', intersect:false,
          callbacks:{{
            title: (items) => `Cohort ${{items[0].label}} — ${{attempted[items[0].dataIndex].toLocaleString()}} users`,
            label: (ctx) => {{
              const i = ctx.dataIndex;
              const n = [compN, insN, canN][ctx.datasetIndex][i];
              return `${{ctx.dataset.label}}: ${{n.toLocaleString()}} (${{ctx.raw}}%)`;
            }},
          }},
        }},
      }},
      scales: {{
        x:{{ stacked:true, ticks:{{ font:{{size:10}}, maxRotation:60, autoSkip:true, maxTicksLimit:30 }} }},
        y:{{ stacked:true, max:100,
             ticks:{{ callback: v => v+'%', font:{{size:11}} }},
             title:{{ display:true, text:'% of att1 attempts', font:{{size:11}} }},
        }},
      }},
    }},
  }});
}})();
</script>
</body>
</html>"""

out = os.path.join(_HERE, "index.html")
with open(out, "w") as f:
    f.write(html)

total_rev_all = sum(total_rev_d[d] for d in DATES)
print(f"→ {out}")
print(f"  Daily chart : {len(DATES)} dates, {len(p1_datasets)} amount buckets")
print(f"  Panel 1 tbl : {len(tbl_rows)} rows × {len(active_amts)+4} columns")
print(f"  Panel 3     : 3 buckets (Completed / Insuff Funds / Cancellations)")
print(f"  Total rev   : ₹{total_rev_all:,.0f}  |  Repeat rev: ₹{total_rep:,.0f}")
