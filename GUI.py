import streamlit as st
import requests
from PIL import Image

# Configure page
st.set_page_config(
    page_title="Tech Tailored PC Recommender",
    page_icon="./LOGO.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)






#-----------------------------code for displaying the Page--------------------------------------------------------

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: black;    
    .stSelectbox, .stRadio, .stSlider {
        margin-bottom: 1rem;
    }
    .recommendation-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #423d3b;
        margin-bottom: 1rem;
    }
    .total-price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #90EE90;
    }
    .component-price {
        color: #90EE90;
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
            

    
    
   
    }
    
    </style>
""", unsafe_allow_html=True)

# Header with logo and title
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("<h1 style='font-size: 3rem; text-align: center;'>Tech Tailored PC Recommender</h1>", unsafe_allow_html=True)
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
            amd_values = ["Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"]
            
            amd_labels = [
             "Ryzen 3",
             "Ryzen 5",
             "Ryzen 7",
             "Ryzen 9"
                         ]
            st.markdown("""
            **AMD Series Guide:**
            - **Ryzen 3**: Budget (General use, light gaming)
            - **Ryzen 5**: Mainstream (Gaming, productivity)
            - **Ryzen 7**: Performance (Content creation, gaming)
            - **Ryzen 9**: Enthusiast (Workstations, high-end gaming)
                        
            """)
        elif preferred_cpu == "Intel":

            intel_values= ["i3", "i5", "i7","i9"]

            intel_labels=["Intel i3", "Intel i5", "Intel i7", "Intel i9"]

            st.markdown("""
            **Intel Series Guide:**
            - **i3**: Budget (General use, office work)
            - **i5**: Mainstream (Gaming, multitasking)
            - **i7**: Performance (Content creation, gaming)
            - **i9**: Enthusiast (Workstations, high-end gaming)
                        
            """)

        # Display series selection as multiple choice based on preferred CPU
        if preferred_cpu == "AMD":
            selected_amd = st.selectbox(
             "**:pushpin: Select AMD Series**",
             options=amd_values,
             format_func=lambda x: amd_labels[amd_values.index(x)],
             help="Choose the AMD series you are interested in."
             )
        elif preferred_cpu == "Intel":
            intel_series = st.selectbox(
                "**📌 Select Intel Series**",
             options = intel_values,
             format_func = lambda x: intel_labels[intel_values.index(x)],
             help="Choose the Intel series you are interested in."
            )

    with col2:
        case_values= [ "Mini Tower", "Mid Tower" , "Full Tower"]
        case_labels=[
                "Mini Tower (Compact, limited expansion)",
                "Mid Tower (Balanced size and expandability)",
                "Full Tower (Maximum expansion, better cooling)",
            ]
        case_size = st.selectbox(
            
           
            "**📏 Case Size Preference**",
             options = case_values,
             format_func = lambda x: case_labels[case_values.index(x)],
             index=0,
              help="Larger cases offer better cooling and expansion"           
        )
        
        
        cooling_values=[ "Air", "Liquid"]
        cooling_labels= [
           
                "Air Cooling (Quiet, reliable)",
                "Liquid Cooling (Better performance, aesthetic)"        
            ]
        cooling = st.selectbox(
            "**🧊 Cooling Solution**",
             options = cooling_values,
             format_func = lambda x: cooling_labels[cooling_values.index(x)],
             index=0,
            
            
        )
        storage_values=[256,512,1024,2048,4096,8192]
        storage_labels=[
            "256 GB (₱1,200 est.)",
            "512 GB (₱1,800 est.)",
            "1 TB (₱2,800 est.)",
            "2 TB (₱4,500 est.)",
            "4 TB(₱8,000 est.)",
            "8 TB (₱15,000 est.)"
]
        storage = st.selectbox(
            "**💾 Storage Configuration**",
            options = storage_values,
             format_func = lambda x: storage_labels[storage_values.index(x)],
             index=0,

        
        )
        ram_values=["8 GB","16 GB","32 GB", "64 GB", "128 GB"]
        ram_labels=[
            "8 GB (₱3,840 est.)",
            "16 GB (₱7,250 est.)",
            "32 GB (₱11,160 est.)",
            "64 GB (₱19,200 est.)",
            "128 GB (₱33,480 est.)"
]
        ram_pref = st.selectbox(
                "💿 Memory Capacity",
                options = ram_values,
                format_func = lambda x: ram_labels[ram_values.index(x)],              
                index=0
            )

    

    if st.button("**🎯 Get My PC Recommendation**", use_container_width=True):
            if not preferred_cpu:
             st.warning("please pick CPU")
             
            user_input = {               
                "cpu_model": selected_amd if preferred_cpu == "AMD" else intel_series,
                "case_size": case_size,
                "cooling": cooling,
                "pref_storage_size": storage,
                "pref_memory_size": ram_pref,
                "pref_storage_type": "SSD",                   
                "pref_memory_type": "DDR5"          
            }

             #needs changing sql 
    # cpu_model: str 
    # #needs changing sql
    # case_size: str
    # #needs changing sql
    # cooling: str 
    # #frontend changing
    # pref_memory_size: str
    # pref_storage_size: int
    # pref_memory_type: str
    # pref_storage_type: str
#-----------------------------code for displaying thec Main Page <End>--------------------------------------------------------

#------------------------------code for displaying the recommended Build------------------------------------------
            with st.spinner("Finding the perfect components for your build..."):
                
                
                try:
                    res = requests.post("http://localhost:8001/get_user_build", json = user_input)

                    if res.status_code == 200:
                        data = res.json()
                        if "build" in data:
                            
                            build = data["build"]                           
                            total_price = build.get("recommended_total_cost", 0)
                            cpu_name = build.get("recommended_cpu_name")
                            

                            st.success("### 🎉 Here's your personalized PC build!")

                            col1, col2 = st.columns(2)

                            with col1:
                                
                                 st.markdown("#### Core Components")
                                 st.markdown(f"""    
                                    <div class="recommendation-card">
                                        <p><strong>💻 CPU:</strong> {build.get("recommended_cpu_name")} <span class="component-price">₱ {build.get("recommended_cpu_price")}</span></p>
                                        <p><strong>🎮 GPU:</strong> {build.get("recommended_gpu_name")} <span class="component-price">₱ {build.get("recommended_gpu_price")}</span></p>
                                        <p><strong>🧠 RAM:</strong> {build.get("recommended_memory_name")} <span class="component-price">₱ {build.get("recommended_memory_price")}</span></p>
                                        <p><strong>💾 Storage:</strong> {build.get("recommended_storage_name")} <span class="component-price">₱ {build.get("recommended_storage_price")}</span></p>
                                    </div>
                                """, unsafe_allow_html=True)

                            with col2:                                
                                st.markdown("#### Supporting Components")
                                st.markdown(f"""
                                    <div class="recommendation-card">
                                        <p><strong>🧩 Motherboard:</strong> {build.get('recommended_mobo_name')} <span class="component-price">₱ {build.get('recommended_mobo_price')}</span></p>
                                        <p><strong>🔌 PSU:</strong> {build.get('recommended_psu_name')} <span class="component-price">₱ {build.get('recommended_mobo_price')}</span></p>
                                        <p><strong>🏢 Case:</strong> {build.get('recommended_case_name')} <span class="component-price">₱ {build.get('recommended_mobo_price')}</span></p>
                                        <p><strong>🧊 Cooling:</strong> {build.get('recommended_cooling_name')} <span class="component-price">₱ {build.get('recommended_mobo_price')}</span></p>
                                    </div>
                                """, unsafe_allow_html=True)

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

#------------------------------code for displaying the recommended Build------------------------------------------

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
