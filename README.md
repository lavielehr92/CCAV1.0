# 📊 CCA Growth Opportunity Dashboard# Philadelphia Educational Desert Explorer

## CCA Expansion Analysis Dashboard

**A data-driven platform to identify high-potential neighborhoods for Cornerstone Christian Academy enrollment growth.**

A comprehensive Streamlit dashboard for analyzing educational opportunities and identifying expansion opportunities for Cornerstone Christian Academy (CCA) in Philadelphia.

---

## 📊 Dashboard Features

## 🎯 **Purpose**

### Core Functionality

This interactive dashboard helps CCA's leadership team:- **Educational Desert Index (EDI)**: Sophisticated algorithm combining multiple access metrics

- **Identify high-potential family neighborhoods** based on economic capacity and mission alignment- **Marketing Priority Analysis**: Data-driven targeting for families earning up to $350K

- **Discover educational access gaps** where Christian education options are limited- **Interactive Maps**: Plotly-powered visualizations with demographic overlays

- **Prioritize marketing and outreach efforts** using evidence-based geographic targeting- **Proximity Analysis**: Distance-based scoring from existing CCA campuses

- **Visualize demographic patterns** across Philadelphia block groups- **Real-time Filtering**: Dynamic ZIP code analysis based on multiple criteria

- **Export actionable data** for CRM integration and campaign planning

### Key Visualizations

---- ZIP code-level demographic mapping

- School location overlays (public, private, charter)

## 🚀 **Quick Start**- Current student distribution

- Marketing intelligence summary metrics

### **Access the Dashboard**

