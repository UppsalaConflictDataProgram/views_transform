"""
Recieves .parquet bytes, does a requested transformation, and returns data in the same format.
"""
import io
import os
import re

import pydantic
import requests
import fastapi

import pandas as pd
import url_args
from transforms import timelag

ROUTER_URL = "http://0.0.0.0:8000"

app = fastapi.FastAPI()

"""
Each transform takes two arguments:

    rhs, which is the URL to the router resource to be transformed
    The dataset df, which is retrieved from the rhs
"""

TRANSFORMS = {
        "priogrid_month":{
            "identity":lambda r,df: df,
            "tlag":timelag
            },
        "country_month":{
            "identity":lambda r,df: df,
            "tlag":timelag
            }
        }

@app.get("/{loa}/{transform_name}/{url_args_raw}/{rhs:path}")
def transform(loa:str, transform_name:str, url_args_raw:url_args.url_args, rhs:str):
    rhs_url = os.path.join(ROUTER_URL,loa,rhs)
    rhs_request = requests.get(rhs_url)

    if not rhs_request.status_code == 200:
        return fastapi.Response(f"Router returned {rhs_request.status_code} "
                f"{rhs_request.content}",
                status_code=rhs_request.status_code)


    try:
        data = pd.read_parquet(io.BytesIO(rhs_request.content))
    except ValueError:
        return fastapi.Response(f"RHS {rhs} returned wrong data type "
                f"{str(rhs_request.content)}",
                status_code=500)

    try:
        fn = TRANSFORMS[loa][transform_name]
    except KeyError:
        return fastapi.Response(f"Transform not found: {loa}>{transform_name}", status_code=404)

    args = [rhs_url,data]
    if url_args_raw == "_":
        pass
    else:
        args = args + url_args.parse(url_args_raw)
        
    try:
        data = fn(*args)
    except TypeError as e:
        # Wrong number of arguments
        return fastapi.Response(content=str(e),status_code=400)

    fake_file = io.BytesIO()
    data.to_parquet(fake_file,compression="gzip")

    return fastapi.Response(fake_file.getvalue(),media_type="application/octet-stream")
