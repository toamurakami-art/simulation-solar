import streamlit as st
import pandas as pd
import pulp

# ==========================================
# 🎁 究極版 v4.8: 制約条件に「投資回収年数(Payback Period)」を追加
# ==========================================
PV_PROFILE = {"1":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0,"30":0.0},"6":{"0":0.0,"30":0.0},"7":{"0":0.0061,"30":0.0365},"8":{"0":0.1186,"30":0.1608},"9":{"0":0.1946,"30":0.2156},"10":{"0":0.214,"30":0.2111},"11":{"0":0.1965,"30":0.1863},"12":{"0":0.185,"30":0.1863},"13":{"0":0.1798,"30":0.1751},"14":{"0":0.1634,"30":0.1445},"15":{"0":0.1144,"30":0.0616},"16":{"0":0.0238,"30":0.0016},"17":{"0":0.0,"30":0.0},"18":{"0":0.0,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"2":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0,"30":0.0},"6":{"0":0.0,"30":0.0078},"7":{"0":0.0574,"30":0.1268},"8":{"0":0.1946,"30":0.2279},"9":{"0":0.2484,"30":0.2586},"10":{"0":0.2526,"30":0.2465},"11":{"0":0.2296,"30":0.2153},"12":{"0":0.2157,"30":0.2206},"13":{"0":0.2177,"30":0.2221},"14":{"0":0.2133,"30":0.1978},"15":{"0":0.1708,"30":0.1333},"16":{"0":0.0938,"30":0.0282},"17":{"0":0.006,"30":0.0},"18":{"0":0.0,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"3":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0,"30":0.0019},"6":{"0":0.0225,"30":0.0685},"7":{"0":0.1444,"30":0.1905},"8":{"0":0.2252,"30":0.2471},"9":{"0":0.2583,"30":0.2626},"10":{"0":0.2556,"30":0.249},"11":{"0":0.2352,"30":0.2222},"12":{"0":0.2274,"30":0.2355},"13":{"0":0.2366,"30":0.2416},"14":{"0":0.2357,"30":0.2142},"15":{"0":0.1985,"30":0.1748},"16":{"0":0.1411,"30":0.0895},"17":{"0":0.0515,"30":0.0106},"18":{"0":0.0,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"4":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0003},"5":{"0":0.0098,"30":0.0346},"6":{"0":0.0923,"30":0.1263},"7":{"0":0.1572,"30":0.1759},"8":{"0":0.1927,"30":0.2018},"9":{"0":0.2013,"30":0.1969},"10":{"0":0.1852,"30":0.1739},"11":{"0":0.1573,"30":0.145},"12":{"0":0.1513,"30":0.1607},"13":{"0":0.1748,"30":0.1873},"14":{"0":0.1911,"30":0.1901},"15":{"0":0.1758,"30":0.158},"16":{"0":0.1403,"30":0.1152},"17":{"0":0.0892,"30":0.0347},"18":{"0":0.0108,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"5":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0004,"30":0.0094},"5":{"0":0.0535,"30":0.0813},"6":{"0":0.116,"30":0.1373},"7":{"0":0.1556,"30":0.1673},"8":{"0":0.1756,"30":0.1799},"9":{"0":0.1811,"30":0.1786},"10":{"0":0.1683,"30":0.1556},"11":{"0":0.1396,"30":0.1302},"12":{"0":0.1344,"30":0.1468},"13":{"0":0.159,"30":0.1702},"14":{"0":0.1727,"30":0.1715},"15":{"0":0.1683,"30":0.1569},"16":{"0":0.1439,"30":0.1293},"17":{"0":0.1108,"30":0.0809},"18":{"0":0.0423,"30":0.0076},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"6":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.002,"30":0.0089},"5":{"0":0.0383,"30":0.055},"6":{"0":0.0767,"30":0.0928},"7":{"0":0.1108,"30":0.1248},"8":{"0":0.1383,"30":0.1476},"9":{"0":0.1565,"30":0.161},"10":{"0":0.1547,"30":0.1458},"11":{"0":0.1348,"30":0.1264},"12":{"0":0.1305,"30":0.1409},"13":{"0":0.148,"30":0.1524},"14":{"0":0.1529,"30":0.1512},"15":{"0":0.1474,"30":0.1368},"16":{"0":0.1308,"30":0.1131},"17":{"0":0.0946,"30":0.0668},"18":{"0":0.048,"30":0.0132},"19":{"0":0.0042,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"7":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0001,"30":0.0039},"5":{"0":0.0261,"30":0.0378},"6":{"0":0.0574,"30":0.0728},"7":{"0":0.0911,"30":0.1044},"8":{"0":0.1224,"30":0.1337},"9":{"0":0.1418,"30":0.1452},"10":{"0":0.1435,"30":0.1386},"11":{"0":0.1316,"30":0.1231},"12":{"0":0.1261,"30":0.1357},"13":{"0":0.1444,"30":0.1498},"14":{"0":0.1507,"30":0.1498},"15":{"0":0.1512,"30":0.1417},"16":{"0":0.132,"30":0.1067},"17":{"0":0.0908,"30":0.0623},"18":{"0":0.0449,"30":0.012},"19":{"0":0.0041,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"8":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0006},"5":{"0":0.0107,"30":0.0279},"6":{"0":0.055,"30":0.0728},"7":{"0":0.0945,"30":0.109},"8":{"0":0.1296,"30":0.1435},"9":{"0":0.1527,"30":0.157},"10":{"0":0.1548,"30":0.1486},"11":{"0":0.1374,"30":0.1274},"12":{"0":0.1286,"30":0.1324},"13":{"0":0.1409,"30":0.1448},"14":{"0":0.1485,"30":0.1488},"15":{"0":0.1401,"30":0.1276},"16":{"0":0.1115,"30":0.0947},"17":{"0":0.0777,"30":0.0493},"18":{"0":0.0248,"30":0.0035},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"9":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0001,"30":0.0105},"6":{"0":0.0536,"30":0.0878},"7":{"0":0.1222,"30":0.1433},"8":{"0":0.1621,"30":0.1727},"9":{"0":0.1688,"30":0.1635},"10":{"0":0.1554,"30":0.1454},"11":{"0":0.1316,"30":0.1263},"12":{"0":0.1296,"30":0.133},"13":{"0":0.1408,"30":0.1428},"14":{"0":0.1442,"30":0.1387},"15":{"0":0.1266,"30":0.1052},"16":{"0":0.0875,"30":0.0586},"17":{"0":0.0298,"30":0.0064},"18":{"0":0.0011,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"10":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0,"30":0.0002},"6":{"0":0.015,"30":0.0592},"7":{"0":0.1208,"30":0.1456},"8":{"0":0.1645,"30":0.1736},"9":{"0":0.1762,"30":0.1727},"10":{"0":0.161,"30":0.149},"11":{"0":0.1313,"30":0.1286},"12":{"0":0.1333,"30":0.1373},"13":{"0":0.1523,"30":0.1631},"14":{"0":0.1527,"30":0.1393},"15":{"0":0.1248,"30":0.0977},"16":{"0":0.0643,"30":0.0154},"17":{"0":0.0019,"30":0.0},"18":{"0":0.0,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"11":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0,"30":0.0},"6":{"0":0.0,"30":0.0072},"7":{"0":0.0444,"30":0.101},"8":{"0":0.139,"30":0.1562},"9":{"0":0.1626,"30":0.1623},"10":{"0":0.153,"30":0.143},"11":{"0":0.1284,"30":0.128},"12":{"0":0.128,"30":0.1276},"13":{"0":0.1279,"30":0.1261},"14":{"0":0.1132,"30":0.0946},"15":{"0":0.0725,"30":0.026},"16":{"0":0.0085,"30":0.0},"17":{"0":0.0,"30":0.0},"18":{"0":0.0,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}},"12":{"0":{"0":0.0,"30":0.0},"1":{"0":0.0,"30":0.0},"2":{"0":0.0,"30":0.0},"3":{"0":0.0,"30":0.0},"4":{"0":0.0,"30":0.0},"5":{"0":0.0,"30":0.0},"6":{"0":0.0,"30":0.0},"7":{"0":0.009,"30":0.0406},"8":{"0":0.106,"30":0.136},"9":{"0":0.155,"30":0.1677},"10":{"0":0.1667,"30":0.1633},"11":{"0":0.1529,"30":0.1509},"12":{"0":0.153,"30":0.154},"13":{"0":0.146,"30":0.1385},"14":{"0":0.1252,"30":0.1021},"15":{"0":0.079,"30":0.0198},"16":{"0":0.0012,"30":0.0},"17":{"0":0.0,"30":0.0},"18":{"0":0.0,"30":0.0},"19":{"0":0.0,"30":0.0},"20":{"0":0.0,"30":0.0},"21":{"0":0.0,"30":0.0},"22":{"0":0.0,"30":0.0},"23":{"0":0.0,"30":0.0}}}

