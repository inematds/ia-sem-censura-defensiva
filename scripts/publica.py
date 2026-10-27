"""Publica o vídeo "IA sem censura, do jeito certo" (explicavideos v2) em inematds/ia-sem-censura-defensiva.
Release video-v1.0.0 (MP4 16:9 + SRT, e MP4 9:16 se existir) + Pages: videos/index.html com o player, capítulos e legendas VTT.
Uso: python3 scripts/publica.py   (idempotente: sobe só o que mudou; commit só se houver diff).
Entradas (fora do repo, na pasta de produção ~/projetos/output/explica-*/v2/ que tiver o MP4 final; ou IA_SEM_CENSURA_OUT=<pasta>):
  final/ia-sem-censura-defensiva-pt.mp4 (+ .srt ao lado)      obrigatório
  verification/assembled-pt.json                        opcional (capítulos e conferência de bytes)
  docs/lesson-pt.json                                   opcional (títulos dos capítulos)
  final/9x16/ia-sem-censura-defensiva-pt-9x16.mp4              opcional (versão vertical)
Não mexe no index.html da raiz (que leva ao guia)."""
import html, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

ID = 'ia-sem-censura-defensiva'


def achar_out():
    if os.environ.get('IA_SEM_CENSURA_OUT'):
        return Path(os.environ['IA_SEM_CENSURA_OUT']).expanduser()
    achados = sorted(Path.home().glob(f'projetos/output/explica-*/v2/final/{ID}-pt.mp4'))
    if len(achados) != 1:
        sys.exit(f'esperava 1 vídeo final em ~/projetos/output/explica-*/v2/final/{ID}-pt.mp4, achei {len(achados)}; '
                 'defina IA_SEM_CENSURA_OUT=<pasta de produção>')
    return achados[0].parents[2]


OUT = achar_out()
REPO = Path(__file__).resolve().parent.parent
GH = f'inematds/{ID}'
TAG = 'video-v1.0.0'
BASE = f'https://github.com/{GH}/releases/download/{TAG}/'
PAGES = f'https://inematds.github.io/{ID}/'
TITLE = 'IA sem censura, do jeito certo: seu próprio modelo para segurança defensiva'
H1 = 'IA sem censura, do <b>jeito certo</b>'
LEAD = ('Um modelo aberto que não recusa perguntas técnicas, ligado ao DeepSeek Harness por API, GPU na RunPod '
        'ou LM Studio local. Como provar texto, função e imagem, treinar num laboratório falso e não deixar a GPU '
        'cobrando à toa — sempre só no que é seu.')
V2 = OUT / 'v2'
FINAL = V2 / 'final'
FULL = FINAL / f'{ID}-pt.mp4'
V916 = FINAL / '9x16' / f'{ID}-pt-9x16.mp4'


def sh(*a, **kw):
    return subprocess.run(a, check=True, text=True, capture_output=True, **kw).stdout


def dur(p):
    return float(sh('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)))


def mmss(d):
    return f'{int(d // 60)}min{int(d % 60):02d}s'


def capitulos():
    rec_p, les_p = V2 / 'verification/assembled-pt.json', V2 / 'docs/lesson-pt.json'
    if not rec_p.exists() or not les_p.exists():
        return []
    rec = json.loads(rec_p.read_text())
    assert Path(rec['file']) == FULL and FULL.stat().st_size == rec['bytes'], 'assembled-pt.json não bate com o MP4 final'
    scenes = json.loads(les_p.read_text())
    return [(int(c['time']), scenes[c['scene'] - 1]['title']) for c in rec['chapters']]


def main():
    if not FULL.exists():
        sys.exit(f'vídeo final não encontrado: {FULL}')
    srt = FULL.with_suffix('.srt')
    if not srt.exists():
        sys.exit(f'legenda não encontrada: {srt}')
    chapters = capitulos()
    tem916 = V916.exists()
    stage = OUT / 'release'; stage.mkdir(exist_ok=True)
    folder = REPO / 'videos'; folder.mkdir(exist_ok=True)
    pares = [(FULL, f'{ID}-16x9.mp4'), (srt, f'{ID}-16x9.srt')] + ([(V916, f'{ID}-9x16.mp4')] if tem916 else [])
    assets = []
    for src, nome in pares:
        dst = stage / nome
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            dst.write_bytes(src.read_bytes())
        assets.append(dst)
    vtt = 'WEBVTT\n\n' + re.sub(r'(\d\d:\d\d:\d\d),(\d{3})', r'\1.\2', srt.read_text())
    (folder / 'pt.vtt').write_text(vtt)
    caps = ''.join(f'<button type="button" data-time="{s}">{s // 60:02d}:{s % 60:02d} · {html.escape(c)}</button>' for s, c in chapters)
    d1 = dur(FULL)
    cards = [
        f'''<section class="card"><h2>Vídeo completo 16:9 <span>{mmss(d1)}</span></h2>
<video controls preload="metadata" playsinline><source src="{BASE}{ID}-16x9.mp4" type="video/mp4"><track default kind="subtitles" src="pt.vtt" srclang="pt" label="Português"></video>
<p><a href="{BASE}{ID}-16x9.mp4">Baixar MP4</a> · <a href="{BASE}{ID}-16x9.srt">Baixar legendas</a></p>
{f'<details><summary>Capítulos</summary>{caps}</details>' if caps else ''}</section>''']
    delivery = {'16x9': {'url': BASE + f'{ID}-16x9.mp4', 'srt': BASE + f'{ID}-16x9.srt', 'duration': round(d1, 2)}}
    if tem916:
        d2 = dur(V916)
        cards.append(f'''<section class="card vert"><h2>Versão vertical 9:16 <span>{mmss(d2)}</span></h2>
<video controls preload="metadata" playsinline><source src="{BASE}{ID}-9x16.mp4" type="video/mp4"></video>
<p><a href="{BASE}{ID}-9x16.mp4">Baixar MP4</a></p></section>''')
        delivery['9x16'] = {'url': BASE + f'{ID}-9x16.mp4', 'duration': round(d2, 2)}
    if subprocess.run(['gh', 'release', 'view', TAG, '--repo', GH], capture_output=True).returncode:
        notes = stage / 'RELEASE.md'
        notes.write_text(f'{TITLE} — vídeo explicativo do kit, com legendas em português.\n\n'
                         f'Assistir: {PAGES}videos/\n\nGuia e kit: {PAGES}guia/')
        sh('gh', 'release', 'create', TAG, '--repo', GH, '--draft', '--title', f'{TITLE} (vídeo)', '--notes-file', str(notes))
    have = {a['name']: a['size'] for a in json.loads(sh('gh', 'release', 'view', TAG, '--repo', GH, '--json', 'assets'))['assets']}
    for f in assets:
        if have.get(f.name) != f.stat().st_size:
            print('upload', f.name, flush=True)
            sh('gh', 'release', 'upload', TAG, str(f), '--repo', GH, '--clobber')
    page = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)} · INEMA.CLUB</title><meta name="description" content="{html.escape(LEAD)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>:root{{color-scheme:dark;--bg:#0c0c10;--card:#15151c;--line:#2a2a35;--tx:#ededf2;--mut:#a3a3b2;--am:#FACC15}}*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--tx);font:17px/1.6 Inter,system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:32px 16px}}