🔗 **Live Dashboard:** [https://ccav10.streamlit.app](https://ccav10.streamlit.app) *(Streamlit Cloud)*## 🚀 Quick Start



### **Basic Workflow**### Prerequisites

1. **Set Geographic Scope:** Use sidebar to define radius from CCA campuses (default 15km)```bash

2. **Apply Filters:** Narrow by income, HPFI thresholds, or demographic criteriapip install streamlit pandas plotly scikit-learn numpy requests

3. **Choose Visualization:** Select HPFI (economic potential), EDI (access gaps), or Overlay mode```

4. **Explore Top 10 Tables:** Review Premium Growth, Golden Zones, and High HPFI areas

5. **Export Data:** Download filtered results as CSV for deeper analysis### Running the Dashboard

```bash

---streamlit run app_fixed.py

```

## 📈 **Key Metrics Explained**

The dashboard will open at `http://localhost:8501`

### **HPFI - High-Potential Family Index** (0.00 - 1.00)

*Identifies areas with strongest tuition-paying capacity and mission alignment*## 📁 Project Structure



**Formula Components:**```

| Component | Weight | Data Source | What It Measures |MBA8583/

|-----------|--------|-------------|------------------|├── app_fixed.py                    # Main dashboard application

| **Income** | 45% | ACS 2023 median household income | Primary tuition-paying capacity |├── educational_desert_index.py     # EDI calculation algorithms

| **Economic Stability** | 18% | ACS 2023 poverty rate (inverse) | Financial reliability & stability |├── demographics.csv                # ZIP code demographic data (Census-sourced)

| **Campus Proximity** | 13% | Distance to West Oak Lane/Hunting Park | Commute feasibility (exponential decay) |├── schools.csv                     # School location and type data

| **Mission Alignment** | 12% | Christian % (OpenStreetMap church density) | Faith community strength |├── current_students.csv            # Current CCA student addresses

| **K-12 Market Size** | 9% | ACS 2023 modeled enrollment | Addressable student population |├── requirements.txt                # Python dependencies

| **Low Competition** | 3% | Inverse EDI | Areas with unmet need |└── README.md                      # This file

```

**Interpretation:**

- **0.75 - 1.00:** Premium growth opportunities (highest priority)## 📈 Data Sources

- **0.50 - 0.74:** Emerging opportunities (moderate potential)

- **0.00 - 0.49:** Lower priority (limited capacity or far from campuses)### Demographics Data (`demographics.csv`)

- **Source**: U.S. Census Bureau ACS 5-Year 2022 data

---- **Coverage**: 57 Philadelphia ZIP codes

- **Key Fields**:

### **EDI - Educational Desert Index** (0 - 100)  - `k12_pop`: K-12 student population (Census API verified)

*Identifies areas where families have limited access to Christian education options*  - `income`: Median household income

  - `poverty_rate`: Percentage below poverty line

**Methodology:** Two-Step Floating Catchment Area (2SFCA) Analysis  - `%Christian`: Estimated Christian population percentage

- **Research-validated** spatial accessibility model used in healthcare/education planning  - `%first_gen`: First-generation college students percentage

- **Gravity decay function:** Schools 1km away count far more than schools 10km away (exponential decay, 5km half-life)  - `lat/lon`: Geographic coordinates

- **Crowding adjustment:** Accounts for student-to-seat ratios at nearby schools

- **Catchment radius:** 15km maximum travel distance### Schools Data (`schools.csv`)

- School locations with coordinates

**Formula Components:**- Type classification (public, private, charter)

| Component | Weight | What It Measures |- Tuition and rating information

|-----------|--------|------------------|- Capacity estimates

| **Accessibility** | 40% | 2SFCA score (supply/demand ratio within travel zones) |

| **Seat Coverage** | 30% | Students per seat in nearby schools |### Current Students (`current_students.csv`)

| **Socioeconomic Need** | 20% | Poverty rate (higher poverty = higher EDI) |- Current CCA student home addresses

| **Infrastructure** | 10% | Estimated broadband access (poverty proxy) |- Geocoded for proximity analysis



**Interpretation:**## 🎯 Educational Desert Index (EDI)

- **70 - 100:** True educational deserts (far from schools, overcrowded, high poverty)

- **40 - 69:** Moderate access challenges (some gaps in options or capacity)The EDI combines multiple accessibility metrics:

- **0 - 39:** Well-served areas (good school access, sufficient seats)

1. **Two-Step Floating Catchment Analysis (2SFCA)**: Supply/demand ratio

**Default Calculation:** Uses CCA campuses + public schools only  2. **Gravity-Based Access**: Distance-decay accessibility modeling

**Optional Toggle:** Include charter/private schools in supply calculation (sidebar option)3. **Nearest School Distance**: Geographic isolation metric

4. **Neighborhood Need**: Poverty rate and education gaps

---

**Formula**: Weighted combination scaled 0-100 (higher = more underserved)

### **Marketing Zones** (Segmentation Framework)

*Custom scoring system (0-10 points) combining multiple factors*## 🎨 Dashboard Controls



**Scoring Breakdown:**### Sidebar Filters

- **Distance from CCA Campuses:**- **Proximity Targeting**: Distance filter from CCA campuses (1-35km)

  - ≤2km: +4 points | 2-5km: +3 points | 5-10km: +2 points | 10-20km: +1 point- **Map Overlays**: Current students toggle

- **Income Tier:**- **Educational Access**: EDI range slider (4.23-75.05)

  - $100K-$350K: +3 points | $75K-$100K: +2 points | $50K-$75K: +1 point- **Household Income**: Income range targeting ($35K-$350K)

- **Christian % (Mission Alignment):**- **School Types**: Filter visible school types

  - ≥43% (high church density): +2 points | 37-43% (moderate): +1 point- **Target Criteria**: First-gen and Christian population filters

- **K-12 Population:**

  - ≥200 students: +1 point### Marketing Priority Algorithm

Scores ZIP codes based on:

**Zone Classifications:**- Distance to CCA campuses (highest weight)

1. **Premium Growth Targets (8-10 points):** High income + close proximity + strong faith community- Household income brackets

2. **Golden Zones (High HPFI + Low EDI):** Affluent areas with existing school access- First-generation college percentage

3. **Emerging Opportunities (6-7 points):** Moderate potential, requires nurturing- Christian population estimates

4. **Foundation Building (0-5 points):** Long-term relationship development areas- Educational desert severity (EDI scores)



---## 🔧 Technical Implementation



## 📊 **Data Sources & Accuracy**### Key Libraries

- **Streamlit**: Web application framework

### **Demographics & Enrollment (ACS 2023)**- **Plotly**: Interactive mapping and visualization

| Data Type | Source | Granularity | Methodology |- **Pandas**: Data manipulation and analysis

|-----------|--------|-------------|-------------|- **Scikit-learn**: Machine learning preprocessing

| **Median Household Income** | ACS 2023 5-year estimates (B19013) | Block group | Direct survey data |- **NumPy**: Numerical computations

| **Poverty Rate** | ACS 2023 5-year estimates (S1701) | Block group | % of families below poverty line |

| **Total Population** | ACS 2023 5-year estimates (B01001) | Block group | Population by age/sex |### Performance Considerations

| **K-12 Enrollment** | ACS 2023 5-year estimates (B01001 + S1401) | **Modeled** | Tract rate × block group age 5-17 population |- Efficient haversine distance calculations

| **Race/Ethnicity** | ACS 2023 5-year estimates (B02001) | Block group | % Black, % White, % Other |- Optimized data filtering and merging

- Responsive map rendering with appropriate zoom levels

**K-12 Modeling Approach:**

1. **Block group ages 5-17:** Sum of ACS B01001 fields 004E-006E (male) + 028E-030E (female)## 📊 Marketing Intelligence Metrics

2. **Tract enrollment rate:** ACS S1401 (kindergarten + grades 1-8 + grades 9-12) / tract population

3. **Downscaling:** Block group K-12 estimate = (tract rate) × (block group age 5-17 pop)The dashboard provides actionable metrics:

4. **Quality flag:** All estimates marked as "modeled"; missing data areas imputed with 0- **Ultra High Priority**: Areas with marketing scores ≥8

- **Tier 1 Priority**: Areas with scores ≥6

**Total K-12 Students Modeled:** ~165,934 across 1,338 Philadelphia block groups- **Tier 2 Targets**: Areas with scores ≥4

- **Premium First-Gen**: High-income + high first-generation families

---

## 🎯 Use Cases

### **Christian % (Mission Alignment)**

| Data Type | Source | Granularity | Methodology |1. **Expansion Planning**: Identify underserved areas for new campuses

|-----------|--------|-------------|-------------|2. **Marketing Strategy**: Target high-potential ZIP codes for enrollment

| **County Baseline** | ARDA U.S. Religion Census 2020 | County | Christian adherents / total population |3. **Resource Allocation**: Understand current student distribution

| **Block-Level Variation** | OpenStreetMap (Overpass API) | Block group | Church density modulation |4. **Competitive Analysis**: Visualize school density and gaps

5. **Demographic Research**: Explore Philadelphia education landscape

**Philadelphia County Baseline:** 36.3% Christian (ARDA 2020 adherents data)

## 🛠 Customization

**Church Density Methodology:**

1. **Data Source:** OpenStreetMap places of worship tagged `amenity=place_of_worship` + `religion=christian`### Adding New Data Sources

2. **Churches Found:** 1,420 Christian churches across Philadelphia County1. Update CSV files with new data

3. **Assignment:** Count churches within 1km of each block group centroid2. Modify column mappings in `app_fixed.py`

4. **Density Calculation:** Churches per 1,000 residents3. Adjust EDI weights in `educational_desert_index.py`

5. **Modulation Formula:**

   ```### Extending Analysis

   density_ratio = (block_churches_per_1k) / (county_avg_churches_per_1k)- Add new demographic variables

   multiplier = 1.0 + 0.4 × log(density_ratio)- Implement additional scoring algorithms

   estimated_christian_pct = 36.3% × multiplier- Create custom visualizations

   smoothed_pct = 0.6 × estimated_pct + 0.4 × 36.3%  // Spatial smoothing- Export analysis results

   ```

6. **Range:** 36.3% (low church density) to 47.5% (high church density)## 📝 Notes for Collaborators



**Distribution:**### Data Quality

- **232 blocks (17%):** ≥43% Christian (top quartile, strong faith communities)- K-12 population data sourced from official Census API

- **778 blocks (58%):** 37-43% Christian (moderate faith presence)- Geographic coordinates verified for accuracy

- **328 blocks (25%):** <37% Christian (secular/diverse neighborhoods)- Income data represents median household estimates



**Denominations in Data:** Baptist (266), Catholic/Roman Catholic (91), Presbyterian (47), Methodist (35), Pentecostal (33), Episcopal (33), Lutheran (30), and others.### Known Limitations

- Some ZIP codes may lack complete Census data

**Note:** Christian % represents active congregational presence (church density), not self-identified religious affiliation surveys.- Private school data may have gaps

- Christian population percentages are estimates

---

### Future Enhancements

### **School Locations**- Real-time Census data integration

| Data Type | Source | Count | Used For |- Advanced demographic forecasting

|-----------|--------|-------|----------|- Machine learning predictive models

| **Public Schools** | NCES School Directories + Census EDGE | ~43 schools | EDI supply calculation (default) |- Export functionality for analysis results

| **Charter/Private Schools** | Local data compilation | Variable | Optional EDI supply (user toggle) |

| **CCA Campuses** | Internal data | 2 campuses | Proximity scoring, HPFI calculation |## 📞 Support



**CCA Campus Locations:**For questions or contributions, contact the development team or submit issues through your preferred collaboration platform.

- **West Oak Lane Campus:** 40.056339°N, -75.153858°W

- **Hunting Park Campus:** 40.015278°N, -75.138889°W---

*Built for MBA 8583 - Strategic Analysis*  

---*Cornerstone Christian Academy Expansion Planning*



## 🗺️ **Map Visualization Modes**## Setup



### **1. HPFI (Tuition Potential) - Default**1. Install dependencies: `pip install -r requirements.txt`

- **Color Scale:** Blue (low) → Yellow → Red (high potential)2. Run the app: `streamlit run app.py`

- **Use Case:** Identify affluent, accessible, faith-aligned neighborhoods

- **Best For:** Premium growth targeting, tuition-based enrollment campaigns## Data Connection



### **2. EDI (Access Opportunity)**The app uses placeholder CSV files. To connect real data:

- **Color Scale:** Green (well-served) → Yellow → Red (educational deserts)

- **Use Case:** Find underserved areas where CCA fills real infrastructure gaps- `demographics.csv`: Replace with data from Philly Open Data or NCES. Columns: ZIP, income, EDI, %Christian

- **Best For:** Mission-driven outreach, scholarship targeting, community need assessment- `schools.csv`: Data from NCES or CCA internal. Columns: school_name, type, tuition, rating, lat, lon

- `outreach_plan.csv`: Internal plan data. Columns: month, key_initiative, channel

### **3. Overlay (EDI × HPFI Grid)**

- **Four Quadrants:**For census tract choropleth, integrate geojson from Philly Open Data.

  - **Golden Zones** (Low EDI + High HPFI): Affluent, well-served areas - premium pricing potential

  - **Mission Zones** (High EDI + Low HPFI): Underserved, lower-income - scholarship/mission focus## Features

  - **Affluent Well-Served** (Low EDI + Low HPFI): Saturated markets, secondary priority

  - **Low Priority** (High EDI + High HPFI): Rare combination, investigate individually- Interactive filters

- **Use Case:** Balanced strategy combining economic viability with mission impact- Maps and charts

- Timeline for outreach
### **4. Marketing Zones (Custom Segmentation)**
- **Color Scale:** Dark blue (0-3 points) → Light blue (4-5) → Yellow (6-7) → Red (8-10)
- **Use Case:** Actionable campaign prioritization using composite scoring
- **Best For:** Sales team routing, direct mail campaigns, event targeting

---

## 🔧 **Dashboard Features**

### **Sidebar Filters**
1. **Geographic Scope:**
   - Radius slider (1-35km from CCA campuses)
   - Default: 15km catchment area

2. **Income Targeting:**
   - Min/max household income sliders
   - Dynamic range based on filtered data

3. **High-Potential Focus:**
   - Checkbox to show only HPFI ≥ 0.75 blocks
   - Narrows view to top-quartile opportunities

4. **Refinement Options:**
   - Exclude non-residential areas (parks, industrial zones)
   - Exclude blocks with 0 K-12 children
   - Optional economic opportunity filter (poverty threshold)

5. **Map Layers:**
   - Toggle current student locations
   - Show/hide charter/private schools
   - Filter by school type (Catholic, Baptist, etc.)
   - Include competitors in EDI calculation (toggle)

6. **Data Quality & Technical Details:**
   - Collapsible section with cache timestamps, imputation counts, school data stats
   - For power users only - hidden by default

---

### **Interactive Map**
- **Hover Tooltips:** Block group ID, income, K-12 population, HPFI, EDI, Christian %, poverty rate
- **Click for Details:** Expands block group information panel
- **Competition Schools:** Diamond markers color-coded by school type
- **Current Students:** Optional overlay showing CCA's existing reach

---

### **Top 10 Tables**
1. **Premium Growth Targets:** Highest marketing zone scores (8-10 points)
2. **Golden Zones:** Best HPFI + EDI combination
3. **Top 10 HPFI:** Highest tuition-paying potential blocks

**Columns:** HPFI, EDI, Income, K-12 Population, Block Group ID  
**Export:** Download button for CSV export of full filtered dataset

---

## 📥 **Data Export**

### **CSV Export Features**
- **Button Location:** Bottom of page after Top 10 tables
- **Filename:** `cca_growth_opportunities_YYYYMMDD.csv`
- **Includes:** All filtered block groups with full demographic + scoring data

**Exported Columns:**
- Block Group ID, Latitude, Longitude
- Income, Poverty Rate, Total Population
- K-12 Population (modeled), K-12 Imputed Flag
- HPFI Score, EDI Score
- Christian %, Church Count, Churches per 1k
- Marketing Zone Score
- Nearest Campus Distance

**Use Cases:**
- Import into Salesforce/CRM for territory assignment
- Merge with address databases for direct mail campaigns
- GIS analysis in ArcGIS/QGIS
- Custom reporting in Excel/Tableau

---

## 🛠️ **Technical Architecture**

### **Tech Stack**
- **Frontend:** Streamlit 1.45.1 (Python web framework)
- **Mapping:** Plotly Express (scattermapbox for choropleth visualization)
- **Geospatial:** GeoPandas (block group geometries)
- **Data Processing:** Pandas, NumPy
- **Spatial Analysis:** Custom 2SFCA implementation with haversine distance calculations
- **Deployment:** Streamlit Cloud (automatic GitHub deployment)

### **Data Pipeline**
1. **Census API Integration:** Fetch ACS 2023 block group demographics
2. **Enrollment Modeling:** Downscale tract-level enrollment to block groups
3. **Church Density Analysis:** OpenStreetMap Overpass API for church locations
4. **EDI Calculation:** 2SFCA spatial accessibility model
5. **HPFI Scoring:** Multi-component weighted index with MinMax normalization
6. **Caching:** 1-hour TTL for performance (st.cache_data)

### **Repository Structure**
```
MBA8583/
├── app_block_groups.py              # Main Streamlit dashboard
├── educational_desert_index_bg.py   # 2SFCA EDI calculation module
├── demographics_block_groups.csv    # Pre-loaded demographic data
├── philadelphia_block_groups.geojson # Block group geometries
├── fetch_block_groups.py            # Census API data fetcher
├── fetch_church_density_osm.py      # OpenStreetMap church analysis
├── data/cache/                      # Cached API responses
│   ├── churches_openstreetmap.csv
│   ├── church_density_analysis.csv
│   └── county_christian_adherents_arda2020.csv
└── Cornerstone/
    ├── competitors.csv              # Charter/private school data
    └── student_locations_geocoded.csv # Current CCA students
```

### **Deployment**
- **Platform:** Streamlit Cloud (community plan)
- **Auto-Deploy:** GitHub push to `main` branch triggers redeployment
- **Repository:** https://github.com/lavielehr92/CCAV1.0
- **Branch:** `main`
- **Python Version:** 3.11+
- **Dependencies:** Listed in `requirements.txt`

---

## 📖 **User Guide - Common Scenarios**

### **Scenario 1: Find Premium Growth Neighborhoods**
1. Set **Geographic Scope** to 10km (realistic commute distance)
2. Set **Income Targeting** to $75K - $200K (tuition-viable range)
3. Check **"Show Only High HPFI Areas (≥ 0.75)"**
4. Select **"Marketing Zones"** visualization
5. Review **"Premium Growth Targets"** table (8-10 point blocks)
6. Export CSV and upload to CRM for sales team routing

**Expected Result:** 50-100 high-priority blocks for immediate outreach

---

### **Scenario 2: Identify Mission-Aligned Faith Communities**
1. Keep default **15km Geographic Scope**
2. Remove income filters (inclusive outreach)
3. Select **"HPFI (Tuition Potential)"** visualization
4. Sort map by Christian % (hover tooltips show 36-47% range)
5. Look for blocks with **≥43% Christian** + moderate income
6. Cross-reference with **church locations** (diamond markers)

**Expected Result:** Neighborhoods with strong church presence for partnership opportunities

---

### **Scenario 3: Find Educational Deserts for Scholarship Programs**
1. Set **Geographic Scope** to 20km (broader mission reach)
2. Select **"EDI (Access Opportunity)"** visualization
3. Apply **poverty filter** to focus on lower-income areas
4. Look for **red/orange blocks** (EDI 60-100)
5. Review **"Mission Zones"** in Overlay mode
6. Export blocks with high EDI + low income for scholarship targeting

**Expected Result:** Underserved neighborhoods where CCA fills real educational gaps

---

### **Scenario 4: Analyze Current vs. Potential Student Distribution**
1. Check **"Show Current Student Locations"** in sidebar
2. Select **"HPFI (Tuition Potential)"** visualization
3. Compare **current students** vs. **high-HPFI blocks** (red areas)
4. Identify **high-HPFI blocks with no current students** (untapped markets)
5. Export discrepancies for targeted campaigns

**Expected Result:** Geographic gaps in current enrollment vs. opportunity

---

## ❓ **Frequently Asked Questions**

### **Q: Why does the dashboard show "modeled" K-12 enrollment instead of exact counts?**
**A:** The U.S. Census Bureau doesn't publish school enrollment at the block group level. We use a statistically sound downscaling method:
- Tract-level enrollment rates (ACS S1401) × Block group age 5-17 population (ACS B01001)
- This provides reasonable estimates for neighborhood-level planning
- All estimates are flagged as "modeled" for transparency

### **Q: How often is the data updated?**
**A:** 
- **Census demographics:** ACS 2023 5-year estimates (most recent available, updated annually)
- **Christian %:** OpenStreetMap data (static snapshot, refresh script available)
- **School locations:** Periodically updated from NCES directories
- **Cache refresh:** Dashboard reloads data every 24 hours automatically

### **Q: What does "Christian %" actually measure?**
**A:** Christian % represents **church density** (churches per 1,000 residents) modulated around the county baseline (36.3% from ARDA 2020). It's NOT self-identified religious affiliation surveys. Higher % = more churches nearby = stronger faith community presence.

### **Q: Why do some blocks have HPFI = 0.00?**
**A:** Usually due to:
- Zero population (industrial/park zones) - use "Exclude Non-Residential Areas" filter
- Missing income data
- Very far from CCA campuses (>35km)

### **Q: Can I add my own school locations or update competitors?**
**A:** Yes! Edit `Cornerstone/competitors.csv` with required columns:
```csv
school_name,type,lat,lon,capacity,grades,address,notable_info
```
Push to GitHub and the dashboard auto-updates.

### **Q: How is the 2SFCA method better than simple distance?**
**A:** 
- **Prevents edge effects:** Distant mega-schools don't dominate scores
- **Gravity decay:** Schools 1km away count far more than schools 10km away
- **True crowding:** Measures seats-per-weighted-student, not simple ratios
- **Research-validated:** Standard method in healthcare/education accessibility studies

### **Q: What's the difference between Golden Zones and Premium Growth Targets?**
**A:**
- **Golden Zones:** High HPFI + Low EDI (affluent, already well-served, premium pricing)
- **Premium Growth Targets:** High marketing score (8-10 points) considering proximity, income, AND faith alignment
- Premium Growth is more actionable for sales; Golden Zones are strategic market positioning

---

## 🚨 **Known Limitations**

1. **K-12 Enrollment Modeling:**
   - Downscaled from tract to block group (not exact counts)
   - Assumes uniform enrollment rates within tracts
   - Doesn't account for school choice/charter enrollment patterns

2. **Christian % Methodology:**
   - Based on church locations (supply), not household surveys (demand)
   - Assumes church density correlates with Christian population
   - Limited to OpenStreetMap data quality (may miss smaller churches)
   - All Philly County blocks get same baseline; no suburban variation (yet)

3. **EDI Calculation:**
   - Default model excludes charter/private schools (toggle to include)
   - Assumes 15km max travel distance (may vary by family)
   - Doesn't account for school quality differences
   - Uses estimated school capacity (not always accurate)

4. **Income Data:**
   - ACS 5-year estimates (2019-2023 average, not 2023 snapshot)
   - Block group median = all households averaged (doesn't show within-block variation)
   - Margins of error not displayed (available in ACS technical docs)

---

## 🔮 **Future Enhancements**

### **Planned Features**
- [ ] **Real-time enrollment tracking:** Integrate with CCA student information system
- [ ] **Predictive modeling:** Machine learning to forecast enrollment likelihood
- [ ] **Competition analysis:** School quality scores (GreatSchools ratings, test scores)
- [ ] **Transportation modeling:** SEPTA route integration for transit accessibility
- [ ] **Mobile app:** Field use for admissions staff during community events
- [ ] **A/B testing framework:** Track campaign effectiveness by geographic zone
- [ ] **Temporal analysis:** Year-over-year demographic shifts

### **Data Improvements**
- [ ] **Real broadband data:** Replace poverty proxy with ACS S2801 (when available)
- [ ] **Household survey data:** Commission custom Christian affiliation study
- [ ] **School capacity verification:** Audit NCES estimates with district data
- [ ] **Suburban expansion:** Include Bucks, Chester, Delaware, Montgomery counties

### **UX Enhancements**
- [ ] **Custom territory drawing:** Let users define custom polygons
- [ ] **Multi-year comparison:** Slider to view historical demographic trends
- [ ] **3D visualization:** Population density + HPFI as height maps
- [ ] **Mobile-responsive design:** Optimize for tablet/phone field use

---

## 📜 **Data Privacy & Usage Policy**

### **Student Privacy**
- Current student locations are **aggregated and de-identified**
- No individual student names, addresses, or personal information displayed
- Complies with FERPA (Family Educational Rights and Privacy Act)

### **Data Usage**
- Dashboard is for **internal CCA use only**
- Census data is public domain
- Exported CSVs should be stored securely and not shared publicly
- Do not use for discriminatory practices (income/race-based exclusion)

### **Ethical Considerations**
- HPFI prioritizes economic capacity but **does not exclude low-income families**
- EDI highlights underserved areas for **scholarship/mission focus**
- Dashboard supports **diverse and inclusive enrollment growth**
- Christian % used for mission alignment, **not as exclusion criteria**

---

## 🔗 **Resources**

### **Technical Documentation**
- **Streamlit Docs:** https://docs.streamlit.io
- **ACS Data Dictionary:** https://www.census.gov/programs-surveys/acs/technical-documentation.html
- **2SFCA Methodology Paper:** Luo & Wang (2003) - "Measures of Spatial Accessibility to Health Care"
- **ARDA Data Portal:** https://www.thearda.com/data-archive

### **Related Tools**
- **Census Reporter:** https://censusreporter.org (explore any block group demographics)
- **PolicyMap:** https://www.policymap.com (commercial demographic analysis)
- **School Attendance Boundary Survey:** https://nces.ed.gov/programs/edge/SABS

---

## 📝 **Version History**

### **v2.0 (November 2025) - Current**
- ✅ Added block-level Christian % variation (OpenStreetMap church density)
- ✅ Integrated Christian % into HPFI (12% weight)
- ✅ Enhanced marketing zone scoring with 3-tier Christian % classification
- ✅ Reorganized sidebar for production readiness
- ✅ Implemented rigorous 2SFCA for EDI calculation
- ✅ Added campus proximity to HPFI (13% weight)
- ✅ Fixed competition schools map rendering errors
- ✅ Removed first-generation college metrics (not available in ACS)

### **v1.0 (Initial Release)**
- Basic HPFI calculation (income, poverty, K-12, EDI)
- Simple distance-based EDI
- Marketing zone framework
- CSV export functionality

---

## 📞 **Support**

**Questions? Issues? Feature Requests?**

🐛 **Bug Reports:** https://github.com/lavielehr92/CCAV1.0/issues  
📧 **Contact:** Open a GitHub issue or contact your data team

---

**Last Updated:** November 11, 2025  
**Document Version:** 2.0  
**Dashboard Version:** 2.0 (Streamlit Cloud)

---

*Built for Cornerstone Christian Academy's mission to provide excellent, Christ-centered education to Philadelphia families.*
