"""
Disease information database: treatment, symptoms, prevention.
Covers all 38 PlantVillage classes.
"""

DISEASE_INFO = {
    # ── APPLE ─────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "common_name": "Apple Scab",
        "cause": "Fungus (Venturia inaequalis)",
        "symptoms": "Olive-brown or black scabby lesions on leaves and fruit surface.",
        "treatment": [
            "Apply fungicides (captan, mancozeb) at bud break",
            "Remove and destroy infected leaves and fruit",
            "Prune to improve air circulation",
        ],
        "prevention": [
            "Plant resistant apple varieties",
            "Rake and compost fallen leaves",
            "Apply dormant-season copper sprays",
        ],
    },
    "Apple___Black_rot": {
        "common_name": "Apple Black Rot",
        "cause": "Fungus (Botryosphaeria obtusa)",
        "symptoms": "Brown circular leaf spots, rotting fruit with black concentric rings.",
        "treatment": [
            "Remove mummified fruit from the tree",
            "Prune dead or diseased wood",
            "Apply fungicide (thiophanate-methyl)",
        ],
        "prevention": [
            "Keep orchard clean of debris",
            "Avoid wounding trees during pruning",
        ],
    },
    "Apple___Cedar_apple_rust": {
        "common_name": "Cedar Apple Rust",
        "cause": "Fungus (Gymnosporangium juniperi-virginianae)",
        "symptoms": "Bright orange-yellow spots on upper leaf surface in spring.",
        "treatment": [
            "Apply myclobutanil or propiconazole fungicide",
            "Remove nearby cedars/junipers if possible",
        ],
        "prevention": [
            "Plant rust-resistant apple varieties",
            "Avoid planting apple near eastern red cedar",
        ],
    },
    "Apple___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected. Plant appears healthy.",
        "treatment": [],
        "prevention": ["Continue regular monitoring", "Maintain proper irrigation and fertilization"],
    },

    # ── BLUEBERRY ─────────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Maintain soil pH 4.5–5.5", "Mulch to retain moisture"],
    },

    # ── CHERRY ────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "common_name": "Cherry Powdery Mildew",
        "cause": "Fungus (Podosphaera clandestina)",
        "symptoms": "White powdery coating on leaves and young shoots.",
        "treatment": [
            "Apply sulfur-based or potassium bicarbonate fungicide",
            "Remove heavily infected shoots",
        ],
        "prevention": ["Ensure good air circulation", "Avoid excess nitrogen fertilization"],
    },
    "Cherry_(including_sour)___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Regular pruning for airflow", "Monitor during humid periods"],
    },

    # ── CORN (MAIZE) ───────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "common_name": "Gray Leaf Spot",
        "cause": "Fungus (Cercospora zeae-maydis)",
        "symptoms": "Long rectangular gray-tan lesions running parallel to leaf veins.",
        "treatment": [
            "Apply strobilurin or triazole fungicides",
            "Rotate crops with non-host plants",
        ],
        "prevention": ["Use resistant hybrids", "Incorporate crop residue into soil"],
    },
    "Corn_(maize)___Common_rust_": {
        "common_name": "Common Corn Rust",
        "cause": "Fungus (Puccinia sorghi)",
        "symptoms": "Cinnamon-brown pustules scattered across both leaf surfaces.",
        "treatment": ["Apply triazole fungicide (propiconazole)", "Early application is critical"],
        "prevention": ["Plant rust-resistant corn varieties", "Early planting to avoid peak spore season"],
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "common_name": "Northern Leaf Blight",
        "cause": "Fungus (Exserohilum turcicum)",
        "symptoms": "Long cigar-shaped gray-green lesions on leaves.",
        "treatment": [
            "Apply fungicide (mancozeb, azoxystrobin) at tasseling",
            "Remove heavily infected plant debris",
        ],
        "prevention": ["Use resistant hybrids", "Crop rotation", "Tillage to bury residue"],
    },
    "Corn_(maize)___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Proper spacing for airflow", "Balanced fertilization"],
    },

    # ── GRAPE ─────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "common_name": "Grape Black Rot",
        "cause": "Fungus (Guignardia bidwellii)",
        "symptoms": "Brown circular lesions on leaves; fruit shrivels into mummified 'raisins'.",
        "treatment": [
            "Apply myclobutanil or mancozeb fungicide",
            "Remove mummified berries and infected canes",
        ],
        "prevention": ["Prune for open canopy", "Avoid wetting foliage during irrigation"],
    },
    "Grape___Esca_(Black_Measles)": {
        "common_name": "Esca / Black Measles",
        "cause": "Fungal complex (Phaeomoniella, Phaeoacremonium, Fomitiporia)",
        "symptoms": "Tiger-stripe discolorations on leaves; wood shows brown streaking.",
        "treatment": [
            "No cure available; prune infected wood immediately",
            "Protect pruning wounds with fungicide paste",
        ],
        "prevention": ["Prune during dry weather", "Disinfect pruning tools between cuts"],
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "common_name": "Grape Leaf Blight",
        "cause": "Fungus (Pseudocercospora vitis)",
        "symptoms": "Dark brown irregular spots on older leaves causing early defoliation.",
        "treatment": ["Apply copper-based fungicide", "Remove and destroy affected leaves"],
        "prevention": ["Good canopy management", "Avoid overhead irrigation"],
    },
    "Grape___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Regular scouting", "Maintain open canopy for airflow"],
    },

    # ── ORANGE ────────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "common_name": "Citrus Greening (HLB)",
        "cause": "Bacterium (Candidatus Liberibacter asiaticus) spread by psyllid",
        "symptoms": "Asymmetric yellowing (blotchy mottle) of leaves; misshapen bitter fruit.",
        "treatment": [
            "No cure; remove and destroy infected trees",
            "Control Asian citrus psyllid vector with insecticides",
        ],
        "prevention": [
            "Use certified disease-free planting material",
            "Monitor and control psyllid populations",
            "Quarantine new plant material",
        ],
    },

    # ── PEACH ─────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "common_name": "Peach Bacterial Spot",
        "cause": "Bacterium (Xanthomonas arboricola pv. pruni)",
        "symptoms": "Water-soaked angular leaf spots turning brown; fruit pitting and cracking.",
        "treatment": [
            "Apply copper hydroxide bactericide",
            "Remove infected plant material",
        ],
        "prevention": ["Plant resistant varieties", "Avoid overhead irrigation", "Windbreaks to reduce spread"],
    },
    "Peach___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Annual dormant copper spray", "Proper thinning to improve airflow"],
    },

    # ── PEPPER ────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "common_name": "Pepper Bacterial Spot",
        "cause": "Bacterium (Xanthomonas campestris pv. vesicatoria)",
        "symptoms": "Small water-soaked lesions that turn dark brown with yellow halos.",
        "treatment": [
            "Apply copper-based bactericide + mancozeb",
            "Remove and destroy heavily infected plants",
        ],
        "prevention": ["Use certified disease-free seed", "Avoid overhead irrigation", "Crop rotation"],
    },
    "Pepper,_bell___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Regular monitoring", "Avoid plant stress"],
    },

    # ── POTATO ────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "common_name": "Potato Early Blight",
        "cause": "Fungus (Alternaria solani)",
        "symptoms": "Dark brown spots with concentric rings (target-board pattern) on older leaves.",
        "treatment": [
            "Apply chlorothalonil or mancozeb fungicide",
            "Remove lower infected leaves",
        ],
        "prevention": ["Crop rotation", "Avoid over-irrigation", "Use certified seed potatoes"],
    },
    "Potato___Late_blight": {
        "common_name": "Potato Late Blight",
        "cause": "Oomycete (Phytophthora infestans) — caused the Irish Famine",
        "symptoms": "Large irregular water-soaked lesions turning brown-black; white mold on undersides.",
        "treatment": [
            "Apply metalaxyl or cymoxanil + mancozeb immediately",
            "Destroy infected haulms before harvest",
        ],
        "prevention": [
            "Use resistant varieties",
            "Avoid excess nitrogen",
            "Ensure good drainage",
            "Monitor weather (cool, wet conditions favour outbreak)",
        ],
    },
    "Potato___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Certified seed", "Adequate hilling", "Balanced fertilization"],
    },

    # ── RASPBERRY ─────────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Annual pruning of old canes", "Mulching to reduce splash spread"],
    },

    # ── SOYBEAN ───────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Crop rotation", "Use certified seed"],
    },

    # ── SQUASH ────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "common_name": "Squash Powdery Mildew",
        "cause": "Fungus (Erysiphe cichoracearum / Podosphaera xanthii)",
        "symptoms": "White powdery patches on upper leaf surface; leaves yellow and die early.",
        "treatment": [
            "Apply potassium bicarbonate or sulfur fungicide",
            "Neem oil as organic option",
        ],
        "prevention": ["Plant resistant varieties", "Avoid dense plantings", "Reduce humidity"],
    },

    # ── STRAWBERRY ────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "common_name": "Strawberry Leaf Scorch",
        "cause": "Fungus (Diplocarpon earlianum)",
        "symptoms": "Small dark purple spots that merge; leaf edges appear scorched.",
        "treatment": [
            "Apply captan or myclobutanil fungicide",
            "Remove and destroy infected leaves",
        ],
        "prevention": ["Renovate planting after harvest", "Avoid overhead watering", "Crop rotation"],
    },
    "Strawberry___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected.",
        "treatment": [],
        "prevention": ["Annual renovation", "Proper spacing"],
    },

    # ── TOMATO ────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "common_name": "Tomato Bacterial Spot",
        "cause": "Bacterium (Xanthomonas vesicatoria)",
        "symptoms": "Small water-soaked leaf spots with yellow halos; raised corky spots on fruit.",
        "treatment": [
            "Apply copper bactericide + mancozeb",
            "Remove and discard infected plants",
        ],
        "prevention": ["Use disease-free transplants", "Avoid working in wet fields", "Crop rotation"],
    },
    "Tomato___Early_blight": {
        "common_name": "Tomato Early Blight",
        "cause": "Fungus (Alternaria solani)",
        "symptoms": "Dark brown spots with concentric rings on older lower leaves.",
        "treatment": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin",
            "Remove lower infected foliage",
        ],
        "prevention": ["Mulch to reduce soil splash", "Stake plants for airflow", "Crop rotation"],
    },
    "Tomato___Late_blight": {
        "common_name": "Tomato Late Blight",
        "cause": "Oomycete (Phytophthora infestans)",
        "symptoms": "Large greasy gray-green patches; white fungal growth on undersides.",
        "treatment": [
            "Apply metalaxyl or chlorothalonil immediately",
            "Destroy infected plants completely",
        ],
        "prevention": [
            "Plant resistant varieties",
            "Avoid overhead irrigation",
            "Scout weekly during cool wet weather",
        ],
    },
    "Tomato___Leaf_Mold": {
        "common_name": "Tomato Leaf Mold",
        "cause": "Fungus (Passalora fulva)",
        "symptoms": "Pale greenish-yellow spots on upper leaf surface; olive-green mold below.",
        "treatment": [
            "Apply copper-based or chlorothalonil fungicide",
            "Reduce humidity in greenhouse",
        ],
        "prevention": ["Good ventilation", "Avoid leaf wetness", "Plant resistant varieties"],
    },
    "Tomato___Septoria_leaf_spot": {
        "common_name": "Septoria Leaf Spot",
        "cause": "Fungus (Septoria lycopersici)",
        "symptoms": "Numerous small circular spots with dark borders and gray centers on leaves.",
        "treatment": [
            "Apply chlorothalonil, mancozeb, or copper fungicide",
            "Remove infected lower leaves",
        ],
        "prevention": ["Mulch to prevent soil splash", "Avoid wetting foliage", "Crop rotation"],
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "common_name": "Spider Mite Damage",
        "cause": "Pest (Tetranychus urticae)",
        "symptoms": "Stippled, bronzed leaves; fine webbing on leaf undersides.",
        "treatment": [
            "Apply miticide (abamectin, bifenazate)",
            "Spray with insecticidal soap or neem oil",
            "Introduce predatory mites (Phytoseiulus persimilis)",
        ],
        "prevention": [
            "Maintain adequate soil moisture (stressed plants more susceptible)",
            "Avoid dusty conditions",
            "Monitor undersides of leaves regularly",
        ],
    },
    "Tomato___Target_Spot": {
        "common_name": "Target Spot",
        "cause": "Fungus (Corynespora cassiicola)",
        "symptoms": "Brown spots with concentric rings and yellow halos on leaves and stems.",
        "treatment": [
            "Apply azoxystrobin or chlorothalonil fungicide",
            "Remove infected leaves promptly",
        ],
        "prevention": ["Proper plant spacing", "Avoid leaf wetness", "Crop rotation"],
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "cause": "Virus transmitted by whitefly (Bemisia tabaci)",
        "symptoms": "Upward leaf curling, yellowing of leaf margins, stunted plant growth.",
        "treatment": [
            "No cure; remove and destroy infected plants",
            "Control whitefly population with insecticides (imidacloprid, thiamethoxam)",
        ],
        "prevention": [
            "Use TYLCV-resistant varieties",
            "Install insect-proof nets in greenhouses",
            "Apply reflective mulch to deter whiteflies",
        ],
    },
    "Tomato___Tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "cause": "Virus (Tomato mosaic virus) — contact transmission",
        "symptoms": "Mottled light and dark green mosaic pattern on leaves; distorted fruit.",
        "treatment": [
            "No cure; remove infected plants immediately",
            "Disinfect tools with 10% bleach solution",
        ],
        "prevention": [
            "Use virus-free certified seed",
            "Wash hands before handling plants",
            "Control aphid vectors",
        ],
    },
    "Tomato___healthy": {
        "common_name": "Healthy",
        "cause": "N/A",
        "symptoms": "No disease detected. Plant appears healthy.",
        "treatment": [],
        "prevention": ["Regular scouting", "Proper fertilization", "Crop rotation"],
    },
}


def get_disease_info(class_name: str) -> dict:
    """Return disease info dict for a given class name. Falls back gracefully."""
    info = DISEASE_INFO.get(class_name)
    if info:
        return info
    # Try partial match
    for key, val in DISEASE_INFO.items():
        if class_name.lower() in key.lower():
            return val
    return {
        "common_name": class_name.replace("_", " "),
        "cause": "Unknown",
        "symptoms": "Information not available.",
        "treatment": ["Consult a local agricultural extension officer."],
        "prevention": ["Regular monitoring and crop scouting."],
    }


def parse_class_name(class_name: str) -> tuple[str, str]:
    """Extract plant and disease from class name string."""
    parts = class_name.split("___")
    plant = parts[0].replace("_", " ") if parts else class_name
    disease = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
    return plant, disease
