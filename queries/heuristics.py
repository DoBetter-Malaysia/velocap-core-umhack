from datetime import datetime

# Did not do SQL sanitization due to time constraint

def founded_at(start_date, end_date):
    if not start_date and not end_date:
        return ""
    average_date = None
    if not start_date:
        start_date = '1900-01-01'
        average_date = end_date
    else:
        start_date = str(start_date) + '-01-01'
    if not end_date:
        end_date = '2100-12-30'
        average_date = start_date
    else:
        end_date = str(end_date) + '-12-30'

    if not average_date:
        d1 = datetime.strptime(start_date,"%Y-%m-%d")
        d2 = datetime.strptime(end_date,"%Y-%m-%d")
        average_date = d1.date() + (d2-d1) / 2

    return f"""(CASE WHEN s.founded_at >= '{start_date}' 
             OR S.founded_at <= '{end_date}' 
         THEN 0 ELSE ABS(DATE_PART('year', s.founded_at) - DATE_PART('year', '{average_date}'::date)) END) """

def engagement_date(date):
    if not date:
        return ""
    return f"""(CASE WHEN s.last_engagement_at >= '{date}' 
         THEN 0 ELSE ABS((DATE_PART('year', s.founded_at) - DATE_PART('year', '{date}'::date)) * 12 + (DATE_PART('month', s.founded_at) - DATE_PART('month', '{date}'::date)) ) END) """

def num_founders(num):
    if not num:
        return ""
    return f"""    (SELECT ABS(COUNT(*) - {num})
        FROM founders f
        WHERE f.company_id = s.id) """

def funding_total(fund):
    if not fund:
        return ""
    # every 50,000 will be counted as 1
    return f"""    (ABS(s.funding_total_usd - {fund}) / 50000) """

def yoe(year):
    if year is None or year == "":
        return ""
    
    return f"""    (SELECT ABS(AVG(years_of_experience) - {year})
         FROM founders f 
        WHERE f.company_id = s.id) """

def gender(g):
    if not g:
        return ""
    if g == 'female':
        g = 'f'
    else:
        g = 'm'
    return f"""    -(SELECT COUNT(*)
        FROM founders f
        where f.company_id = s.id
            AND f.gender = '{g}') +
    (SELECT COUNT(*)
        FROM founders f
        where f.company_id = s.id
            AND f.gender != '{g}') """

def search(q):
    if not q:
        return ""
    ls = []
    for v in q.split(" "):
        ls.append(f"description ILIKE '%{v}%'")
        ls.append(f"name ILIKE '%{v}%'")
        ls.append(f"category_list ILIKE '%{v}%'")

    return " OR ".join(ls)

def prev_startup(n):
    if n is None or n == "":
        return ""
    return f"""    (SELECT ABS(AVG(f.prev_founded) - {n})
         FROM founders f 
        WHERE f.company_id = s.id)  """

def query(json):
    data = json
    res = []
    res.append(founded_at(data.get("companyFoundedMinYear"), data.get("companyFoundedMaxYear")))
    res.append(num_founders(data.get("numberOfFounders")))
    res.append(engagement_date(data.get("lastEngagement")))
    res.append(funding_total(data.get("fundingTotal")))
    res.append(yoe(data.get("founderYearsOfExperience")))
    res.append(gender(data.get("founderGender")))
    res.append(prev_startup(data.get("noOfPreviousStartups")))

    res = list(filter(lambda x: x, res))
    if len(res) == 0:
        return "SELECT * FROM startups"
    
    sterm = search(data.get("searchQuery"))
    finding = ""
    if sterm:
        finding = f" WHERE {sterm}"

    return f"""SELECT *,
        {'+'.join(res)}
        AS score
FROM startups s
{finding}
ORDER BY score ASC"""
    