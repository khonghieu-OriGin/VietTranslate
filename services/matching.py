import unicodedata
from models import Job, Proposal, Contract, TranslatorPreference, TranslatorProfile, User
from datetime import datetime

def normalize_text(value):
    if not value:
        return ''
    return unicodedata.normalize('NFKD', str(value)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()

def calculate_job_match_score(translator, job):
    # Base score 0 to 100
    score = 0
    reasons = []
    
    # 1. Language (40 points)
    pref = translator.preference
    prof = translator.profile
    
    translator_langs = []
    if pref and pref.languages:
        translator_langs = [normalize_text(l) for l in pref.languages.split(',')]
    elif prof and prof.languages:
        translator_langs = [normalize_text(l) for l in prof.languages.split(',')]
        
    source_norm = normalize_text(job.source_lang)
    target_norm = normalize_text(job.target_lang)
    
    if source_norm in translator_langs and target_norm in translator_langs:
        score += 40
        reasons.append("Khớp ngôn ngữ")
    elif source_norm in translator_langs or target_norm in translator_langs:
        score += 20
        reasons.append("Khớp một phần ngôn ngữ")

    # 2. Service Type (25 points)
    job_group = job.display_category_group
    job_type = job.display_service_type
    
    pref_services = []
    if pref and pref.service_types:
        pref_services = [normalize_text(s) for s in pref.service_types.split(',')]
        
    job_service_matches = []
    if job_group == 'translation':
        job_service_matches.append(normalize_text('Dịch thuật'))
    else:
        if job_type in ['conference', 'meeting', 'escort']:
            job_service_matches.append(normalize_text('Phiên dịch'))
        if job_type in ['meeting']:
            job_service_matches.append(normalize_text('Hội họp'))
        if job_type in ['business']:
            job_service_matches.append(normalize_text('Kinh doanh'))
        if job_type in ['travel']:
            job_service_matches.append(normalize_text('Du lịch'))
        if job_type in ['event']:
            job_service_matches.append(normalize_text('Sự kiện'))
        if not job_service_matches or job_type == 'other_interpretation':
            job_service_matches.append(normalize_text('Khác'))

    if pref_services and any(s in pref_services for s in job_service_matches):
        score += 25
        reasons.append("Khớp loại công việc")
    elif not pref_services:
        score += 25
        
    # 3. Experience (15 points)
    exp_score = 0
    if prof:
        if prof.is_verified:
            exp_score += 5
        if prof.total_jobs and prof.total_jobs >= 5:
            exp_score += 5
        elif prof.total_jobs and prof.total_jobs > 0:
            exp_score += 2
        if prof.rating and prof.rating >= 4.5:
            exp_score += 5
        elif prof.rating and prof.rating >= 4.0:
            exp_score += 3
    
    exp_score = min(exp_score, 15)
    score += exp_score
    if exp_score >= 10:
        reasons.append("Kinh nghiệm phù hợp")
        
    # 4. Location (10 points)
    loc_score = 10
    job_loc_norm = normalize_text(job.event_location)
    
    if job_loc_norm:
        if "online" in job_loc_norm or "tu xa" in job_loc_norm:
            reasons.append("Làm việc từ xa (Online)")
        elif prof and prof.bio and normalize_text(prof.bio):
            bio_norm = normalize_text(prof.bio)
            if "ha noi" in job_loc_norm and "ha noi" not in bio_norm:
                loc_score = 5
            elif "ho chi minh" in job_loc_norm and "ho chi minh" not in bio_norm and "hcm" not in bio_norm:
                loc_score = 5
            else:
                reasons.append("Phù hợp địa điểm")
        else:
            pass # No penalty if lack of info
    score += loc_score

    # 5. Budget (10 points)
    budget_score = 10
    if job.budget_min and prof:
        min_price = min([s.basic_price for s in prof.services if s.basic_price], default=None)
        if min_price and job.budget_min < (min_price * 0.7):
            budget_score = 5
        elif min_price and job.budget_min >= min_price:
            reasons.append("Ngân sách phù hợp")
    score += budget_score

    # Limit score to 100
    score = min(score, 100)

    return score, reasons

def get_recommended_jobs_for_translator(user_id, limit=10):
    from app import translator_accepts_job
    translator = User.query.get(user_id)
    if not translator or translator.role != 'translator' or not translator.is_active:
        return []
        
    open_jobs = Job.query.filter_by(status='open', is_flagged=False).all()
    
    scored_jobs = []
    for job in open_jobs:
        if Proposal.query.filter_by(job_id=job.id, translator_id=user_id).first():
            continue
            
        if not translator_accepts_job(translator, job):
            continue
            
        # check schedule conflict
        if job.event_date:
            conflict = Contract.query.filter_by(
                translator_id=user_id,
                scheduled_date=job.event_date
            ).filter(Contract.status.in_(['escrow_pending', 'in_progress'])).first()
            if conflict:
                continue

        score, reasons = calculate_job_match_score(translator, job)
        if score > 0:
            # check if reasons list contains specific ones to match the prompt's examples precisely
            # The prompt examples: "Khớp ngôn ngữ", "Khớp loại công việc", "Phù hợp thời gian"
            if not conflict and job.event_date:
                reasons.append("Phù hợp thời gian")
            
            scored_jobs.append({
                'job_id': job.id,
                'match_score': score,
                'reasons': reasons,
                'created_at': job.created_at
            })
            
    scored_jobs.sort(key=lambda x: (x['match_score'], x['created_at']), reverse=True)
    
    return [{'job_id': x['job_id'], 'match_score': x['match_score'], 'reasons': x['reasons']} for x in scored_jobs[:limit]]

def calculate_translator_match_score(translator, job):
    # This is symmetric to calculate_job_match_score
    return calculate_job_match_score(translator, job)

def get_recommended_translators_for_job(job_id, limit=10):
    job = Job.query.get(job_id)
    if not job or job.status != 'open':
        return []

    # Get all active translators
    active_translators = User.query.filter_by(role='translator', is_active=True).all()
    
    scored_translators = []
    for translator in active_translators:
        # Check if they already proposed
        if Proposal.query.filter_by(job_id=job.id, translator_id=translator.id).first():
            continue
            
        try:
            score, reasons = calculate_translator_match_score(translator, job)
            if score > 0:
                scored_translators.append({
                    'translator': translator,
                    'score': score,
                    'reasons': reasons
                })
        except Exception as e:
            # Safe matching
            print(f"Matching error for translator {translator.id}: {e}")
            continue
            
    scored_translators.sort(key=lambda x: (x['score'], x['translator'].created_at), reverse=True)
    
    results = []
    for x in scored_translators[:limit]:
        t = x['translator']
        prof = t.profile
        min_price = min([s.basic_price for s in prof.services if s.basic_price], default=None) if prof else None
        
        results.append({
            'translator_id': t.id,
            'profile_id': prof.id if prof else 0,
            'name': t.name,
            'avatar_initial': t.name[0].upper() if t.name else '?',
            'languages': prof.languages if prof else '',
            'title': prof.title if prof else '',
            'rating': prof.rating if prof else 0.0,
            'total_reviews': prof.total_reviews if prof else 0,
            'is_verified': prof.is_verified if prof else False,
            'min_price': min_price,
            'match_score': x['score'],
            'reasons': x['reasons']
        })
        
    return results
