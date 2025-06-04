
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

from parse_module import *

app = FastAPI()


class Application(BaseModel):
    id: float
    application_date: str
    contracts: str | float | dict | list

@app.get("/")
def read_root():
    return {"Response": "OK"}


@app.put("/process-feature")
def process_feature(app: Application):
    contracts = process_contracts(app.contracts)
    application_date = process_app_date(app.application_date)

    if isinstance(contracts, int):
        return {'tot_claim_cnt_l180d': -3,
                'disb_bank_loan_wo_tbc': -3,
                'day_sinlastloan': -3}
    
    tot_claim_cnt_l180d = cc180(application_date, contracts)
    disb_bank_loan_wo_tbc = disb_loan_sum(contracts)
    day_sinlastloan = days_since_last_loan(application_date, contracts)

    result = {'tot_claim_cnt_l180d': int(tot_claim_cnt_l180d),
                'disb_bank_loan_wo_tbc': disb_bank_loan_wo_tbc,
                'day_sinlastloan': int(day_sinlastloan)}
    try:
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