def get_default_pv(df_demand):
    pv_gen = []
    for _, row in df_demand.iterrows():
        m = str(int(row['M']))
        h = str(int(row['H']))
        mn = str(int(row['Min']))
        val = PV_PROFILE.get(m, {}).get(h, {}).get(mn, 0.0)
        pv_gen.append(val)
    df_pv = df_demand[['M', 'D', 'H', 'Min']].copy()
    df_pv['PV_Gen_1kW_kWh'] = pv_gen
    return df_pv

def get_template_csv():
    cols = ["利用日"] + [f"{h}:{m:02d}" for h in range(24) for m in (0, 30)]
    df_template = pd.DataFrame(columns=cols)
    df_template.loc[0] = ["2024/01/01"] + [0.0] * 48
    return df_template.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

# ==========================================
# 先に減価償却の関数を定義（AIが計算に使うため）
# ==========================================
def calc_depreciation_200db(cost, years):
    if years == 1: return [cost] + [0] * 29 
    tax_rates = { 7: {'r': 0.286, 'r_rev': 0.334, 'g': 0.07115}, 10: {'r': 0.200, 'r_rev': 0.250, 'g': 0.06552}, 17: {'r': 0.118, 'r_rev': 0.125, 'g': 0.04648} }
    rates = tax_rates.get(years, {'r': 2.0/years, 'r_rev': 2.0/years, 'g': 0})
    deps, balance = [], cost
    guarantee = cost * rates['g']
    switched, revised_cost = False, 0
    for y in range(1, 31):
        if y <= years:
            if not switched:
                d = balance * rates['r']
                if d < guarantee:
                    switched, revised_cost = True, balance
                    d = revised_cost * rates['r_rev']
            else: d = revised_cost * rates['r_rev']
            if y == years: d = balance - 1
            if d > balance: d = balance - 1
            deps.append(d)
            balance -= d
        else: deps.append(0)
    return deps

