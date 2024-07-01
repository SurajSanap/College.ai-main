import streamlit as st
from streamlit_lottie import st_lottie 
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import ast
import requests
from bs4 import BeautifulSoup

def get_date(day_cnt):
    """
    Monday == day_cnt == 0
    Tuesday == day_cnt == 1
    and so on 
     """
    date = datetime.now()
    date_list = []
    while len(date_list) < 2:
        date += timedelta(days=1)
        if date.weekday() == day_cnt:  
            date_list.append(date.strftime("%d/%m/%Y"))
    
    return date_list

    
def get_all_contest():
    """
    all_contest={
    platform_icon:"",
    contest_name:"",
    contest_date:"",
    contest_time:"",
    contest_link:""
    }

    """
    all_contest=[]
    # GFG
    sunday=get_date(6)
    saturday=get_date(5)
    gfg=[{"platform_icon":"https://media.geeksforgeeks.org/wp-content/cdn-uploads/20210420155809/gfg-new-logo.png",
          "contest_name":"Weekly Contest",
          "contest_date":sunday[0],
          "contest_time":"19:00",
          "contest_link":"https://www.geeksforgeeks.org/events/rec/gfg-weekly-coding-contest"},
          {"platform_icon":"https://media.geeksforgeeks.org/wp-content/cdn-uploads/20210420155809/gfg-new-logo.png",
          "contest_name":"Weekly Contest",
          "contest_date":sunday[1],
          "contest_time":"19:00",
          "contest_link":"https://www.geeksforgeeks.org/events/rec/gfg-weekly-coding-contest"}]
    all_contest.extend(gfg)

    leetcode=[{"platform_icon":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/LeetCode_Logo_black_with_text.svg/458px-LeetCode_Logo_black_with_text.svg.png",
          "contest_name":"Weekly Contest",
          "contest_date":sunday[0],
          "contest_time":"08:00",
          "contest_link":"https://leetcode.com/contest/"},

        {"platform_icon":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/LeetCode_Logo_black_with_text.svg/458px-LeetCode_Logo_black_with_text.svg.png",
          "contest_name":"Biweekly Contest",
          "contest_date":saturday[0],
          "contest_time":"20:00",
          "contest_link":"https://leetcode.com/contest/"},

        {"platform_icon":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/LeetCode_Logo_black_with_text.svg/458px-LeetCode_Logo_black_with_text.svg.png",
          "contest_name":"Weekly Contest",
          "contest_date":sunday[1],
          "contest_time":"08:00",
          "contest_link":"https://leetcode.com/contest/"},
         
        {"platform_icon":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/LeetCode_Logo_black_with_text.svg/458px-LeetCode_Logo_black_with_text.svg.png",
          "contest_name":"Biweekly Contest",
          "contest_date":saturday[1],
          "contest_time":"20:00",
          "contest_link":"https://leetcode.com/contest/"}]
    all_contest.extend(leetcode)
    
    # codechef
    try:
        url ="https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=all" 
        response = requests.get(url)
        dict_obj = ast.literal_eval(response.text)
        formatted_contests=[]
        for contest in dict_obj["future_contests"]:
            start_datetime = datetime.strptime(contest['contest_start_date'], '%d %b %Y %H:%M:%S')
            contest_date = start_datetime.strftime('%d/%m/%Y')
            contest_time = start_datetime.strftime('%H:%M')
            formatted_contest = {
            'platform_icon': 'https://cdn.codechef.com/sites/all/themes/abessive/cc-logo.png',  
            'contest_name': contest['contest_name'],
            'contest_date': contest_date,
            'contest_time': contest_time,
            "contest_link":"https://www.codechef.com/contests"
            }
            formatted_contests.append(formatted_contest)
        codechef=formatted_contests
        all_contest.extend(codechef)
    except:
        pass

   #codeforces
    try:
        codeforces_url = "https://codeforces.com/contests"
        response = requests.get(codeforces_url)
        soup = BeautifulSoup(response.text, "html.parser")
        codeforces = []
        upcoming_contests = soup.find_all("div", {"class": "datatable"})[0].find_all("tr")
        for contest in upcoming_contests:
            columns = contest.find_all("td")
            if len(columns) == 6:
                name = (
                    columns[0]
                    .text.strip()
                    .replace("Enter", " ")
                    .replace("Virtual participation", " ")
                    .replace("\u00bb", " ")
                )
                start_time_str = columns[2].text.strip()
                datetime_obj = datetime.strptime(start_time_str, '%b/%d/%Y %H:%M')
                date_obj = datetime_obj.date()
                time_obj = datetime_obj.time()
                start_date = date_obj.strftime('%d/%m/%Y')
                start_time = time_obj.strftime('%H:%M')
                
                name = " ".join(
                    line.strip() for line in name.splitlines() if line.strip()
                )
                codeforces.append(
                    {   "platform_icon":"https://asset.brandfetch.io/idMR4CMjcL/idPWmM8aOc.png?updated=1716797858256",
                        "contest_name": name,
                        "contest_date": start_date,
                        "contest_time":start_time,
                        "contest_link":"https://codeforces.com/contests",
                        
                    }
                )
        all_contest.extend(codeforces)
    except:
        pass



    all_contest = sorted(all_contest, key=lambda x: (datetime.strptime(x['contest_date'], '%d/%m/%Y'), x['contest_time']))
    return all_contest

