import json
import base64
import requests

def main():
  params_dict = {"actionName": "taskLog","authPass": "admin","authUser": "security@company.com","lastExecution": False,"taskId": 1}
  json_str = json.dumps(params_dict).encode('utf-8')
  base64_str = base64.b64encode(json_str).decode()
  metaservlet_url = 'http://192.168.149.136:8080/org.talend.administrator-8.0.1/metaServlet?' + base64_str
  print(metaservlet_url)
  resp = requests.get(metaservlet_url)
  if resp.status_code == 200:
    json_dict = json.loads(resp.text)
    print(json_dict['result'])

if __name__ == '__main__':
  main()
