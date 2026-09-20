from flask import abort

def can_access_contract(user_id, contract):
    return user_id in {
        contract.hirer_id,
        contract.translator_id
    }

def require_contract_access(user_id, contract):
    if not can_access_contract(user_id, contract):
        abort(403)