def get_payback_years(capex, cf_list):
    if capex <= 0: return 0.0
    for y in range(30):
        if cf_list[y] >= capex:
            if y == 0: return capex / cf_list[y] if cf_list[y] > 0 else 0
            else:
                prev_cf = cf_list[y-1]
                this_year_cf = cf_list[y] - prev_cf
                return y + ((capex - prev_cf) / this_year_cf if this_year_cf > 0 else 0)
    return None

def read_csv_robust(file, header_val=None):
    file.seek(0)
    try: return pd.read_csv(file, header=header_val, encoding='utf-8')
    except Exception:
        file.seek(0)
        try: return pd.read_csv(file, header=header_val, encoding='cp932')
        except Exception:
            file.seek(0)
            return pd.read_csv(file, header=header_val, encoding='shift_jis', errors='replace')


# ==========================================
# 2. 最適化エンジン (PuLP) - 投資回収年数の逆算を実装！
# ==========================================
def optimize_system(df, params):
    Y = params['years']
    T = len(df)
    
    demand_list = df['Demand_kWh'].tolist()
    pv_gen_list = df['PV_Gen_1kW_kWh'].tolist()
    
    prob = pulp.LpProblem("Energy_Optimization", pulp.LpMinimize)
    X_pv = pulp.LpVariable('X_pv', lowBound=0, cat='Continuous')
    X_bat = pulp.LpVariable('X_bat', lowBound=0, cat='Continuous')
    
    E_buy = [pulp.LpVariable(f'E_buy_{t}', lowBound=0) for t in range(T)]
    E_pv_use = [pulp.LpVariable(f'E_pv_use_{t}', lowBound=0) for t in range(T)]
    E_charge = [pulp.LpVariable(f'E_charge_{t}', lowBound=0) for t in range(T)]
    E_discharge = [pulp.LpVariable(f'E_discharge_{t}', lowBound=0) for t in range(T)]
    S = [pulp.LpVariable(f'S_{t}', lowBound=0) for t in range(T)]
    
    capex = params['cost_pv_net'] * X_pv + params['cost_bat_net'] * X_bat
    price_unit = params['price_base'] + params['adj_fuel'] + params['surcharge']
    opex_energy = Y * pulp.lpSum([price_unit * E_buy[t] for t in range(T)])
    
    capex_gross_var = params['cost_pv_gross'] * X_pv + params['cost_bat_gross'] * X_bat
    om_total = Y * capex_gross_var * params['om_rate']
    pcs_total = capex_gross_var * params['pcs_rate'] if Y >= params['pcs_year'] else 0
    disp_total = capex_gross_var * params['disp_rate']
    
    # 目的関数（トータルコストの最小化）
    prob += capex + opex_energy + om_total + pcs_total + disp_total
    eta_c, eta_d = params['eff_charge'], params['eff_discharge']
    
    # 💡 ユーザーが指定した「絶対守るべき制約」
    if params.get('fix_pv_kw') is not None:
        prob += X_pv == params['fix_pv_kw']
        
    if params.get('max_capex_man') is not None:
        prob += capex <= params['max_capex_man'] * 10000

    annual_demand_kwh = sum(demand_list)
    base_cost_yr1 = annual_demand_kwh * price_unit

    if params.get('min_reduction_rate') is not None:
        target_opex_yr1_rate = base_cost_yr1 * (1.0 - params['min_reduction_rate'] / 100.0)
        prob += pulp.lpSum([price_unit * E_buy[t] for t in range(T)]) <= target_opex_yr1_rate

    if params.get('min_reduction_amount_man') is not None:
        target_opex_yr1_amount = base_cost_yr1 - (params['min_reduction_amount_man'] * 10000)
        prob += pulp.lpSum([price_unit * E_buy[t] for t in range(T)]) <= target_opex_yr1_amount

    # 💡 新規追加: 「指定年数以内に初期投資を全額回収する」という超高度な制約
    if params.get('max_payback_years') is not None:
        target_year = int(params['max_payback_years'])
        dep_fracs = calc_depreciation_200db(1.0, params['dep_years'])
        
        total_savings = 0
        total_cost = 0
        total_tax_shield = 0
        
        annual_gen_1kw = sum(pv_gen_list)
        capex_n = params['cost_pv_net'] * X_pv + params['cost_bat_net'] * X_bat
        capex_g = params['cost_pv_gross'] * X_pv + params['cost_bat_gross'] * X_bat
        cost_with_pv_yr1 = pulp.lpSum([price_unit * E_buy[t] for t in range(T)])
        savings_yr1_expr = base_cost_yr1 - cost_with_pv_yr1
        
        for y in range(1, target_year + 1):
            deg_loss_kwh = annual_gen_1kw * X_pv * 0.004 * (y - 1)
            savings_y = savings_yr1_expr - deg_loss_kwh * price_unit
            total_savings += savings_y
            
            cost_y = capex_g * params['om_rate']
            if y == params['pcs_year']:
                cost_y += capex_g * params['pcs_rate']
            if y == min(params['years'], 30):
                cost_y += capex_g * params['disp_rate']
            total_cost += cost_y
            
            dep_y = dep_fracs[y-1] * capex_n
            tax_shield_y = (dep_y + cost_y) * params['tax_rate']
            total_tax_shield += tax_shield_y
            
        # N年間の「削減額 - 維持経費 + 節税効果」の合計が、初期投資額以上になること！
        prob += (total_savings - total_cost + total_tax_shield) >= capex_n

    for t in range(T):
        prob += demand_list[t] == E_pv_use[t] + E_discharge[t] + E_buy[t]
        prob += E_pv_use[t] + E_charge[t] <= pv_gen_list[t] * X_pv
        if t == 0:
            prob += S[t] == E_charge[t] * eta_c - (E_discharge[t] / eta_d)
        else:
            prob += S[t] == S[t-1] + E_charge[t] * eta_c - (E_discharge[t] / eta_d)
        prob += S[t] <= X_bat
        
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return {
        'Status': pulp.LpStatus[prob.status],
        'Optimal_PV_kW': pulp.value(X_pv),
        'Optimal_Bat_kWh': pulp.value(X_bat),
        'Total_Cost': pulp.value(prob.objective)
    }, prob

