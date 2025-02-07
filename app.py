
################################################################################
### Loading the required modules
from flask import Flask, request, jsonify, render_template, send_file
import requests
from wikidataintegrator import wdi_core
import json
import re
################################################################################


app = Flask(__name__)

################################################################################
### The landing page
@app.route('/')
def home():
    return render_template('home.html')
################################################################################

################################################################################
### Pages under 'Project Information'
@app.route('/information/mission_and_vision')
def mission_and_vision():
    return render_template('information/mission_and_vision.html')

@app.route('/information/research_lines')
def research_lines():
    return render_template('information/research_lines.html')

@app.route('/case_studies_and_regulatory_questions')
def case_studies_and_regulatory_questions():
    return render_template('information/case_studies_and_regulatory_questions.html')

@app.route('/information/partners_and_consortium')
def partners_and_consortium():
    return render_template('information/partners_and_consortium.html')

@app.route('/information/contact')
def contact():
    return render_template('information/contact.html')

@app.route('/youp')
def youp():
    return render_template('case_studies/thyroid/youp.html')

################################################################################

################################################################################
### Pages under 'Services' 

# Page to list all the services based on the list of services on the cloud repo.
@app.route('/templates/services/service_list')
def service_list():
    # Github API link to receive the list of the services on the cloud repo:
    url = f'https://api.github.com/repos/VHP4Safety/cloud/contents/docs/service'
    response = requests.get(url)

    # Checking if the request was successful (status code 200).
    if response.status_code == 200:
        # Extracting the list of files.
        service_content = response.json()

        # Separating .json and .md files.
        json_files = {file['name']: file for file in service_content if file['type'] == 'file' and file['name'].endswith('.json')}
        md_files = {file['name']: file for file in service_content if file['type'] == 'file' and file['name'].endswith('.md')}
        png_files = {file['name']: file for file in service_content if file['type'] == 'file' and file['name'].endswith('.png')}

        # Creating an empty list to store the results. 
        services = []

        # Fetching the .json files.
        for json_file_name, json_file in json_files.items():
            # Skipping the template.json file. 
            if json_file_name == 'template.json':
                continue
 
            json_url = json_file['download_url']  # Using the download URL from the API response.
            json_response = requests.get(json_url)

            if json_response.status_code == 200:
                json_data = json_response.json()
                
                # Extracting the 'service' field from the json file.
                service_name = json_data.get('service')
                description_string = json_data.get('description') 

                if service_name:
                    # Replacing the .json extension with the .md to get the corresponding .md file.
                    md_file_name = json_file_name.replace('.json', '.md')
                    html_name = json_file_name.replace('.json', '.html')
                    url = "https://cloud.vhp4safety.nl/service/"+ html_name 

                    if md_file_name in md_files:
                        md_file_url = f'https://raw.githubusercontent.com/VHP4Safety/cloud/main/docs/service/{md_file_name}'
                    else:
                        md_file_url = "md file not found"
                    png_file_name = md_file_name.replace('.md', '.png')

                    if png_file_name in png_files:
                        png_file_url = f'https://raw.githubusercontent.com/VHP4Safety/cloud/main/docs/service/{png_file_name}'
                        services.append({
                            'service': service_name,
                            'url': url,
                            'meta_data': md_file_url,
                            'description': description_string,
                            'png': png_file_url
                        })
                    else:
                        services.append({
                            'service': service_name,
                            'url': url,
                            'meta_data': md_file_url,
                            'description': description_string,
                            'png': "../../static/images/logo.png"
                        })

        mid=len(services) // 2
        chunk1 = services[ :mid]
        chunk2 = services[mid: ]
        print("Chunk1:")
        print(chunk1)

        print("Chunk2:")
        print(chunk2)

        # Passing the services data to the template after processing all JSON files.
        return render_template('services/service_list.html', chunk1=chunk1, chunk2=chunk2)
    else:
        return f"Error fetching files: {response.status_code}"

    # return render_template('services/service_list.html')

@app.route('/templates/services/qsprpred')
def qsprpred():
    return render_template('services/qsprpred.html')
    
################################################################################

################################################################################
### Pages under 'Case Studies' 

@app.route('/templates/case_studies/kidney/kidney')
def kidney_main():
    return render_template('case_studies/kidney/kidney.html')

@app.route('/templates/case_studies/parkinson/parkinson')
def parkinson_main():
    return render_template('case_studies/parkinson/parkinson.html')

@app.route('/templates/case_studies/parkinson/workflows/parkinson_hackathon_workflow')
def parkinson_hackathon_workflow():
    return render_template('case_studies/parkinson/workflows/parkinson_hackathon_workflow.html')

@app.route('/templates/case_studies/thyroid/thyroid')
def thyroid_main():
    return render_template('case_studies/thyroid/thyroid.html')

@app.route('/templates/case_studies/thyroid/workflows/thyroid_hackathon_demo_workflow')
def thyroid_workflow_1():
    return render_template('case_studies/thyroid/workflows/thyroid_hackathon_demo_workflow.html')
@app.route('/templates/case_studies/thyroid/workflows/ngra_silymarin')
def ngra_silymarin():
    return render_template('case_studies/thyroid/workflows/ngra_silymarin.html')

################################################################################