a{{color:var(--am)}}h1{{font:800 clamp(1.9rem,5vw,3rem)/1.12 Sora,sans-serif;margin:.4em 0}}h1 b{{color:var(--am)}}.lead{{color:var(--mut);max-width:760px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:28px 0}}.card h2{{font:700 1.25rem Sora,sans-serif;margin:0 0 8px}}.card h2 span{{color:var(--mut);font:500 .95rem Inter,sans-serif}}
video{{width:100%;aspect-ratio:16/9;background:#000;border-radius:12px}}.vert video{{aspect-ratio:9/16;max-width:420px;display:block;margin:auto}}
summary{{cursor:pointer;color:var(--am);margin-top:8px}}button{{display:block;background:var(--bg);color:var(--tx);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:6px 0;text-align:left;cursor:pointer;width:100%;font:inherit}}
.kit li{{margin:.35em 0}}.etica{{border-left:4px solid #F0918A}}:focus-visible{{outline:3px solid var(--am);outline-offset:3px}}footer{{color:var(--mut);font-size:15px;margin-top:40px}}</style></head>
<body><main><nav><a href="https://inema.club">INEMA.CLUB</a> · <a href="../guia/">Guia</a> · <a href="https://github.com/{GH}">GitHub</a></nav>
<h1>{H1}</h1><p class="lead">{html.escape(LEAD)}</p>
{cards[0]}
<section class="card"><h2>O kit em português</h2><ul class="kit">
<li><a href="https://github.com/{GH}/blob/main/kit/COMECE-AQUI.md">COMECE-AQUI</a> — o caminho mais curto e o que tem no kit</li>
<li><a href="https://github.com/{GH}/tree/main/kit/prompts">prompts</a> — os 9 prompts, cada um com o bloco de fronteiras</li>
<li><a href="https://github.com/{GH}/tree/main/kit/guias">guias</a> — as 3 rotas, ferramentas, segurança do modelo, custo e problemas comuns</li>
<li><a href="https://github.com/{GH}/tree/main/kit/scripts">scripts</a> — checador de endpoint, laboratório, checagem com escopo e guarda ociosa</li>
<li><a href="https://github.com/{GH}/blob/main/kit/verificacao/STATUS.md">STATUS</a> — o que foi testado e o que depende da sua conta</li></ul>
<p>Passo a passo no <a href="../guia/">guia</a>.</p></section>
<section class="card etica"><h2>A regra</h2><p>Só sistemas seus ou com permissão por escrito. Escopo registrado antes, laboratório sintético primeiro, credenciais fora do chat. Na RunPod, pare o Pod e confira EXITED.</p></section>
{''.join(cards[1:])}
<footer>Conteúdo aberto e gratuito do <a href="https://inema.club">INEMA.CLUB</a>. DeepSeek Harness, LM Studio, RunPod e os modelos citados são de seus autores.</footer></main>
<script>document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{{const v=b.closest('.card').querySelector('video');v.currentTime=Number(b.dataset.time);v.play();}}));</script></body></html>
'''
    (folder / 'index.html').write_text(page)
    (folder / 'delivery.json').write_text(json.dumps(delivery, indent=2) + '\n')
    g = lambda *a: sh('git', '-c', 'user.name=inematds', '-c', 'user.email=inematds@gmail.com', *a, cwd=REPO)
    g('add', 'videos')
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO).returncode:
        g('commit', '-m', 'feat: player do vídeo\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>')
        g('push', '-q', 'origin', 'HEAD:main')
    sh('gh', 'release', 'edit', TAG, '--repo', GH, '--draft=false')
    for n in delivery.values():
        with urllib.request.urlopen(urllib.request.Request(n['url'], method='HEAD'), timeout=60) as r:
            assert r.status == 200
    for _ in range(40):
        try:
            with urllib.request.urlopen(PAGES + 'videos/delivery.json?v=' + str(int(time.time())), timeout=30) as f:
                if '16x9' in f.read().decode():
                    break
        except Exception:
            pass
        time.sleep(30)
    else:
        sys.exit('push e release feitos; Pages ainda não respondeu')
    print('OK', PAGES + 'videos/')


if __name__ == '__main__':
    main()
