### YouTube Data Analysis Using PostgreSQL and Streamlit 📊🎥

🔍 **Project Overview**  
In this project, I leveraged **PostgreSQL** for database management and **Streamlit** to build an interactive dashboard, aimed at analyzing YouTube channel data. The analysis focuses on video performance, channel engagement, and content categorization, enabling efficient exploration of key metrics such as views, video categories, and channel statistics.  

---

### Key Steps

**1. Scraping**  
Using the YouTube API and custom utility module (`yt_yt`), I retrieved:  
- Channel Information: ID, name, and metadata  
- Video Details: Titles, view counts, categories, and published dates  
- Category Mapping: YouTube category IDs mapped to names  

**2. Migration**  
The scraped data was structured and stored in a **PostgreSQL** database with **SQLAlchemy** models:  
- Channel Data: Stored in `YtChannelModel`  
- Video Data: Stored in `YtVideosModel`, linking to channels and categories  
- Optional: Comments in `YtCommentsModel`  

**3. Ask Questions**  
I built an interactive **Streamlit** dashboard to answer questions such as:  
- View trends of the last 50 videos via line charts (using **Altair**)  
- Filter videos by category, grouped by channel, with clickable YouTube links  

**4. Analysis**  
Key analyses performed:  
- **View Trends Visualization**: Displayed video view trends over time  
- **Category Exploration**: Showed top channels for specific video categories  
- **Interactive Video Exploration**: Provided direct links to videos for detailed exploration  

---

### **Conclusion**  
This project highlights a streamlined process for scraping, migrating, and analyzing YouTube data. The **interactive dashboard** provides valuable insights into channel performance and content trends.  

#YouTubeAnalysis #DataScience #PostgreSQL #Streamlit #Altair #DataVisualization #YouTubeAPI #SQLAlchemy