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

/* Additional user infobox illustrations: these are character images, not fruit appearances. */
const extraPortraits=[{"id":"inu-inu-no-mi-mod-le-dachshund","portrait_file":"Lassoo Anime Infobox.png","portrait":"https://static.wikia.nocookie.net/onepiece/images/e/ea/Lassoo_Anime_Infobox.png/revision/latest","portrait_source":"One Piece Wiki","portrait_kind":"illustration-infobox"},{"id":"inu-inu-no-mi-mod-le-tanuki","portrait_file":"Bunbuku Manga Infobox.png","portrait":"https://static.wikia.nocookie.net/onepiece/images/3/33/Bunbuku_Manga_Infobox.png/revision/latest","portrait_source":"One Piece Wiki","portrait_kind":"illustration-infobox"}];
if(Array.isArray(window.SHINO_DATA))for(const p of extraPortraits){const f=window.SHINO_DATA.find(f=>f.id===p.id);if(f&&!f.portrait)Object.assign(f,p)}
/* Verified Wiki image filenames for visualized powers; not necessarily the physical fruit. */
window.SHINO_POWER_IMAGES=[{"id":"numa-numa-no-mi","file":"Numa Numa no Mi Infobox.png","image":"https://static.wikia.nocookie.net/onepiece/images/d/d3/Numa_Numa_no_Mi_Infobox.png/revision/latest","visual":"pouvoir","image_kind":"pouvoir-illustré"},{"id":"wapu-wapu-no-mi","file":"Wapu Wapu no Mi.gif","image":"https://static.wikia.nocookie.net/onepiece/images/5/5e/Wapu_Wapu_no_Mi.gif/revision/latest","visual":"pouvoir","image_kind":"pouvoir-animé"},{"id":"inu-inu-no-mi-mod-le-loup","file":"Full-Beast Form of Jabra's fruit.png","image":"https://static.wikia.nocookie.net/onepiece/images/e/e1/Full-Beast_Form_of_Jabra%27s_fruit.png/revision/latest","visual":"pouvoir","image_kind":"forme-zoan"}];
if(Array.isArray(window.SHINO_DATA))for(const p of window.SHINO_POWER_IMAGES){const f=window.SHINO_DATA.find(f=>f.id===p.id);if(f&&!f.image)Object.assign(f,p)}
