import streamlit as st

# Sample data (replace this with your actual data)
docker_containers = [
    {"name": "1", "ports": "8080:80", "status": "running", "image": "nginx:latest"},
    {"name": "2", "ports": "3306:3306", "status": "stopped", "image": "mysql:5.7"},
    {"name": "3", "ports": "6379:6379", "status": "running", "image": "redis:alpine"}
]

def get_status_icon(status):
    if status == "running":
        return "✅"
    elif status == "stopped":
        return "🛑"
    else:
        return "❓"

def container():
    #st.set_page_config(page_title="Docker Containers", layout="wide")

    st.title("Docker Containers")

    # Custom CSS to style the cards
    st.markdown("""
    <style>
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .card:hover {
                border : 1px solid green;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                cursor:pointer;
        }
        .card {
                text-decoration: none;
            border : 1px solid black;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
                width: max-content;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .card-content {
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)



    # Generate cards for each Docker container
    card_html =""" 
     
      <div class="container">  
     
        """
    for container in docker_containers:
        card_html += f"""

        
    <a href="/logpage/{container['name']}"  target="_self">
        <div class="card">
            <div class="card-title">{container['name']}</div>
            <div class="card-content">
                <p><strong>Ports:</strong> {container['ports']}</p>
                <p><strong>Status:</strong> {get_status_icon(container['status'])} {container['status']}</p>
                <p><strong>Image:</strong> {container['image']}</p>
            </div>
        </div>
    
    </a>
        

        """


    # Close the container
    st.markdown( card_html , unsafe_allow_html=True)
   
    

    