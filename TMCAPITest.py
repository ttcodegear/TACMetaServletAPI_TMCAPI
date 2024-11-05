import requests
from pathlib import Path

def main():
  tenant = 'https://api.ap.cloud.talend.com'
  #apitoken = 'yu6M5HV9TLykf1UXkTPo8DEO5....'
  apitoken = Path('personal_token.txt').read_text()
  headers = {
    'Authorization': 'Bearer ' + apitoken
  }
  taskid = '661ca072c77502053bedf8ad'
  url = tenant + '/processing/executables/tasks/' + taskid + '/executions?offset=0&limit=100'
  print(url)
  resp = requests.get(url, headers=headers)
  if resp.status_code == 200:
    resp = resp.json()
    #print(resp['total'])
    for exe in resp['items']:
      execid = exe['executionId']
      url = tenant + '/monitoring/executions/' + execid + '/logs?fileFormat=TEXT'
      print(url)
      resp = requests.post(url, headers=headers)
      if resp.status_code == 200:
        resp = resp.json()
        #print(resp['token']) #Token used to check the status of the log file generation
        url = tenant + '/monitoring/executions/' + execid + '/logs/status'
        print(url)
        resp = requests.post(url, headers=headers, data=resp['token'])
        if resp.status_code == 200:
          resp = resp.json()
          if resp['status'] == 'READY':
            #print(resp['presignedURL']) # URL to download full logs, valid for 60 minutes
            resp = requests.get(resp['presignedURL'])
            if resp.status_code == 200:
              with open(taskid + '_' + exe['triggerTimestamp'].replace(':', '-') + '_' + execid + '.log', mode='wb') as f:
                f.write(resp.content)
                print(f.name)

if __name__ == '__main__':
  main()