# ==========================================
# 3. UI設定 (Streamlit)
# ==========================================
st.set_page_config(page_title="最適容量シミュレーター v4.8", layout="wide")
st.title("🌱 再エネ・蓄電池 最適容量シミュレーター")

with st.sidebar:
    st.header("⚙️ 条件設定")
    st.subheader("1. 導入コスト・補助金")
    cost_pv_man = st.number_input("太陽光パネル単価 (万円/kW)", value=30.0, step=1.0)
    sub_pv_man = st.number_input("太陽光パネル補助金 (万円/kW)", value=15.0, step=1.0)
    cost_bat_man = st.number_input("蓄電池単価 (万円/kWh)", value=10.0, step=1.0)
    sub_bat_man = st.number_input("蓄電池補助金 (万円/kWh)", value=5.0, step=1.0)
    
    st.subheader("2. 電気料金プラン (高圧)")
    price_base = st.number_input("電力量単価 (円/kWh)", value=20.0, step=0.5)
    surcharge = st.number_input("再エネ賦課金 (円/kWh)", value=3.49, step=0.1)
    adj_fuel = st.number_input("燃料費調整額 (円/kWh)", value=0.0, step=0.1)
    
    st.subheader("3. 減価償却・税効果")
    dep_years = st.selectbox("償却期間 (年)", [1, 7, 10, 17], index=3)
    tax_rate = st.number_input("法人実効税率 (%)", value=30.0, step=1.0)
    
    st.subheader("4. 評価期間")
    st.subheader("4. 事業計画の評価期間")
    years = st.slider(
        "コスパを判断する基準年数", 
        10, 30, 20,
        help="短くすると「早期回収」を優先した手堅い小型システムになり、長くすると「生涯の総利益」を最大化するシステムを提案します。"
    )
    
    # 💡 新規追加：選んだ年数によって、AIの戦略を画面に分かりやすく表示！
    if years <= 15:
        st.success("💡 **【短期回収・低リスク重視 モード】**\n初期費用を極力抑え、最速で投資回収できる手堅い容量を計算します。")
    elif years >= 25:
        st.warning("💡 **【長期利益・環境価値重視 モード】**\n初期費用はかかりますが、生涯の電気代削減額とCO2削減量が最大になる大容量を計算します。")
    else:
        st.info("💡 **【バランス型（標準） モード】**\n一般的な設備の寿命（20年）に合わせた、投資回収と総利益のバランスが最も良い容量を計算します。")
    
    st.subheader("5. 将来の維持・廃棄コスト")
    om_rate_input = st.number_input("年間O&M費用 (初期費用の%)", value=0.0, step=0.1)
    pcs_rate_input = st.number_input("パワコン交換費用 (初期費用の%)", value=0.0, step=1.0)
    pcs_year_input = st.number_input("パワコン交換時期 (年目)", value=0, step=1)
    disp_rate_input = st.number_input("産廃・廃棄費用 (初期費用の%)", value=0.0, step=0.5)

    st.subheader("6. 詳細な制約条件（オプション）")
    use_fix_pv = st.checkbox("📌 太陽光パネル容量を固定する")
    fix_pv_kw = st.number_input("指定パネル容量 (kW)", value=50.0, step=5.0) if use_fix_pv else None
    
    use_max_capex = st.checkbox("💰 初期投資額（実質）の上限を設ける")
    max_capex_man = st.number_input("上限額 (万円)", value=1000.0, step=100.0) if use_max_capex else None
    
    use_min_reduction = st.checkbox("📉 目標の電気代削減率をクリアする")
    min_reduction_rate = st.number_input("最低目標削減率 (%)", value=30.0, step=5.0) if use_min_reduction else None

    use_min_reduction_amount = st.checkbox("💴 目標の電気代削減額をクリアする")
    min_reduction_amount_man = st.number_input("最低目標削減額 (万円/年)", value=100.0, step=10.0) if use_min_reduction_amount else None

    # 💡 新規追加: 回収年数の縛り
    use_max_payback = st.checkbox("⏳ 目標の投資回収年数をクリアする")
    max_payback_years = st.number_input("目標回収年数 (年以内)", value=10, step=1, min_value=1, max_value=30) if use_max_payback else None


