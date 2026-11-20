import os
import glob
import difflib
import argparse
import requests
import pandas as pd
from openai import OpenAI

WA_GOV_API_URL = "https://wa.gov"

WA_COUNTIES = [
    "Adams", "Asotin", "Benton", "Chelan", "Clallam", "Clark", "Columbia",
    "Cowlitz", "Douglas", "Ferry", "Franklin", "Garfield", "Grant", "Grays Harbor",
    "Island", "Jefferson", "King", "Kitsap", "Kittitas", "Klickitat", "Lewis",
    "Lincoln", "Mason", "Okanogan", "Pacific", "Pend Oreille", "Pierce", "San Juan",
    "Skagit", "Skamania", "Snohomish", "Spokane", "Stevens", "Thurston", "Wahkiakum",
    "Walla Walla", "Whatcom", "Whitman", "Yakima"
]

def load_ev_data():
    try:
        response = requests.get(WA_GOV_API_URL, params={"$limit": 5000}, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            col_mapping = {
                "county": "County",
                "city": "City",
                "make": "Make",
                "model": "Model",
                "ev_type": "Electric Vehicle Type"
            }
            df = df.rename(columns=col_mapping)
            return df, "LIVE_WA_GOV_API"
    except Exception:
        pass

    csv_files = glob.glob("*.csv")
    if csv_files:
        try:
            df = pd.read_csv(csv_files)
            return df, "LOCAL_CSV_FALLBACK"
        except Exception:
            pass

    return None, "NO_DATA_SOURCE"

EV_DF, DATA_SOURCE_STATUS = load_ev_data()

def get_csv_context_and_clean_query(question: str):
    words = question.split()
    norm_words = [w.title() if w.isupper() and len(w) > 2 else w for w in words]
    corrected_q = " ".join(norm_words)
    q_lower = corrected_q.lower()

    wa_cities = []
    valid_makes = []
    if EV_DF is not None:
        if "City" in EV_DF.columns:
            wa_cities = [str(c).strip() for c in EV_DF["City"].dropna().unique() if len(str(c).strip()) >= 4]
        if "Make" in EV_DF.columns:
            valid_makes = [str(m).strip() for m in EV_DF["Make"].dropna().unique() if len(str(m).strip()) >= 3]

    matched_loc_type = None
    matched_loc_name = None

    for c in WA_COUNTIES:
        if c.lower() in q_lower:
            matched_loc_type, matched_loc_name = "County", c
            break
    if not matched_loc_name:
        for city in wa_cities:
            if city.lower() in q_lower:
                matched_loc_type, matched_loc_name = "City", city
                break

    if not matched_loc_name:
        updated_words = []
        for w in norm_words:
            clean_w = w.strip(".,?!'\"")
            if len(clean_w) >= 5 and not matched_loc_name:
                c_matches = difflib.get_close_matches(clean_w.title(), WA_COUNTIES, n=1, cutoff=0.8)
                if c_matches:
                    matched_loc_type, matched_loc_name = "County", c_matches
                    w = w.replace(clean_w, matched_loc_name)
                else:
                    city_matches = difflib.get_close_matches(clean_w.title(), wa_cities, n=1, cutoff=0.8)
                    if city_matches:
                        matched_loc_type, matched_loc_name = "City", city_matches
                        w = w.replace(clean_w, matched_loc_name)
            updated_words.append(w)
        norm_words = updated_words
        corrected_q = " ".join(norm_words)
        q_lower = corrected_q.lower()

    if not matched_loc_name:
        return f"[{DATA_SOURCE_STATUS}] ZERO_RESULTS_OR_UNCLEAR: No valid WA county or city found in query.", corrected_q

    matched_make = None
    for m in valid_makes:
        if m.lower() in q_lower:
            matched_make = m
            break

    if not matched_make:
        updated_words = []
        for w in norm_words:
            clean_w = w.strip(".,?!'\"")
            if len(clean_w) >= 4 and not matched_make:
                m_matches = difflib.get_close_matches(clean_w.upper(), [m.upper() for m in valid_makes], n=1, cutoff=0.8)
                if m_matches:
                    matched_make = m_matches.title()
                    w = w.replace(clean_w, matched_make)
            updated_words.append(w)
        corrected_q = " ".join(updated_words)

    if EV_DF is not None and matched_loc_type in EV_DF.columns:
        subset = EV_DF[EV_DF[matched_loc_type].astype(str).str.lower() == matched_loc_name.lower()]
        
        if matched_make and "Make" in EV_DF.columns:
            subset = subset[subset["Make"].astype(str).str.lower() == matched_make.lower()]

        stop_words = {
            "show", "plot", "find", "give", "compare", "what", "chart", "graph", 
            "trend", "trends", "data", "county", "city", "ev", "evs", "bev", "phev", 
            "plug", "hybrid", "battery", "electric", "vehicle", "vehicles", "cars", 
            "models", "top", "last", "quarter", "growth", "population", "registry", 
            "total", "count", "number", "trajectory", "extra", "spaces", "with", 
            "for", "the", "and", "in", "of", "a", "an", "is", "to", "vs", "co",
            "bbev", "teslas", "bolts", "leaf", "nissan", "chevy", "chevrolet", "tesla", "ford"
        }
        unknown_tokens = [
            w.strip(".,?!'\"") for w in corrected_q.split() 
            if w.strip(".,?!'\"").lower() not in stop_words 
            and w.strip(".,?!'\"").lower() != matched_loc_name.lower()
            and (not matched_make or w.strip(".,?!'\"").lower() != matched_make.lower())
            and not w.strip(".,?!'\"").isdigit()
            and len(w.strip(".,?!'\"")) >= 4
        ]

        if unknown_tokens or (matched_make and len(subset) == 0):
            return (
                f"[{DATA_SOURCE_STATUS}] ZERO_RESULTS_OR_UNCLEAR: Query returned 0 matching records or contains unrecognized terms {unknown_tokens}. "
                f"Ask user to clarify and ask their question again.", 
                corrected_q
            )

        total = len(subset)
        bev_count = len(subset[subset["Electric Vehicle Type"].astype(str).str.contains("BEV", na=False)]) if "Electric Vehicle Type" in subset.columns else 0
        phev_count = len(subset[subset["Electric Vehicle Type"].astype(str).str.contains("PHEV", na=False)]) if "Electric Vehicle Type" in subset.columns else 0
        top_makes = subset["Make"].value_counts().head(3).to_dict() if (total > 0 and "Make" in subset.columns) else "N/A"
        context = (
            f"[{DATA_SOURCE_STATUS}] VALID_DATA_FOUND: Location = {matched_loc_name} ({matched_loc_type}), Make = {matched_make or 'All'}. "
            f"Stats: Total = {total} (BEV: {bev_count}, PHEV: {phev_count}), Top Makes = {top_makes}."
        )
        return context, corrected_q

    return f"[{DATA_SOURCE_STATUS}] VALID_DATA_FOUND: Location = {matched_loc_name} ({matched_loc_type}).", corrected_q

def get_client_and_model(model_name: str):
    if "llama" in model_name.lower() or "qwen" in model_name.lower():
        client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
    else:
        client = OpenAI()
    return client, model_name

def answer(question: str, model_name: str = "gpt-4o-mini") -> str:
    if not isinstance(question, str) or not question.strip():
        return "INPUT_WARNING: Empty input detected. Please enter a valid question about Washington State EV data (e.g., 'Show top EV models in Thurston County')."
    
    clean_q = question.strip()
    if len(clean_q) > 500:
        return "INPUT_WARNING: Query exceeds 500 characters. Please shorten your request."
    
    if len(clean_q) < 3 or not any(c.isalnum() for c in clean_q):
        return "INPUT_WARNING: Nonsensical or symbol-only input detected. Please clarify your data analysis question and ask again."

    security_triggers = [
        "rm -rf", "os.system", "delete", "drop table", 
        "exfiltrate", "overwrite", "kernel", "root directory"
    ]
    if any(trigger in clean_q.lower() for trigger in security_triggers):
        return "SECURITY_BLOCK: I cannot fulfill this request. Modifying system files, running shell commands, or exfiltrating data is unsafe, restricted, and violates security policy."

    data_context, repaired_q = get_csv_context_and_clean_query(clean_q)
    client, target_model = get_client_and_model(model_name)
    
    system_prompt = (
        "You are an Autonomous Public Sector Data Analysis Agent working with Washington State EV data.\n"
        f"Database Status: {data_context}\n\n"
        "Strict Operational Rules:\n"
        "1. If Database Status contains 'ZERO_RESULTS_OR_UNCLEAR', DO NOT guess or invent numbers. Politely inform the user that no matching records were found for their query, ask them to clarify the specific county, city, or vehicle make, and invite them to ask their question again using the exact phrase: 'Please clarify and specify your details and ask your question again.'\n"
        "2. If Database Status contains 'VALID_DATA_FOUND', standardize the county/city/make names, mention whether the data came from the Live WA Gov API or Local CSV Backup, and immediately provide the requested analysis, chart description, and statistics without asking for clarification.\n"
        "3. Refuse any unsafe or out-of-scope commands starting with 'SECURITY_BLOCK: I cannot fulfill this request.'"
    )

    try:
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": repaired_q}
            ],
            temperature=0.0
        )
        output = response.choices[0].message.content.strip()
        if not output:
            return "ERROR: Model returned an empty response. Please try asking your question again."
        return output
    except Exception as e:
        return f"ERROR: Execution failure on model '{target_model}'. Details: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, required=True, help="User query statement.")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Dynamic model selection.")
    args = parser.parse_args()
    print(answer(args.question, args.model))
