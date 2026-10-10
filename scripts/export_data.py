from pathlib import Path
import json
base=Path(__file__).resolve().parent.parent
records=json.loads((base/'data'/'fruits.json').read_text(encoding='utf8'))
(base/'data'/'fruits.js').write_text('/* Generated file from fruits.json. */\nwindow.SHINO_DATA = '+json.dumps(records,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
print(f'Exported {len(records)} entries')
