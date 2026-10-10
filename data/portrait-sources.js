/* V4.7 — filenames verified against published One Piece Wiki portrait categories; third-party images remain remote, not packaged. */
window.SHINO_PORTRAIT_SOURCES = {
  "mori-mori-no-mi": {
    "portrait_file": "Aramaki Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/a/a2/Aramaki_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "kobu-kobu-no-mi": {
    "portrait_file": "Belo Betty Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/9/98/Belo_Betty_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "poke-poke-no-mi": {
    "portrait_file": "Blamenco Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/7/75/Blamenco_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "mushi-mushi-no-mi-mod-le-suzumebachi": {
    "portrait_file": "Bian Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/2/27/Bian_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "iku-iku-no-mi": {
    "portrait_file": "Biblo Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/5/56/Biblo_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "nori-nori-no-mi": {
    "portrait_file": "Bluegrass Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/d/de/Bluegrass_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "doru-doru-no-mi": {
    "portrait_file": "Galdino Mr. 3 Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/a/a6/Galdino_Mr._3_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-wiki"
  },
  "magu-magu-no-mi": {
    "portrait_file": "Sakazuki PW Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/e/e3/Sakazuki_PW_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-jeu"
  },
  "green-blood-mero-mero": {
    "portrait_file": "S-Snake PW Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/d/d6/S-Snake_PW_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-jeu"
  },
  "choki-choki-no-mi": {
    "portrait_file": "Inazuma Impel Down Prisoner Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/d/d9/Inazuma_Impel_Down_Prisoner_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-époque"
  },
  "juku-juku-no-mi": {
    "portrait_file": "Shinobu Oniwabanshu Portrait.png",
    "portrait": "https://static.wikia.nocookie.net/onepiece/images/f/f9/Shinobu_Oniwabanshu_Portrait.png/revision/latest",
    "portrait_source": "One Piece Wiki",
    "portrait_kind": "portrait-époque"
  }
};
if(Array.isArray(window.SHINO_DATA))for(const f of window.SHINO_DATA){const x=window.SHINO_PORTRAIT_SOURCES[f.id];if(x && !f.portrait)Object.assign(f,x)}
