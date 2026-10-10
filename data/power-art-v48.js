/* V4.8 — Power illustrations from indexed gallery filenames. Not depictions of the physical Green Blood fruit (there is none). */
window.SHINO_EXTRA_POWER_ART=[
  {
    "id": "green-blood-supa-supa",
    "file": "Artificial Supa Supa no Mi.png",
    "image": "https://static.wikia.nocookie.net/onepiece/images/6/66/Artificial_Supa_Supa_no_Mi.png/revision/latest",
    "visual": "pouvoir",
    "image_kind": "scène-anime",
    "visual_description": "S-Hawk utilisant la lame artificielle",
    "visual_provenance": "https://onepiece.fandom.com/wiki/Supa_Supa_no_Mi",
    "visual_validation": "source filename indexed, remote image load not tested"
  },
  {
    "id": "green-blood-sui-sui",
    "file": "Sui Sui no Mi Water Depiction.png",
    "image": "https://static.wikia.nocookie.net/onepiece/images/e/ef/Sui_Sui_no_Mi_Water_Depiction.png/revision/latest",
    "visual": "pouvoir",
    "image_kind": "scène-anime",
    "visual_description": "S-Shark utilisant la nage dans la matière",
    "visual_provenance": "https://onepiece.fandom.com/wiki/Category:Season_21_Episode_Images",
    "visual_validation": "source filename indexed, remote image load not tested"
  },
  {
    "id": "green-blood-nikyu-nikyu",
    "file": "S-Bear Uses Ursus Shock.png",
    "image": "https://static.wikia.nocookie.net/onepiece/images/e/e5/S-Bear_Uses_Ursus_Shock.png/revision/latest",
    "visual": "pouvoir",
    "image_kind": "scène-anime",
    "visual_description": "S-Bear utilise Ursus Shock",
    "visual_provenance": "https://onepiece.fandom.com/wiki/Category:Season_21_Episode_Images",
    "visual_validation": "source filename indexed, remote image load not tested"
  },
  {
    "id": "green-blood-mero-mero",
    "file": "S-Snake Petrifies CP0 Agents.png",
    "image": "https://static.wikia.nocookie.net/onepiece/images/5/5e/S-Snake_Petrifies_CP0_Agents.png/revision/latest",
    "visual": "pouvoir",
    "image_kind": "scène-anime",
    "visual_description": "S-Snake pétrifie des agents du CP0",
    "visual_provenance": "https://onepiece.fandom.com/wiki/Category:Season_21_Episode_Images",
    "visual_validation": "source filename indexed, remote image load not tested"
  }
];
if(Array.isArray(window.SHINO_DATA)){const ids=new Map(window.SHINO_EXTRA_POWER_ART.map(x=>[x.id,x]));for(const f of window.SHINO_DATA){const art=ids.get(f.id);if(art&&!f.image)Object.assign(f,art)}}