def main():
    st.write("<h1><center>Contest Calendar</center></h1>", unsafe_allow_html=True)
    st.write("<center>Dominate the Leaderboard: Never Miss a Contest Again!</center>", unsafe_allow_html=True)
    with open('src/contest.json', encoding='utf-8') as anim_source:
        animation = json.load(anim_source)
    st_lottie(animation, 1, False, True, "high",150,-200)
    contest_list=get_all_contest()
    combined_contests = {
    "platform_icon": [],
    "contest_name": [],
    "contest_date": [],
    "contest_time": [],
    "contest_link": [],

    }
    for contest in contest_list:
        combined_contests["platform_icon"].append(contest["platform_icon"])
        combined_contests["contest_name"].append(f'<a href="{contest["contest_link"]}" target="_blank">{contest["contest_name"]}</a>')
        combined_contests["contest_date"].append(contest["contest_date"])
        combined_contests["contest_time"].append(contest["contest_time"])
        combined_contests["contest_link"].append(contest["contest_link"])
    data_df = pd.DataFrame(
    {
        "S.no": np.arange(1, len(contest_list) + 1),
        "Contest Name": combined_contests["contest_name"],
        "Platform Name": combined_contests["platform_icon"],
        "Contest Date": combined_contests["contest_date"],
        "Contest Time": combined_contests["contest_time"],
        "Contest Link": combined_contests["contest_link"]

    }
    )

       
    def make_clickable(name, link):
        return f'<a href="{link}" target="_blank">{name}</a>'
    def render_table(df):
        df['Platform Name'] = df['Platform Name'].apply(lambda x: f'<img src="{x}" width="80" height="30">')
        return df.to_html(escape=False, index=False)
    
    data_df['Contest Name'] = data_df.apply(lambda row: make_clickable(row['Contest Name'], row['Contest Link']), axis=1)
    data_df['Contest Date'] = pd.to_datetime(data_df['Contest Date'],format="%d/%m/%Y")
    data_df['Contest Time'] = pd.to_datetime(data_df['Contest Time'], format='%H:%M').dt.time
    data_df = data_df.drop(columns=['Contest Link'])
    sorted_data_df = data_df.sort_values(by=['Contest Date','Contest Time'])
    st.markdown("""<style>
    .table-container {
        width: 100%;
        display: flex;
        justify-content: center;
    }
    table {
        border-collapse: collapse;
        width: 80%;
        margin: 20px 0;
        font-family: Arial, sans-serif;
    }
    th, td {
        text-align: center;
        padding: 8px;
    }
    th {
        background-color: #cf96df;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
                color: #000;
    }
    tr:nth-child(odd) {
        background-color: #f9f9f9;
                color: #000;
    }
    tr:hover {
        background-color: #cf96df;
    }
    a {
        text-decoration: none;
        color: #007BFF;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="table-container">' + render_table(sorted_data_df) + '</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()