params = {
    'cost_pv_gross': cost_pv_man * 10000, 'cost_bat_gross': cost_bat_man * 10000,
    'cost_pv_net': (cost_pv_man - sub_pv_man) * 10000, 'cost_bat_net': (cost_bat_man - sub_bat_man) * 10000,
    'price_base': price_base, 'surcharge': surcharge, 'adj_fuel': adj_fuel,
    'years': years, 'dep_years': dep_years, 'tax_rate': tax_rate / 100.0,
    'eff_charge': 0.95, 'eff_discharge': 0.95,
    'om_rate': om_rate_input / 100.0, 'pcs_rate': pcs_rate_input / 100.0,
    'pcs_year': int(pcs_year_input), 'disp_rate': disp_rate_input / 100.0,
    'fix_pv_kw': fix_pv_kw, 'max_capex_man': max_capex_man, 'min_reduction_rate': min_reduction_rate,
    'min_reduction_amount_man': min_reduction_amount_man,
    'max_payback_years': max_payback_years
}

# ==========================================
# 4. メイン画面 (データのアップロード)
# ==========================================
st.subheader("📂 デマンドデータの準備とアップロード")
st.markdown("各電力会社のデータ形式がバラバラな場合は、以下の**専用テンプレート**をダウンロードして数値を貼り付けてからアップロードしてください。")

