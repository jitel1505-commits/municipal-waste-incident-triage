import streamlit as st
import pandas as pd
import datetime
import random

# ---------------------------------------------------------
# 1. Page Configuration & Custom CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Municipal Waste Incident Triage System",
    page_icon="🚛",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 16px; color: #4B5563; margin-bottom: 25px; }
    .card { background-color: #F3F4F6; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .ticket-box { background-color: #EFF6FF; border: 2px solid #3B82F6; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for tracking dispatch tickets
if 'tickets' not in st.session_state:
    st.session_state.tickets = []

# ---------------------------------------------------------
# 2. NLP Triage Engine (Keyword & Rule-Based Analytics)
# ---------------------------------------------------------
def analyze_waste_complaint(text):
    text_lower = text.lower()
    
    # Category Classification Keywords
    categories = {
        "Organic & Food Waste": ["organic", "food", "garbage", "smell", "rotten", "vegetables", "wet", "odor", "stink", "market"],
        "Recyclable & Dry Waste": ["plastic", "bottles", "paper", "cardboard", "boxes", "cans", "metal", "dry", "packaging"],
        "Construction & Bulky Debris": ["debris", "construction", "concrete", "bricks", "furniture", "wood", "tiles", "rubble"],
        "Hazardous & E-Waste": ["chemical", "battery", "e-waste", "batteries", "toxic", "medical", "wire", "oil", "hazardous", "glass", "sharp"]
    }
    
    # Emergency & High-Urgency Keywords
    high_urgency_words = ["overflowing", "blocking", "traffic", "fire", "leak", "severe", "drain", "school", "hospital", "toxic", "emergency", "immediate"]
    medium_urgency_words = ["full", "smell", "stink", "dumped", "heap", "days", "market", "large"]
    
    # Detect Waste Category
    detected_category = "General Municipal Waste"
    max_cat_score = 0
    for cat, keywords in categories.items():
        score = sum(1 for word in keywords if word in text_lower)
        if score > max_cat_score:
            max_cat_score = score
            detected_category = cat

    # Detect Urgency Tier
    high_score = sum(1 for word in high_urgency_words if word in text_lower)
    med_score = sum(1 for word in medium_urgency_words if word in text_lower)
    
    if high_score >= 1 or "block" in text_lower or "toxic" in text_lower:
        urgency = "Tier 3: Critical / Emergency"
        target_response = "< 4 Hours"
        department = "Emergency Rapid Dispatch Unit"
    elif med_score >= 1 or max_cat_score >= 2:
        urgency = "Tier 2: Moderate Priority"
        target_response = "12 - 24 Hours"
        department = "Regional Sanitation Fleet"
    else:
        urgency = "Tier 1: Low Priority"
        target_response = "24 - 48 Hours"
        department = "Scheduled Route Maintenance"
        
    return detected_category, urgency, target_response, department

# ---------------------------------------------------------
# 3. Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3209/3209995.png", width=80)
st.sidebar.title("Navigation Portal")
page = st.sidebar.radio("Go to:", ["Log Civic Incident", "Municipal Admin Dashboard", "About System"])

# ---------------------------------------------------------
# PAGE 1: LOG CIVIC INCIDENT
# ---------------------------------------------------------
if page == "Log Civic Incident":
    st.markdown("<div class='main-header'>🚨 Municipal Waste Incident Reporting</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Report urban waste issues using plain text. The AI system will categorize the waste and dispatch appropriate resources.</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Incident Details")
        location = st.text_input("Incident Location / Ward Number:", placeholder="e.g., Ward 12, Main Market Road, Sector 4")
        complaint_text = st.text_area("Describe the Waste Situation in Detail:", height=150, placeholder="e.g., Large heap of organic waste overflowing near the vegetable market. Foul smell spreading and blocking the walkway.")
        reporter_name = st.text_input("Reporter Name / ID (Optional):", placeholder="e.g., Resident / Sanitation Inspector 4")
        
        submit_btn = st.button("Submit Report for AI Triage", type="primary")

    with col2:
        st.subheader("Quick Test Samples")
        st.info("Click a sample to copy text for testing:")
        st.code("Large pile of plastic bottles and cardboard boxes dumped near Sector 5 park.", language="text")
        st.code("Broken batteries and chemical liquid leaking near hospital drain gate blocking road.", language="text")
        st.code("Overflowing food waste bin with severe odor near public school entrance.", language="text")

    # Processing Submission
    if submit_btn:
        if not complaint_text or not location:
            st.error("Please provide both location and a description of the waste incident.")
        else:
            category, urgency, response_time, department = analyze_waste_complaint(complaint_text)
            ticket_id = f"TKT-{random.randint(1000, 9999)}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save ticket
            new_ticket = {
                "Ticket ID": ticket_id,
                "Timestamp": timestamp,
                "Location": location,
                "Category": category,
                "Urgency Tier": urgency,
                "Target Response": response_time,
                "Assigned Department": department,
                "Description": complaint_text,
                "Status": "Dispatched"
            }
            st.session_state.tickets.append(new_ticket)
            
            st.success("Incident Logged & Dispatched Successfully!")
            
            # Display Triage Card
            st.markdown("<div class='ticket-box'>", unsafe_allow_html=True)
            st.markdown(f"### 📋 AI Automated Dispatch Ticket ({ticket_id})")
            st.write(f"**Logged At:** {timestamp}")
            st.write(f"**Location:** {location}")
            st.write(f"**Detected Category:** `{category}`")
            
            if "Critical" in urgency:
                st.error(f"**Urgency Level:** {urgency}")
            elif "Moderate" in urgency:
                st.warning(f"**Urgency Level:** {urgency}")
            else:
                st.info(f"**Urgency Level:** {urgency}")
                
            st.write(f"**Target SLA Response Time:** {response_time}")
            st.write(f"**Assigned Dispatch Team:** {department}")
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: MUNICIPAL ADMIN DASHBOARD
# ---------------------------------------------------------
elif page == "Municipal Admin Dashboard":
    st.markdown("<div class='main-header'>📊 Municipal Dispatch & Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Real-time tracking of active dispatch tickets, sector workload, and urgency tiering.</div>", unsafe_allow_html=True)
    
    if not st.session_state.tickets:
        st.info("No active incident tickets logged yet. Submit a report from the 'Log Civic Incident' page.")
    else:
        df = pd.DataFrame(st.session_state.tickets)
        
        # Top Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Tickets Logged", len(df))
        m2.metric("Critical Emergencies", len(df[df["Urgency Tier"].str.contains("Critical")]))
        m3.metric("Moderate Incidents", len(df[df["Urgency Tier"].str.contains("Moderate")]))
        m4.metric("Routine Cleans", len(df[df["Urgency Tier"].str.contains("Low")]))
        
        st.markdown("---")
        
        # Active Ticket Table
        st.subheader("Active Incident Dispatch Manifest")
        st.dataframe(df[["Ticket ID", "Timestamp", "Location", "Category", "Urgency Tier", "Assigned Department", "Target Response"]], use_container_width=True)
        
        # Visual Analytics
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Incidents by Waste Category")
            cat_counts = df["Category"].value_counts()
            st.bar_chart(cat_counts)
            
        with col_b:
            st.subheader("Urgency Level Distribution")
            urg_counts = df["Urgency Tier"].value_counts()
            st.line_chart(urg_counts)

# ---------------------------------------------------------
# PAGE 3: ABOUT SYSTEM
# ---------------------------------------------------------
elif page == "About System":
    st.markdown("<div class='main-header'>ℹ️ About AI Municipal Triage System</div>", unsafe_allow_html=True)
    st.write("""
    ### System Overview
    The **AI Municipal Waste Incident Triage & Response System** is designed for smart city municipal corporations. 
    It replaces manual inspection sheets with automated Natural Language Processing (NLP) text triage.
    
    ### Key Features:
    * **Instant Text Classification:** Categorizes unformatted citizen descriptions into Organic, Recyclable, Construction, or Hazardous waste.
    * **Urgency Stratification:** Flags critical street blockages and public health hazards for immediate <4 hour dispatch.
    * **Automated Dispatch Routing:** Directs reports directly to specialized crews (e.g., E-Waste unit vs. General Sanitation).
    """)
