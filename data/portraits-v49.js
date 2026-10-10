/* V4.9 — Indexed filenames: untested new CDN image URLs; use Media Check for real loads. */
window.SHINO_PORTRAITS_V49=[
  {
    "id": "uma-uma-no-mi",
    "portrait_file": "Pierre Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/5/50/Pierre_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/fr/wiki/Pierre",
    "source_confidence": "gallery-listed",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "sara-sara-no-mi-mod-le-axolotl",
    "portrait_file": "Smiley Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/7/77/Smiley_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/wiki/Category:Season_16_Episode_Images",
    "source_confidence": "gallery-listed",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "beri-beri-no-mi",
    "portrait_file": "Very Good Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/3/38/Very_Good_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/fr/wiki/Very_Good",
    "source_confidence": "gallery-listed",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "ato-ato-no-mi",
    "portrait_file": "Giolla Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/5/50/Giolla_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/wiki/Category:Season_17_Episode_Images",
    "source_confidence": "filename-listed",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "ton-ton-no-mi",
    "portrait_file": "Machvise Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/5/5f/Machvise_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/fr/wiki/Machvise",
    "source_confidence": "gallery-title-inferred",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "guru-guru-no-mi",
    "portrait_file": "Buffalo Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/3/37/Buffalo_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/fr/wiki/Liste_des_Personnages_Canon",
    "source_confidence": "filename-listed",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "gocha-gocha-no-mi",
    "portrait_file": "Charlotte Newshi Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/5/5e/Charlotte_Newshi_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/wiki/Category:Low_Quality_Images",
    "source_confidence": "filename-listed-low-quality",
    "portrait_load_status": "à contrôler depuis Media Check"
  },
  {
    "id": "jake-jake-no-mi",
    "portrait_file": "Kelly Funk Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/0/0c/Kelly_Funk_Portrait.png/revision/latest",
    "portrait_kind": "character-portrait",
    "portrait_source": "One Piece Wiki",
    "portrait_evidence": "https://onepiece.fandom.com/wiki/Category:Season_17_Episode_Images",
    "source_confidence": "filename-listed",
    "portrait_load_status": "à contrôler depuis Media Check"
  }
];
if(Array.isArray(window.SHINO_DATA)){const map=new Map(window.SHINO_PORTRAITS_V49.map(p=>[p.id,p]));for(const f of window.SHINO_DATA){const candidate=map.get(f.id);if(candidate && !f.portrait)Object.assign(f,candidate)}}
