import streamlit as st
import requests
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

st.set_page_config(
    page_title="IL Calculator - 80/20 Pool",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def calculate_impermanent_loss_80_20(p0_a, p0_b, p1_a, p1_b):
    price_change_a = p1_a / p0_a
    price_change_b = p1_b / p0_b
    
    w_a = 0.8
    w_b = 0.2
    
    pool_value_ratio = (price_change_a ** w_a) * (price_change_b ** w_b)
    
    hold_value_ratio = (price_change_a * w_a) + (price_change_b * w_b)
    
    il_ratio = pool_value_ratio / hold_value_ratio
    il_percentage = (il_ratio - 1) * 100
    
    return il_percentage, pool_value_ratio

def get_initia_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'initia',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'initia' in data:
                price = data['initia']['usd']
                change_24h = data['initia'].get('usd_24h_change', 0)
                last_updated = data['initia'].get('last_updated_at', int(time.time()))
                return price, change_24h, last_updated
        
        return None, None, None
    except Exception as e:
        st.error(f"Error fetching Initia price: {str(e)}")
        return None, None, None

def create_il_chart(scenarios, il_values, title):
    return None

def create_price_impact_surface():
    price_multipliers = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0, 20.0]
    
    x, y, z = [], [], []
    
    for mult_a in price_multipliers:
        for mult_b in price_multipliers:
            il, _ = calculate_impermanent_loss_80_20(1.0, 1.0, mult_a, mult_b)
            il = abs(il)  # Make IL always positive for display
            x.append(mult_a)
            y.append(mult_b)
            z.append(il)
    
    fig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=4,
            color=z,
            colorscale='Reds',
            colorbar=dict(title=dict(text="IL %", font=dict(size=16)), titlefont=dict(size=16), tickfont=dict(size=14)),
            opacity=0.8
        ),
        hovertemplate='Asset A: %{x:.2f}x<br>Asset B: %{y:.2f}x<br>IL: %{z:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text="Impermanent Loss Surface (80/20 Pool)", font=dict(size=24, color='white')),
        scene=dict(
            xaxis_title="Asset A Price Multiplier",
            yaxis_title="Asset B Price Multiplier", 
            zaxis_title="Impermanent Loss (%)",
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(titlefont=dict(size=16), tickfont=dict(size=14)),
            yaxis=dict(titlefont=dict(size=16), tickfont=dict(size=14)),
            zaxis=dict(titlefont=dict(size=16), tickfont=dict(size=14))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=16),
        height=600
    )
    
    return fig

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .price-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .warning-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #000;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.2);
    }
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #000;
        box-shadow: 0 4px 15px rgba(168, 237, 234, 0.2);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .stSelectbox label, .stNumberInput label, .stSlider label {
        font-weight: 600;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🔄 Impermanent Loss Calculator</h1>
    <h3>80/20 Pool Analysis Tool</h3>
    <p>Calculate impermanent loss for concentrated liquidity pools with 80/20 weight distribution</p>
    <div style="margin-top: 15px; padding: 8px 15px; background: rgba(0,0,0,0.7); border-radius: 8px; font-size: 16px;">
        <span style="color: white;">💝 Donate: </span>
        <span style="color: #ffeb3b;">Initia:</span> <code style="color: #ffffff; background: #000000; padding: 3px 6px; border-radius: 4px; font-size: 14px; font-weight: bold;">init1rvsfu3cscp9xelq35r2dmy0gqykdt6yjmpdtn5</code> | 
        <span style="color: #ffeb3b;">EVM:</span> <code style="color: #ffffff; background: #000000; padding: 3px 6px; border-radius: 4px; font-size: 14px; font-weight: bold;">0x1b209e4710C04A6cfc11A0D4dD91E8012cd5e892</code>
    </div>
</div>
""", unsafe_allow_html=True)

tab1 = st.tabs(["🪙 Initia/USDC Analysis"])[0]

with tab1:
    st.header("General 80/20 LP Impermanent Loss Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏁 Initial Prices")
        initial_price_a = st.number_input("Initial Price Asset A ($)", value=0.5, min_value=0.0001, step=0.0001, key="init_a")
        initial_price_b = st.number_input("Initial Price Asset B ($)", value=1.0, min_value=0.01, step=0.01, key="init_b")
    
    with col2:
        st.subheader("🎯 Future Prices")
        future_price_a = st.number_input("Future Price Asset A ($)", value=1.0, min_value=0.0001, step=0.0001, key="future_a")
        future_price_b = st.number_input("Future Price Asset B ($)", value=1.0, min_value=0.01, step=0.01, key="future_b")
    
    if st.button("🔄 Calculate Impermanent Loss", type="primary"):
        il_percentage, pool_value_ratio = calculate_impermanent_loss_80_20(
            initial_price_a, initial_price_b, future_price_a, future_price_b
        )
        
        price_change_a = ((future_price_a / initial_price_a) - 1) * 100
        price_change_b = ((future_price_b / initial_price_b) - 1) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📉 Impermanent Loss</h3>
                <h2>{il_percentage:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Pool Value Ratio</h3>
                <h2>{pool_value_ratio:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Price Ratio Change</h3>
                <h2>{((future_price_a/future_price_b)/(initial_price_a/initial_price_b)-1)*100:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        if il_percentage < -1:
            st.markdown(f"""
            <div class="warning-card">
                <h4>⚠️ Impermanent Loss Warning</h4>
                <p>You would lose {abs(il_percentage):.2f}% compared to just holding the assets individually.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-card">
                <h4>⚠️ Impermanent Loss</h4>
                <p>You would lose {abs(il_percentage):.2f}% compared to just holding the assets individually.</p>
            </div>
            """, unsafe_allow_html=True)

    st.header("🪙 Initia (INIT) / USDC Pool Analysis")
    
    with st.spinner("🔄 Fetching current INIT price..."):
        current_init_price, price_change_24h, last_updated = get_initia_price()
    
    if current_init_price:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            change_color = "#44ff44" if price_change_24h >= 0 else "#ff4444"
            st.markdown(f"""
            <div class="price-card">
                <h3>💎 Current INIT Price</h3>
                <h2>${current_init_price:.4f}</h2>
                <p style="color: {change_color};">24h: {price_change_24h:+.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="price-card">
                <h3>💵 USDC Price</h3>
                <h2>$1.0000</h2>
                <p style="color: #888;">Stable</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            update_time = datetime.fromtimestamp(last_updated).strftime("%H:%M:%S")
            st.markdown(f"""
            <div class="price-card">
                <h3>🕒 Last Updated</h3>
                <h2>{update_time}</h2>
                <p>Real-time data</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.subheader("📈 Price Pump Scenarios")
        
        pump_scenarios = ["2x", "4x", "10x", "20x"]
        pump_multipliers = [2, 4, 10, 20]
        pump_il_values = []
        
        for multiplier in pump_multipliers:
            future_init_price = current_init_price * multiplier
            il, _ = calculate_impermanent_loss_80_20(current_init_price, 1.0, future_init_price, 1.0)
            pump_il_values.append(abs(il))
        
        st.subheader("💰 HODL vs LP Comparison (Increasing INIT value)")
        
        hodl_data = []
        for scenario, multiplier in zip(pump_scenarios, pump_multipliers):
            new_price = current_init_price * multiplier
            il_actual, _ = calculate_impermanent_loss_80_20(current_init_price, 1.0, new_price, 1.0)
            
            hodl_100_init = 1000 * multiplier
            
            hodl_80_20_init = 800 * multiplier
            hodl_80_20_usdc = 200
            hodl_80_20_total = hodl_80_20_init + hodl_80_20_usdc
            
            lp_value = hodl_80_20_total * (1 + il_actual/100)
            
            difference_100 = hodl_100_init - lp_value
            difference_80_20 = hodl_80_20_total - lp_value
            
            hodl_data.append([
                scenario,
                f"${new_price:.4f}",
                f"${hodl_100_init:.0f}",
                f"${hodl_80_20_total:.0f}",
                f"${lp_value:.0f}",
                f"{abs(il_actual):.2f}%",
                f"${difference_100:.0f}",
                f"${difference_80_20:.0f}"
            ])
        
        table_html = f"""<div style="margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; overflow: hidden; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);"><thead><tr style="background: rgba(0,0,0,0.4);"><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">Scenario</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">INIT Price</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">HODL 100% INIT</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">HODL 80/20</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">LP Value</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">IL %</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">LP vs 100% HODL</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">LP vs 80/20 HODL</th></tr></thead><tbody>"""
        
        for i, row in enumerate(hodl_data):
            bg_color = "rgba(255,255,255,0.15)" if i % 2 == 0 else "rgba(255,255,255,0.08)"
            table_html += f"""<tr style="background: {bg_color};"><td style="padding: 16px; text-align: center; color: white; font-size: 20px; font-weight: bold;">{row[0]}</td><td style="padding: 16px; text-align: center; color: white; font-size: 18px; font-weight: bold;">{row[1]}</td><td style="padding: 16px; text-align: center; color: #4ade80; font-size: 20px; font-weight: bold;">{row[2]}</td><td style="padding: 16px; text-align: center; color: #60a5fa; font-size: 20px; font-weight: bold;">{row[3]}</td><td style="padding: 16px; text-align: center; color: #fbbf24; font-size: 20px; font-weight: bold;">{row[4]}</td><td style="padding: 16px; text-align: center; color: #ffffff; font-size: 20px; font-weight: bold;">-{row[5]}</td><td style="padding: 16px; text-align: center; color: #ffffff; font-size: 20px; font-weight: bold;">-{row[6]}</td><td style="padding: 16px; text-align: center; color: #ffffff; font-size: 20px; font-weight: bold;">-{row[7]}</td></tr>"""
        
        table_html += """</tbody></table></div>"""
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        
        st.subheader("📉 Price Drop Scenarios (Decreasing INIT Value)")
        
        drop_scenarios = ["-50%", "-75%", "-90%"]
        drop_multipliers = [0.5, 0.25, 0.1]
        
        drop_data = []
        for scenario, multiplier in zip(drop_scenarios, drop_multipliers):
            new_price = current_init_price * multiplier
            il_actual, _ = calculate_impermanent_loss_80_20(current_init_price, 1.0, new_price, 1.0)
            
            hodl_100_init = 1000 * multiplier
            
            hodl_80_20_init = 800 * multiplier
            hodl_80_20_usdc = 200
            hodl_80_20_total = hodl_80_20_init + hodl_80_20_usdc
            
            lp_value = hodl_80_20_total * (1 + il_actual/100)
            
            difference_100 = lp_value - hodl_100_init
            difference_80_20 = lp_value - hodl_80_20_total
            
            drop_data.append([
                scenario,
                f"${new_price:.4f}",
                f"${hodl_100_init:.0f}",
                f"${hodl_80_20_total:.0f}",
                f"${lp_value:.0f}",
                f"{abs(il_actual):.2f}%",
                f"${difference_100:+.0f}",
                f"${difference_80_20:+.0f}"
            ])
        
        table_html_drop = f"""<div style="margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; overflow: hidden; box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);"><thead><tr style="background: rgba(0,0,0,0.4);"><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">Scenario</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">INIT Price</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">HODL 100% INIT</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">HODL 80/20</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">LP Value</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">IL %</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">LP vs 100% HODL</th><th style="padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.3);">LP vs 80/20 HODL</th></tr></thead><tbody>"""
        
        for i, row in enumerate(drop_data):
            bg_color = "rgba(255,255,255,0.15)" if i % 2 == 0 else "rgba(255,255,255,0.08)"
            table_html_drop += f"""<tr style="background: {bg_color};"><td style="padding: 16px; text-align: center; color: white; font-size: 20px; font-weight: bold;">{row[0]}</td><td style="padding: 16px; text-align: center; color: white; font-size: 18px; font-weight: bold;">{row[1]}</td><td style="padding: 16px; text-align: center; color: #ffcccc; font-size: 20px; font-weight: bold;">{row[2]}</td><td style="padding: 16px; text-align: center; color: #fbbf24; font-size: 20px; font-weight: bold;">{row[3]}</td><td style="padding: 16px; text-align: center; color: #60a5fa; font-size: 20px; font-weight: bold;">{row[4]}</td><td style="padding: 16px; text-align: center; color: #ffffff; font-size: 20px; font-weight: bold;">-{row[5]}</td><td style="padding: 16px; text-align: center; color: {'#4ade80' if '+' in row[6] else '#ffffff'}; font-size: 20px; font-weight: bold;">{row[6]}</td><td style="padding: 16px; text-align: center; color: {'#4ade80' if '+' in row[7] else '#ffffff'}; font-size: 20px; font-weight: bold;">{row[7]}</td></tr>"""
        
        table_html_drop += """</tbody></table></div>"""
        
        st.markdown(table_html_drop, unsafe_allow_html=True)
        
        
        st.subheader("📊 Complete Scenario Analysis")
        
        # Combine all scenarios for overview
        all_scenarios = pump_scenarios + drop_scenarios
        all_multipliers = pump_multipliers + drop_multipliers
        
        complete_data = []
        for scenario, multiplier in zip(all_scenarios, all_multipliers):
            new_price = current_init_price * multiplier
            il_actual, pool_value_ratio = calculate_impermanent_loss_80_20(current_init_price, 1.0, new_price, 1.0)

            initial_init_value = 800  # $800 in INIT
            initial_usdc_value = 200  # $200 in USDC
            

            hodl_init_value = initial_init_value * multiplier
            hodl_usdc_value = initial_usdc_value  # USDC stays at $200
            hodl_total = hodl_init_value + hodl_usdc_value
            
            lp_value = hodl_total * (1 + il_actual/100) 
            
            difference = hodl_total - lp_value
            
            complete_data.append({
                "Scenario": scenario,
                "INIT Price": f"${new_price:.4f}",
                "Price Change": f"{(multiplier-1)*100:+.1f}%",
                "Impermanent Loss": f"-{abs(il_actual):.2f}%",
                "HODL Value ($1000)": f"${hodl_total:.2f}",
                "LP Value ($1000)": f"${lp_value:.2f}",
                "Difference": f"${difference:+.2f}"
            })
        
        df_complete = pd.DataFrame(complete_data)
        st.dataframe(df_complete, use_container_width=True)
        
    else:
        st.error("❌ Unable to fetch current INIT price. Please check your internet connection.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #888;">
    <p>🔧 Built with Streamlit | 📊 Data from CoinGecko API</p>
</div>
""", unsafe_allow_html=True)