################################################################################
### Tests for API calls and interactive pages.
@app.route('/get_dummy_data', methods=['GET'])
def get_dummy_data():
    results = [
    {
        "Compound": "Compound1" ,
        "SMILES": "Smile 1" 
    },
    {
        "Compound": "Compound1" ,
        "SMILES": "Smile 1" 
    },
    {
        "Compound": "Compound1" ,
        "SMILES": "Smile 1" 
    }
    ]
    return results, 200

@app.route('/get_compounds', methods=['GET'])
def get_compounds():
    # Setting up the url for sparql endpoint.
    compoundwikiEP = "https://compoundcloud.wikibase.cloud/query/sparql"

    # Setting up the sparql query for the full list of compounds.
    sparqlquery_full = '''
    PREFIX wd: <https://compoundcloud.wikibase.cloud/entity/>
    PREFIX wdt: <https://compoundcloud.wikibase.cloud/prop/direct/>

    SELECT DISTINCT (substr(str(?cmp), 45) as ?ID) (?cmpLabel AS ?Term)
        ?SMILES (?cmp AS ?ref)
    WHERE{
        { ?parent wdt:P21 wd:Q2059 ; wdt:P29 ?cmp . } UNION { ?cmp wdt:P21 wd:Q2059 . }
    ?cmp wdt:P1 ?type ; rdfs:label ?cmpLabel . FILTER(lang(?cmpLabel) = 'en')
    ?type rdfs:label ?typeLabel . FILTER(lang(?typeLabel) = 'en')
    OPTIONAL { ?cmp wdt:P7 ?chiralSMILES }
    OPTIONAL { ?cmp wdt:P12 ?nonchiralSMILES }
    BIND (COALESCE(IF(BOUND(?chiralSMILES), ?chiralSMILES, 1/0), IF(BOUND(?nonchiralSMILES), ?nonchiralSMILES, 1/0),"") AS ?SMILES)
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    '''

     # Making the SPARQL query
    compound_dat = wdi_core.WDFunctionsEngine.execute_sparql_query(sparqlquery_full, endpoint=compoundwikiEP, as_dataframe=True)

    # Organizing the output into a list of dictionaries
    compound_list = []
    for _, row in compound_dat.iterrows():
        compound_list.append({"Term": row[2], "SMILES": row[0]})

    return jsonify(compound_list), 200

@app.route('/get_compounds_parkinson', methods=['GET'])
def get_compounds_parkinson():
    # Setting up the url for sparql endpoint.
    compoundwikiEP = "https://compoundcloud.wikibase.cloud/query/sparql"

    # Setting up the sparql query for the full list of compounds.
    sparqlquery_full = '''
    PREFIX wd: <https://compoundcloud.wikibase.cloud/entity/>
    PREFIX wdt: <https://compoundcloud.wikibase.cloud/prop/direct/>

    SELECT DISTINCT (substr(str(?cmp), 45) as ?ID) (?cmpLabel AS ?Term)
        ?SMILES (?cmp AS ?ref)
    WHERE{
        { ?parent wdt:P21 wd:Q5050 ; wdt:P29 ?cmp . } UNION { ?cmp wdt:P21 wd:Q5050 . }
    ?cmp wdt:P1 ?type ; rdfs:label ?cmpLabel . FILTER(lang(?cmpLabel) = 'en')
    ?type rdfs:label ?typeLabel . FILTER(lang(?typeLabel) = 'en')
    OPTIONAL { ?cmp wdt:P7 ?chiralSMILES }
    OPTIONAL { ?cmp wdt:P12 ?nonchiralSMILES }
    BIND (COALESCE(IF(BOUND(?chiralSMILES), ?chiralSMILES, 1/0), IF(BOUND(?nonchiralSMILES), ?nonchiralSMILES, 1/0),"") AS ?SMILES)
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    '''

     # Making the SPARQL query
    compound_dat = wdi_core.WDFunctionsEngine.execute_sparql_query(sparqlquery_full, endpoint=compoundwikiEP, as_dataframe=True)

    # Organizing the output into a list of dictionaries
    compound_list = []
    for _, row in compound_dat.iterrows():
        compound_list.append({"Term": row[2], "SMILES": row[0]})

    return jsonify(compound_list), 200


def fetch_predictions(smiles, models, metadata, threshold=6.5):
    url = "https://qsprpred.cloud.vhp4safety.nl/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=0",
    }
    body = {
        "smiles": smiles,
        "models": models,
        "format": "json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        predictions = response.json()
        filtered_predictions = []
        for prediction in predictions:
            filtered_prediction = {"smiles": prediction["smiles"]}
            for key, value in prediction.items():
                if key != "smiles" and float(value) >= threshold:
                    new_key = re.sub(r'prediction \((.+)\)', r'\1', key)
                    filtered_prediction[new_key] = value
            filtered_predictions.append(filtered_prediction)
            # Ensure metadata exists for the model before updating
            if models and models[0] in metadata:
                filtered_prediction.update(metadata.get(models[0], {}))
        print(f"{len(filtered_predictions)} result(s)")
        return filtered_predictions
    else:
        return {"error": response.text}
    
@app.route("/get_predictions", methods=["POST"])
def get_predictions():
    data = request.json
    smiles = data.get("smiles", [])
    models = data.get("models", [])
    metadata = data.get("metadata", {})
    threshold = data.get("threshold", 6.5)

    results = fetch_predictions(smiles, models, metadata, threshold)
    return jsonify(results)


################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

