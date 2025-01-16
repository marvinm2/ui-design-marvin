from flask import Flask, render_template
import requests

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


if __name__ == '__main__':
    app.run(debug=True)

