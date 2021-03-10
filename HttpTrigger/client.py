'''
Author: Jaime Badiola Ramos
Email: Jaime.badiolaramos@gmail.com
Date: 2021-01-22
'''

import requests
from forge import ForgeApp

Client = ForgeApp(
    "387hqySs00T8SkLPVzq9MtmgjJ02NVhM"
    ,"hpvc6MpeybnyYG1c"
    ,hub_id="b.e7939612-1ad1-4f49-b4d7-6e85aee718a8"
    ,three_legged=True
    ,redirect_uri='https://forge-test.azurewebsites.net'
    ,username='jamieramos@reds10.com'
    ,password='Cax49398'
    ,grant_type="implicit"
)

Client_two_legged = ForgeApp(
    "387hqySs00T8SkLPVzq9MtmgjJ02NVhM"
    ,"hpvc6MpeybnyYG1c"
    ,hub_id="b.e7939612-1ad1-4f49-b4d7-6e85aee718a8"
    ,three_legged=False
    ,redirect_uri='https://forge-test.azurewebsites.net'
    ,username='jamieramos@reds10.com'
    ,password='Cax49398'
    ,grant_type="implicit")