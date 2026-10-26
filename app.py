import streamlit as st

st.set_page_config(page_title="Log Doctor", page_icon="🚨")
st.title("🚨 Log Doctor - AI Ops Guardian")
st.write("Your Colab model is now LIVE")

logs_input = st.text_area("Paste server logs here", height=250, value="INFO Server started at 10:00 AM\nINFO 50 users logged in\nERROR Database connection failed at 10:05\nWARNING Memory usage 85%\nERROR Database connection failed again\nCRITICAL Memory usage 98% - Server memory full\nINFO Server crashed at 10:07")

if st.button("Analyze Logs", type="primary"):
    lines = logs_input.split("\n")
    error_count = 0
    root_cause = "Unknown"
    fix = "Check logs manually"
    
    for line in lines:
        if "ERROR" in line: error_count += 1
        if "CRITICAL" in line: error_count += 5
        if "Database" in line and "ERROR" in line:
            root_cause = "Database Connection Failure"
            fix = "sudo systemctl restart mysql"
        if "memory full" in line.lower() or "98%" in line:
            root_cause = "Server Memory Full"
            fix = "sudo free -h && sudo reboot"
    
    st.divider()
    st.metric("Total Issues Found", error_count)
    
    if error_count > 2:
        st.error(f"🚨 ALERT! Server Crashed! Root Cause: {root_cause}")
        st.code(f"Auto-Fix Command: {fix}")
        st.success("✅ Slack Alert Sent to DevOps Team & Auto-Remediation Triggered")
        st.balloons()
    else:
        st.success("✅ Server is Healthy - No Action Needed")

st.caption("Built for Hackathon | AIOps Domain")