st.download_button(
    label="📥 デマンド入力用テンプレート(CSV)をダウンロード",
    data=get_template_csv(),
    file_name="demand_template.csv",
    mime="text/csv",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    demand_file = st.file_uploader("1. デマンドデータ (Excel/CSV) ※必須", type=['xlsx', 'xls', 'csv'])
with col2:
    pv_files = st.file_uploader("2. 発電量データ (CSV) ※任意・なしでOK", type=['csv'], accept_multiple_files=True)

if demand_file:
    with st.spinner('データを抽出しています...'):
        try:
            if demand_file.name.lower().endswith('.csv'):
                df_demand_raw = read_csv_robust(demand_file, header_val=None)
            else:
                demand_file.seek(0)
                df_demand_raw = pd.read_excel(demand_file, header=None)
                
            start_row, date_col_idx = 0, 0
            target_keywords = ['利用日', '日付', '対象日', '年月日', 'Date', 'date']
            found = False
            for i in range(len(df_demand_raw)):
                row_vals = [str(val).strip() for val in df_demand_raw.iloc[i].values]
                for kw in target_keywords:
                    if kw in row_vals:
                        start_row = i
                        date_col_idx = row_vals.index(kw)
                        found = True
                        break
                if found: break
            
            if not found:
                st.error("エラー：データ内に日付の列が見つかりません。専用テンプレートを使用してアップロードしてください。")
            else:
                times = df_demand_raw.iloc[start_row, date_col_idx+1:].values
                df_demand_data = df_demand_raw.iloc[start_row+1:, date_col_idx:].copy()
                df_demand_data.columns = ['Date'] + list(times)
                df_demand_data = df_demand_data.dropna(subset=['Date'])
                
                df_melt = df_demand_data.melt(id_vars=['Date'], var_name='Time', value_name='Demand_kWh')
                df_melt['Demand_kWh'] = pd.to_numeric(df_melt['Demand_kWh'], errors='coerce')
                df_melt['Date_str'] = pd.to_datetime(df_melt['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
                df_melt['Time_str'] = df_melt['Time'].astype(str)
                df_melt['日時'] = pd.to_datetime(df_melt['Date_str'] + ' ' + df_melt['Time_str'], errors='coerce')
                df_demand = df_melt.dropna(subset=['日時']).sort_values('日時').reset_index(drop=True)
                
                df_demand['M'] = df_demand['日時'].dt.month
                df_demand['D'] = df_demand['日時'].dt.day
                df_demand['H'] = df_demand['日時'].dt.hour
                df_demand['Min'] = df_demand['日時'].dt.minute
                
                if pv_files and len(pv_files) > 0:
                    pv_dfs = []
                    for pf in pv_files:
                        pf.seek(0)
                        try: df_pv_raw = pd.read_csv(pf, header=0, encoding='utf-8')
                        except:
                            pf.seek(0)
                            try: df_pv_raw = pd.read_csv(pf, header=0, encoding='cp932')
                            except:
                                pf.seek(0)
                                df_pv_raw = pd.read_csv(pf, header=0, encoding='shift_jis', errors='replace')
                        if 'kWh' in str(df_pv_raw.iloc[0].values): df_pv_data = df_pv_raw.iloc[1:].copy()
                        else: df_pv_data = df_pv_raw.copy()
                        
                        target_col = [c for c in df_pv_data.columns if '定格比' in str(c) and '発電' in str(c)]
                        target_col = target_col[0] if len(target_col) > 0 else df_pv_data.columns[-1]
                        pv_gen = pd.to_numeric(df_pv_data[target_col], errors='coerce')
                        col_m = '#月' if '#月' in df_pv_data.columns else df_pv_data.columns[0]
                        col_d = '日' if '日' in df_pv_data.columns else df_pv_data.columns[1]
                        col_h = '時' if '時' in df_pv_data.columns else df_pv_data.columns[2]
                        col_min = '分' if '分' in df_pv_data.columns else df_pv_data.columns[3]
                        
                        pv_dfs.append(pd.DataFrame({
                            'PV_Gen_1kW_kWh': pv_gen.values, 'M': pd.to_numeric(df_pv_data[col_m], errors='coerce').values,
                            'D': pd.to_numeric(df_pv_data[col_d], errors='coerce').values, 'H': pd.to_numeric(df_pv_data[col_h], errors='coerce').values,
                            'Min': pd.to_numeric(df_pv_data[col_min], errors='coerce').values
                        }))
                    df_pv_combined = pd.concat(pv_dfs)
                    df_pv = df_pv_combined.groupby(['M', 'D', 'H', 'Min'], as_index=False)['PV_Gen_1kW_kWh'].mean()
                    st.success(f"✅ デマンドと【手動アップロードしたPVデータ】を結合しました！")
                else:
                    df_pv = get_default_pv(df_demand)
                    st.info("💡 発電量データなし：【内蔵のオリジナル高精度PVカーブ】を自動適用しました！")
                    
                df = pd.merge(df_demand, df_pv, on=['M', 'D', 'H', 'Min'], how='inner')
            
        except Exception as e:
            st.error(f"データの解析中にエラーが発生しました。({str(e)})")
            df = pd.DataFrame()

    if len(df) > 0:
        if st.button("🚀 制約条件を守って最適解を計算", type="primary"):
            with st.spinner('最適解を計算中... (糖分足りないよ～( ;∀;))'):
                results, prob = optimize_system(df, params)
                
            if results['Status'] == 'Infeasible':
                st.error("❌ 【解なし】指定された制約条件が厳しすぎます。（例：目標回収年数が短すぎる、など）")
                st.warning("サイドバーの「6. 詳細な制約条件」の数値を緩めるか、チェックを外して再度お試しください。")
            elif results['Status'] == 'Optimal':
                st.markdown("---")
                opt_pv = results['Optimal_PV_kW']
                opt_bat = results['Optimal_Bat_kWh']
                
                capex_gross = params['cost_pv_gross'] * opt_pv + params['cost_bat_gross'] * opt_bat
                capex_net = params['cost_pv_net'] * opt_pv + params['cost_bat_net'] * opt_bat
                
                price_unit = params['price_base'] + params['adj_fuel'] + params['surcharge']
                annual_demand_kwh = df['Demand_kWh'].sum()
                cost_without_yr1 = annual_demand_kwh * price_unit
                
                var_dict = prob.variablesDict()
                e_buy_yr1 = sum((var_dict[f'E_buy_{t}'].varValue or 0.0) for t in range(len(df)))
                e_pv_use_yr1 = sum((var_dict[f'E_pv_use_{t}'].varValue or 0.0) for t in range(len(df)))
                e_charge_yr1 = sum((var_dict[f'E_charge_{t}'].varValue or 0.0) for t in range(len(df)))
                
                cost_with_yr1 = e_buy_yr1 * price_unit
                savings_yr1 = cost_without_yr1 - cost_with_yr1
                annual_gen_yr1 = df['PV_Gen_1kW_kWh'].sum() * opt_pv
                
                self_sufficiency = (1 - (e_buy_yr1 / annual_demand_kwh)) * 100 if annual_demand_kwh > 0 else 0
                reduction_rate = (savings_yr1 / cost_without_yr1) * 100 if cost_without_yr1 > 0 else 0
                co2_reduction_tons = (annual_demand_kwh - e_buy_yr1) * 0.433 / 1000
                
                curtailed_pv = max(0, annual_gen_yr1 - (e_pv_use_yr1 + e_charge_yr1))
                loss_rate = (curtailed_pv / annual_gen_yr1) * 100 if annual_gen_yr1 > 0 else 0
                effective_gen_yr1 = annual_gen_yr1 - curtailed_pv
                
                deps_gross = calc_depreciation_200db(capex_gross, params['dep_years'])
                deps_net = calc_depreciation_200db(capex_net, params['dep_years'])
                
                om_cost = capex_gross * params['om_rate']
                pcs_cost = capex_gross * params['pcs_rate']
                disp_cost = capex_gross * params['disp_rate']
                disp_year = min(params['years'], 30)
                
                cf_gross, cf_net, cum_gross, cum_net = [], [], 0, 0
                cf_summary = []
                
                for y in range(1, 31):
                    deg_loss_kwh = annual_gen_yr1 * 0.004 * (y - 1)
                    gen_y = annual_gen_yr1 - deg_loss_kwh
                    savings_y = savings_yr1 - (deg_loss_kwh * price_unit)
                    
                    cost_y = om_cost
                    if y == params['pcs_year']: cost_y += pcs_cost
                    if y == disp_year: cost_y += disp_cost
                    
                    tax_shield_gross = (deps_gross[y-1] + cost_y) * params['tax_rate']
                    tax_shield_net = (deps_net[y-1] + cost_y) * params['tax_rate']
                    
                    cum_gross += (savings_y - cost_y + tax_shield_gross)
                    cum_net += (savings_y - cost_y + tax_shield_net)
                    
                    cf_gross.append(cum_gross)
                    cf_net.append(cum_net)
                    
                    cf_summary.append({
                        "経過年数(年)": y,
                        "想定発電量_経年劣化後(kWh)": round(gen_y),
                        "電気代削減額(円)": round(savings_y),
                        "維持メンテ・廃棄経費(円)": round(cost_y),
                        "減価償却費_補助金あり適用(円)": round(deps_net[y-1]),
                        "節税効果_補助金あり(円)": round(tax_shield_net),
                        "単年キャッシュフロー_補助金あり(円)": round(savings_y - cost_y + tax_shield_net),
                        "累計回収額_補助金あり(円)": round(cum_net),
                        "節税効果_補助金なし自己負担(円)": round(tax_shield_gross),
                        "単年キャッシュフロー_補助金なし(円)": round(savings_y - cost_y + tax_shield_gross),
                        "累計回収額_補助金なし(円)": round(cum_gross)
                    })
                
                pb_net = get_payback_years(capex_net, cf_net)
                pb_str_net = f"約 {pb_net:.1f} 年" if pb_net is not None else "30年超 (回収不可)"
                pb_gross = get_payback_years(capex_gross, cf_gross)
                pb_str_gross = f"約 {pb_gross:.1f} 年" if pb_gross is not None else "30年超 (回収不可)"
                
                # ==== 結果表示 ====
                st.header("📊 システム構成と年間発電量")
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("🏭 年間消費電力", f"{annual_demand_kwh:,.0f} kWh")
                c2.metric("🌞 最適太陽光容量", f"{opt_pv:,.1f} kW")
                c3.metric("🔋 最適蓄電池容量", f"{opt_bat:,.1f} kWh")
                c4.metric("⚡ 初年度想定発電量", f"{annual_gen_yr1:,.0f} kWh")
                c5.metric("✅ 有効発電量", f"{effective_gen_yr1:,.0f} kWh", "ロス分を除いた実利用量")
                
                st.markdown("---")
                st.header("💡 導入効果と運用効率 (初年度)")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("📉 電気代 削減率", f"{reduction_rate:.1f} %", f"年間 約{savings_yr1/10000:,.0f}万円の削減")
                m2.metric("🌱 電力自給率", f"{self_sufficiency:.1f} %", "消費電力のうち自前で賄う割合")
                m3.metric("⚠️ 発電ロス率 (出力抑制)", f"{loss_rate:.1f} %", "使いきれずに捨てられた電気の割合")
                m4.metric("🌍 CO2 削減量", f"{co2_reduction_tons:,.1f} t-CO2", "※排出係数 0.433kg/kWhで試算")
                
                st.markdown("---")
                st.header("🔧 将来の維持管理・廃棄コスト (目安)")
                st.info("※設備本体総額(グロス)を基準に算出。これらのコストは全て下記の回収シミュレーションのマイナス要素として計算済です。")
                o1, o2, o3 = st.columns(3)
                o1.metric("🛠 年間O&M費用 (メンテ等)", f"約 {om_cost/10000:,.0f} 万円/年", f"初期総額の{params['om_rate']*100:.1f}%")
                o2.metric(f"🔄 パワコン交換費用 ({params['pcs_year']}年目)", f"約 {pcs_cost/10000:,.0f} 万円", f"初期総額の{params['pcs_rate']*100:.1f}%")
                o3.metric(f"🗑 産廃・廃棄費用 ({disp_year}年目)", f"約 {disp_cost/10000:,.0f} 万円", f"初期総額の{params['disp_rate']*100:.1f}%")

                st.markdown("---")
                st.header("📈 投資回収シミュレーション (補助金 あり/なし 比較)")
                st.info(f"※経年劣化（年0.4%低下）、維持管理費・廃棄費、および{params['dep_years']}年間の200%定率法による減価償却（法人税{params['tax_rate']*100:.0f}%）をすべて考慮した手残り現金(累計)です。")
                
                col_left, col_right = st.columns(2)
                with col_left:
                    st.subheader("🟢 補助金【あり】の場合")
                    st.metric("初期投資額 (実質)", f"{capex_net/10000:,.0f} 万円")
                    st.metric("🎯 投資回収年数", pb_str_net)
                    st.markdown("##### 累計回収額・回収率")
                    roi_7_net = (cf_net[6] / capex_net * 100) if capex_net > 0 else 0
                    roi_20_net = (cf_net[19] / capex_net * 100) if capex_net > 0 else 0
                    roi_30_net = (cf_net[29] / capex_net * 100) if capex_net > 0 else 0
                    st.write(f"**7年後:** {cf_net[6]/10000:,.0f} 万円 (回収率: {roi_7_net:,.0f}%)")
                    st.write(f"**20年後:** {cf_net[19]/10000:,.0f} 万円 (回収率: {roi_20_net:,.0f}%)")
                    st.write(f"**30年後:** {cf_net[29]/10000:,.0f} 万円 (回収率: {roi_30_net:,.0f}%)")
                
                with col_right:
                    st.subheader("🔴 補助金【なし】の場合")
                    st.metric("初期投資額 (全額自己負担)", f"{capex_gross/10000:,.0f} 万円")
                    st.metric("🎯 投資回収年数", pb_str_gross)
                    st.markdown("##### 累計回収額・回収率")
                    roi_7_gross = (cf_gross[6] / capex_gross * 100) if capex_gross > 0 else 0
                    roi_20_gross = (cf_gross[19] / capex_gross * 100) if capex_gross > 0 else 0
                    roi_30_gross = (cf_gross[29] / capex_gross * 100) if capex_gross > 0 else 0
                    st.write(f"**7年後:** {cf_gross[6]/10000:,.0f} 万円 (回収率: {roi_7_gross:,.0f}%)")
                    st.write(f"**20年後:** {cf_gross[19]/10000:,.0f} 万円 (回収率: {roi_20_gross:,.0f}%)")
                    st.write(f"**30年後:** {cf_gross[29]/10000:,.0f} 万円 (回収率: {roi_30_gross:,.0f}%)")

                st.markdown("---")
                st.subheader("📥 シミュレーション結果の出力")
                df_cf_export = pd.DataFrame(cf_summary)
                csv_data = df_cf_export.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                
                st.download_button(
                    label="📊 30年間のキャッシュフロー表をCSVでダウンロード",
                    data=csv_data,
                    file_name="simulation_cashflow.csv",
                    mime="text/csv",
                    type="primary"
                )

            else:
                st.error("最適化中に予期せぬエラーが発生しました。条件を見直してください。")
