
################################################################################
### Loading the required modules
from flask import Flask, request, jsonify, render_template, send_file
import requests
from wikidataintegrator import wdi_core
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

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        # Extracting the list of files.
        service_content = response.json()
        
        ##########################################
        ### Filtering the .md files in service_content.
        service_list = [file['name'] for file in service_content if file['type'] == 'file' and file['name'].endswith('.md')]
        ##########################################

        ##########################################
        ### Trying to add links to the items -- could not manage to get it work 
        # md_files_list = [
        #    {
        #         'name': file['name'],
        #         'url': f'https://github.com/VHP4Safety/cloud/blob/main/{file["name"]}'
        #     }
        #     for file in service_content if file['type'] == 'file' and file['name'].endswith('.md')
        # ]
        ##########################################

        return render_template('services/service_list.html', files=service_list)
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

@app.route('/templates/case_studies/thyroid/thyroid')
def thyroid_main():
    return render_template('case_studies/thyroid/thyroid.html')

@app.route('/templates/case_studies/thyroid/workflows/thyroid_hackathon_demo_workflow')
def thyroid_workflow_1():
    return render_template('case_studies/thyroid/workflows/thyroid_hackathon_demo_workflow.html')
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

    SELECT (substr(str(?cmp), 45) as ?ID) (?cmpLabel AS ?Term)
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

    # Making the sparql query.
    compound_dat = wdi_core.WDFunctionsEngine.execute_sparql_query(sparqlquery_full, endpoint=compoundwikiEP, as_dataframe=True)

    # Organizing the output into a list object.
    SMILES = compound_dat[compound_dat.columns[0]]
    ID     = compound_dat[compound_dat.columns[1]]
    Term   = compound_dat[compound_dat.columns[2]]
    ref    = compound_dat[compound_dat.columns[3]]

    compound_list = []
    compound_list.append(Term.tolist())
    compound_list.append(SMILES.tolist())
    compound_list.append(ref.tolist())

    return jsonify(compound_list), 200

################################################################################

if __name__ == '__main__':
    app.run(debug=True, port=5001)

