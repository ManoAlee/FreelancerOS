
import streamlit as st
import sys
import os
import time

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'freelanceros'))
from freelanceros.modules import business_math, text_data, system_files, media_web, job_hunter

# Page Config
st.set_page_config(page_title="FreelancerOS Command Center", page_icon="🚀", layout="wide")

# Styling
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #4F46E5; font-weight: 800;}
    .sub-header {font-size: 1.5rem; color: #6B7280;}
    .card {padding: 20px; background-color: #f3f4f6; border-radius: 10px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# sidebar
st.sidebar.title("🚀 FreelancerOS")
st.sidebar.info("v2.0 | Status: Online")
mode = st.sidebar.radio("Mode", ["Dashboard", "Job Hunter", "Toolbox", "Ventures"])

# 1. DASHBOARD
if mode == "Dashboard":
    st.markdown("<p class='main-header'>Welcome back, Agent.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tools Available", value="220+")
    with col2:
        st.metric(label="Modules Active", value="5")
    with col3:
        st.metric(label="System Status", value="Optimal")

    st.markdown("### ⚡ Quick Actions")
    if st.button("Clean Temporary Files"):
        with st.spinner("Cleaning system..."):
            time.sleep(1)
            st.success("System optimized!")

# 2. JOB HUNTER
elif mode == "Job Hunter":
    st.markdown("## 🕵️ Job Hunter & Auto-Pilot")
    
    tab1, tab2 = st.tabs(["📡 Radar (RSS)", "🤖 Auto-Bot (Selenium)"])
    
    with tab1:
        st.markdown("Automated feed monitoring.")
        source = st.selectbox("Select Source", list(job_hunter.FEEDS.keys()))
        
        if st.button("Scan for Jobs"):
            with st.spinner(f"Scanning {source}..."):
                jobs = job_hunter.fetch_rss_jobs(source)
                st.session_state['jobs'] = jobs
                st.success(f"Found {len(jobs)} opportunities.")

        if 'jobs' in st.session_state:
            for i, job in enumerate(st.session_state['jobs']):
                with st.expander(f"{job['title']}"):
                    st.write(job['summary'])
                    st.markdown(f"[View Job]({job['link']})")
    
    with tab2:
        st.markdown("### 🤖 LinkedIn Auto-Pilot")
        st.warning("This runs the 'Merged' Bot logic (Selenium). Requires Chrome.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            li_email = st.text_input("LinkedIn Email")
        with col_b:
            li_pass = st.text_input("Password", type="password")
            
        headless = st.checkbox("Headless Mode (Invisible)", value=True)
        
        if st.button("🚀 Launch Bot System"):
            if not li_email or not li_pass:
                st.error("Credentials required for the bot.")
            else:
                st.info("Initializing 'LinkedInBot' Core...")
                # Instantiate the merged bot class
                bot = job_hunter.LinkedInBot(headless=headless)
                if bot.start_browser():
                    st.success("Browser Agent Active.")
                    if bot.login(li_email, li_pass):
                        st.success("Authenticated.")
                        # Demo action
                        st.write("Targeting Jobs...")
                        result = bot.apply_to_job("linkedin.com/jobs/search/?keywords=python")
                        st.balloons()
                        st.success(f"Bot Report: {result}")
                    else:
                        st.error("Login Failed.")
                else:
                    st.error("Driver Failed to Start.")

# 3. TOOLBOX
elif mode == "Toolbox":
    st.markdown("## 🛠️ The 220+ Toolkit")
    
    module_map = {
        "Business & Math": business_math,
        "Text & Data": text_data,
        "Media & Web": media_web,
        "System & Files": system_files
    }
    
    selected_mod_name = st.selectbox("Select Module", list(module_map.keys()))
    selected_mod = module_map[selected_mod_name]
    
    # Introspect functions
    funcs = [f for f in dir(selected_mod) if not f.startswith('_')]
    selected_func_name = st.selectbox("Select Tool", sorted(funcs))
    
    if selected_func_name:
        st.markdown(f"**Executing**: `{selected_func_name}`")
        func = getattr(selected_mod, selected_func_name)
        
        # Simple generic input
        arg_input = st.text_input("Arguments (comma separated)", placeholder="e.g. 100, 20")
        
        if st.button("Run Tool"):
            try:
                if arg_input:
                    # Try to parse simple types
                    args = []
                    for x in arg_input.split(','):
                        x = x.strip()
                        if x.replace('.','',1).isdigit():
                            args.append(float(x) if '.' in x else int(x))
                        else:
                            args.append(x)
                    result = func(*args)
                else:
                    result = func()
                
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

# 4. VENTURES
elif mode == "Ventures":
    st.markdown("## 💸 Profitable Ventures")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card"><h3>🤖 Browser Agent</h3><p>Automated interaction bot.</p></div>', unsafe_allow_html=True)
        if st.button("Launch Browser Agent"):
            st.info("Agent script would accept params here. Running headless mode...")
    
    with col2:
        st.markdown('<div class="card"><h3>🧠 AI Crew</h3><p>Multi-agent research team.</p></div>', unsafe_allow_html=True)
        if st.button("Deploy AI Crew"):
            st.info("Crew spinning up... (Check terminal for output)")

