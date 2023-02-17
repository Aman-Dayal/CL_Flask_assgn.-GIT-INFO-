from flask import Flask, request, redirect, render_template
import json
import requests
import pymongo
from pymongo.errors import DuplicateKeyError


app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/git_user')


@app.route('/git_user')
def git_user():
    return render_template('index2.html')



@app.route('/gt_user', methods=['POST'])
def gt_user():
    if request.method == 'POST':

        guser = json.loads(request.data)
        print(guser)
        
        response = requests.get("https://api.github.com/users/"+guser["prof"])
        print(response.status_code)
       


        if response.status_code == 200:
            client = pymongo.MongoClient("mongodb://localhost:27017/git_test")
            db = client.get_database()
            collection = db.get_collection("users")
            daata = response.json()
            # collection.delete_many()
            data = {k: v for k, v in daata.items() if not k.endswith("url") if v}

            # for key , value in data.items():
            # # for k, v in user.items():
            #     if ~key.endswith("url"):
            #         data.update({ key : value })



            try:
                daata['_id'] = daata['login']

                collection.insert_one(daata)

                print(f"Successfully inserted"+ daata['login'] +"into the database.")
                data1 =data
                data1['Source']='Git Api'

                return data1

            except DuplicateKeyError:
                # print(data)
                results = collection.find_one({"_id": guser["prof"]})
                results = {k: v for k, v in results.items() if not k.endswith("url") if v}
                results['Source'] ='MongoDB'
                print("data already stored")
                return results
        else :
            
            return {'Source':"_"*10+'Not Found'+"_"*10}
            
@app.route('/user_repo', methods=['POST'])
def user_repo():
    if request.method == 'POST':

        urepo = json.loads(request.data)
        response1 = requests.get("https://api.github.com/users/"+urepo["prof"]+"/repos")
        repos =response1.json()
        # Filtered_repos = [{k: v for k, v in repo.items() if not k.endswith("url")} for repo in repos]
        
        # for dta in Filtered_repos:
        #     for key in ['owner','license']:
        #         dta.pop(key)
        # print(Filtered_repos)
        # print(repos)
        return repos




if __name__ == "__main__":
    app.run(debug=True)

# HOW TO DEFINE A GLOBAL VARIABLE IN FLASK