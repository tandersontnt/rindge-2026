"""Build src/videodata.json: playable HLS address, duration and (for three meetings) chapter
jump links with short excerpts of this guide's own machine transcript (/workspace/rec/*.txt).
Run once; build.py reads the JSON. Network: fetches Town Hall Streams pages + playlists."""
import json, re, os, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'videos_raw', 'videos.json')
REC = '/workspace/rec'
def curl(u): return subprocess.run(['curl', '-s', '--max-time', '20', u], capture_output=True, text=True).stdout
def ts(s):
    p = [int(x) for x in s.split(':')]; return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]
# chapter labels follow rindge_recordings_report.md (timestamps = minutes:seconds into the video)
CHAPTERS = {
 '2026-09-09': [('0:40', 'Announcements'), ('4:25', 'Energy Commission appointment'), ('6:42', 'Payroll and accounts payable'),
                ('19:37', 'Financial software (BS&A) renewal'), ('20:56', 'Propane bids'), ('30:41', 'Harvest Fair event permit'),
                ('33:35', 'Ambulance service contracts'), ('58:08', 'Motion on the Peterborough ambulance contract'), ('64:33', 'Meetinghouse horse sheds')],
 '2026-09-23': [('0:00', 'Announcements'), ('4:39', 'Payroll and accounts payable'), ('6:05', 'Approval of minutes'),
                ('11:57', 'When the ambulance contract arrives'), ('14:40', 'Ward Trust and the horse sheds roof')],
 '2026-10-07': [('0:45', 'Announcements'), ('2:41', 'CIP Committee appointment'), ('7:15', 'Payroll and accounts payable'), ('9:38', 'Approval of minutes'),
                ('10:17', 'Livestream: ending Town Hall Streams'), ('16:48', 'Police Chief job description'), ('33:41', 'Executive Secretary position'),
                ('43:08', 'Craft fair event permit'), ('46:02', 'ZBA Case 2026-12: rehearing request'), ('57:24', 'Emergency operations plan grant'),
                ('67:00', 'Fire Chief on the ambulance contract'), ('71:21', 'Historical Society gravestone repair'), ('73:12', 'Public comment')],
}
def transcript(date):
    f = [x for x in os.listdir(REC) if x.startswith(date) and x.endswith('.txt')]
    if not f: return []
    out = []
    for line in open(os.path.join(REC, f[0])):
        m = re.match(r'\[(\d+:\d\d(?::\d\d)?)\]\s*(.*)', line.strip())
        if m and m.group(2).strip(): out.append((ts(m.group(1)), m.group(2).strip()))
    return out
def excerpt(lines, t0, t1):
    seg = [x for t, x in lines if t0 <= t < min(t1, t0 + 45)]
    s = ' '.join(seg)
    if len(s) > 320: s = s[:320].rsplit(' ', 1)[0] + '…'
    return s
def duration(hls):
    top = curl(hls)
    m = re.search(r'^(?!#)(\S+\.m3u8)', top, re.M)
    if not m: return None
    chunk = curl(hls.rsplit('/', 1)[0] + '/' + m.group(1))
    return round(sum(float(x) for x in re.findall(r'#EXTINF:([\d.]+)', chunk))) or None
def main():
  pass
raw = None
if __name__ == "__main__":
 raw = json.load(open(RAW))
 out = {}
 for k, v in raw.items():
     if not v.get('hls'): continue
     date = re.search(r'rindge_nh/(\d{4}-\d\d-\d\d)_', v['hls']).group(1)
     e = dict(hls=v['hls'], date=date, dur=duration(v['hls']))
     if date in CHAPTERS:
         lines = transcript(date); ch = CHAPTERS[date]
         e['chapters'] = []
         for i, (t, label) in enumerate(ch):
             t0 = ts(t); t1 = ts(ch[i + 1][0]) if i + 1 < len(ch) else 10 ** 6
             e['chapters'].append(dict(t=t0, label=label, text=excerpt(lines, t0, t1)))
     out[v['src'] if 'src' in v else k] = e
     print(k, date, e['dur'], len(e.get('chapters', [])))
 json.dump(out, open(os.path.join(HERE, 'videodata.json'), 'w'), indent=1)
