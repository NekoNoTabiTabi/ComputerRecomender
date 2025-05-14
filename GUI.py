import streamlit as st
import requests
from PIL import Image

# Configure page
st.set_page_config(
    page_title="PC Build Recommender",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_core_components(build):
   st.markdown("#### Core Components")
   st.markdown(f"""
                                    <div class="recommendation-card">
                                        <p><strong>💻 CPU:</strong> {build.get('cpu', 'N/A')} <span class="component-price">₱{component_prices.get('cpu', 0):,.2f}</span></p>
                                        <p><strong>🎮 GPU:</strong> {build.get('gpu', 'N/A')} <span class="component-price">₱{component_prices.get('gpu', 0):,.2f}</span></p>
                                        <p><strong>🧠 RAM:</strong> {build.get('ram', 'N/A')} <span class="component-price">₱{component_prices.get('ram', 0):,.2f}</span></p>
                                        <p><strong>💾 Storage:</strong> {build.get('storage', 'N/A')} <span class="component-price">₱{component_prices.get('storage', 0):,.2f}</span></p>
                                    </div>
                                """, unsafe_allow_html=True)

def display_supporting_components(build):
  st.markdown("#### Supporting Components")
  st.markdown(f"""
                                    <div class="recommendation-card">
                                        <p><strong>🧩 Motherboard:</strong> {build.get('motherboard', 'N/A')} <span class="component-price">₱{component_prices.get('motherboard', 0):,.2f}</span></p>
                                        <p><strong>🔌 PSU:</strong> {build.get('psu', 'N/A')} <span class="component-price">₱{component_prices.get('psu', 0):,.2f}</span></p>
                                        <p><strong>🏢 Case:</strong> {build.get('case', 'N/A')} <span class="component-price">₱{component_prices.get('case', 0):,.2f}</span></p>
                                        <p><strong>🧊 Cooling:</strong> {build.get('cooling', 'N/A')} <span class="component-price">₱{component_prices.get('cooling', 0):,.2f}</span></p>
                                    </div>
                                """, unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stSelectbox, .stRadio, .stSlider {
        margin-bottom: 1rem;
    }
    .recommendation-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .total-price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e86de;
    }
    .component-price {
        color: #576574;
        font-size: 0.9rem;
    }
    .stButton>button {
        background-color: #2e86de;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1e6fd9;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo and title
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("<h1 style='font-size: 3rem; text-align: center;'>Tech Tailored PC Builder</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Build your perfect PC with personalized recommendations</p>", unsafe_allow_html=True)

# Main content in tabs
tab1, tab2 = st.tabs(["🏗️ Build Recommender", "ℹ️ About"])

with tab1:
    st.subheader("Tell us about your needs")

    col1, col2 = st.columns(2)

    with col1:
        preferred_cpu = st.radio(
            "**🔧 Preferred CPU Brand**",
            ["Intel", "AMD",],
            index=None,
            help="Choose between Intel or AMD processors"
        )

        # Display guide based on CPU brand preference
        if preferred_cpu == "AMD":
            st.markdown("""
            **AMD Series Guide:**
            - **Ryzen 3**: Budget (General use, light gaming)
            - **Ryzen 5**: Mainstream (Gaming, productivity)
            - **Ryzen 7**: Performance (Content creation, gaming)
            - **Ryzen 9**: Enthusiast (Workstations, high-end gaming)
            """)
        elif preferred_cpu == "Intel":
            st.markdown("""
            **Intel Series Guide:**
            - **i3**: Budget (General use, office work)
            - **i5**: Mainstream (Gaming, multitasking)
            - **i7**: Performance (Content creation, gaming)
            - **i9**: Enthusiast (Workstations, high-end gaming)
            """)

        # Display series selection as multiple choice based on preferred CPU
        if preferred_cpu == "AMD":
            amd_series = st.radio(
                "**📌 Select AMD Series**",
                ["Ryzen 3 (₱15,000 - ₱25,000)", "Ryzen 5 (₱25,000 - ₱45,000)", "Ryzen 7 (₱45,000 - ₱75,000)", "Ryzen 9 (₱75,000 and above)"],
                help="Choose the AMD series you are interested in."
            )
        elif preferred_cpu == "Intel":
            intel_series = st.radio(
                "**📌 Select Intel Series**",
                ["Intel i3  (₱15,000 - ₱25,000)", "Intel i5 (₱25,000 - ₱45,000)", "Intel i7 (₱45,000 - ₱75,000)", "Intel i9 (₱75,000 and above)"],
                help="Choose the Intel series you are interested in."
            )

    with col2:
        form_factor = st.radio(
            "**📏 Case Size Preference**",
            [
                "Select size",
                "Mini Tower (Compact, limited expansion)",
                "Mid Tower (Balanced size and expandability)",
                "Full Tower (Maximum expansion, better cooling)",
                "No Preference"
            ],
            index=0,
            help="Larger cases offer better cooling and expansion"
        )

        cooling = st.radio(
            "**🧊 Cooling Solution**",
            [
                "Stock Cooler (Included with CPU)",
                "Air Cooling (Quiet, reliable)",
                "Liquid Cooling (Better performance, aesthetic)",
                "No Preference"
            ],
            index=None,
            horizontal=True
        )

        storage = st.radio(
            "**💾 Storage Configuration**",
            [
                "Select storage",
                "256GB SSD (Basic use)",
                "512GB SSD (Moderate use)",
                "1TB SSD (Gaming, general use)",
                "2TB SSD (Content creators)",
            ],
            index=0
        )


    with st.expander("**⚙️ Advanced Preferences**"):
        adv_col1, adv_col2 = st.columns(2)

        with adv_col1:
            ram_pref = st.selectbox(
                "Memory Capacity",
                ["8GB", "16GB", "32GB", "64GB+", "No Preference"],
                index=4
            )

            gpu_pref = st.radio(
                "GPU Brand Preference",
                ["NVIDIA", "AMD", "No Preference"],
                index=2
            )

            psu_pref = st.selectbox(
                "Power Supply Certification",
                ["80+ Bronze", "80+ Gold", "80+ Platinum", "No Preference"],
                index=3
            )

    if st.button("**🎯 Get My PC Recommendation**", use_container_width=True):
        if not preferred_cpu or (preferred_cpu == "AMD" and not amd_series) or (preferred_cpu == "Intel" and not intel_series) or form_factor == "Select size" or storage == "Select storage":
            st.warning("Please fill in all required fields before submitting.")
        else:
            user_input = {
                "preferred_cpu": preferred_cpu,
                "series": amd_series if preferred_cpu == "AMD" else intel_series,
                "form_factor": form_factor,
                "cooling": cooling,
                "storage": storage,
                "ram_pref": ram_pref,
                "gpu_pref": gpu_pref,
                "psu_pref": psu_pref
            }

            with st.spinner("Finding the perfect components for your build..."):
                try:
                    res = requests.post("http://localhost:8000/recommend", json = user_input)

                    if res.status_code == 200:
                        data = res.json()

                        if "recommended_build" in data:
                            build = data["recommended_build"]
                            component_prices = data.get("component_prices", {})
                            total_price = data.get("total_price", 0)

                            st.success("### 🎉 Here's your personalized PC build!")

                            col1, col2 = st.columns(2)

                            with col1:
                                
                                display_core_components(build)

                            with col2:                                
                                display_supporting_components(build)

                            st.markdown(f"""
                                <div style="margin-top: 2rem;">
                                    <p class="total-price">Total Estimated Price: ₱{total_price:,.2f}</p>
                                    <p>{data.get("note", "")}</p>
                                </div>
                            """, unsafe_allow_html=True)

                            st.markdown("---")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.button("💾 Save This Build", help="Save this configuration to your account")
                            with col2:
                                st.button("🛒 View Online Retailers", help="Find where to buy these components")
                            with col3:
                                st.button("🔄 Generate Alternative", help="Get a different build with similar specs")
                        else:
                            st.warning(data.get("message", "No recommendation available for your criteria."))
                    else:
                        st.error(f"Failed to get recommendation. Status code: {res.status_code} ")
                except Exception as e:
                    st.error(f"Error connecting to the recommendation service: {str(e)}")

with tab2:
    st.markdown("""
        ## About Tech Tailored PC Builder

        This tool helps you build the perfect PC based on your specific needs, preferences, and budget. 
        Our recommendation system analyzes thousands of component combinations to find the best match for you.

        ### How It Works
        1. **Tell us your needs** - Select your preferred components and usage scenario
        2. **Get recommendations** - Our system suggests optimal builds
        3. **Refine your build** - Adjust components as needed

        ### Features
        - Personalized component recommendations
        - Budget-aware suggestions
        - Compatibility checking
        - Performance estimates

        ### Data Sources
        - Latest component pricing and availability
        - Technical specifications from manufacturers
        - Real-world performance benchmarks

    """)

    st.markdown("### Example Builds")
    example_col1, example_col2, example_col3 = st.columns(3)

    with example_col1:
        with st.expander("💰 Budget Build (~₱30,000)"):
            st.markdown("""
                - AMD Ryzen 5 5600G
                - 16GB DDR4 RAM
                - 512GB NVMe SSD
                - Integrated Graphics
                - 550W PSU
                - Basic Case
            """)

    with example_col2:
        with st.expander("🎮 Gaming PC (~₱60,000)"):
            st.markdown("""
                - Intel Core i5-13600KF
                - NVIDIA RTX 4060 Ti
                - 32GB DDR5 RAM
                - 1TB NVMe SSD
                - 650W Gold PSU
                - Mid Tower Case
            """)

    with example_col3:
        with st.expander("💻 Workstation (~₱120,000)"):
            st.markdown("""
                - AMD Ryzen 9 7950X
                - NVIDIA RTX 4080
                - 64GB DDR5 RAM
                - 2TB NVMe SSD + 4TB HDD
                - 850W Platinum PSU
                - Full Tower Case
            """)
