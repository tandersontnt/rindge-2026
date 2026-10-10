"""Curated excerpts: each fragment must appear verbatim in /workspace/rec transcript; ' […] ' joins fragments.
Chapters with no clean passage get no excerpt (jump link only)."""
import json, re, os
import make_videodata as MV  # noqa (only for transcript())
EX = {
 ('2026-09-09', 265): ["Okay, now I make a motion that we appoint Amber Dewey to the Energy Commission", "All in favor? Aye"],
 ('2026-09-09', 1177): ["I'll second that motion All in favor 3-0"],
 ('2026-09-09', 1256): ["The lowest of the three was superior propane At 158 a gallon The highest of the three was 199 a gallon So he's recommending you go forward with superior propane at 158 a gallon"],
 ('2026-09-09', 2015): ["Review of the ambulance service contracts", "But I have a short three page note from him to read For the select board"],
 ('2026-09-09', 3488): ["I'm going to make a motion that we go with Peterborough Fire and Rescue for the Ambulance Service. For next year and the year after, it will be a five year contract when we will evaluate after the second year. Each year is for the first two years, it will be $280,217."],
 ('2026-09-09', 3873): ["We're probably going to have to have another meeting house committee.", "Mike is expecting two more quotes."],
 ('2026-09-23', 279): ["All right, let's move on to the approval of payroll for 9.17 and 9.24."],
 ('2026-09-23', 365): ["Approval of the minutes for 826, 2026, 415, 2026, 826, 2026, non-public session minutes, and 9-9, 2026, non-public session minutes."],
 ('2026-09-23', 717): ["When are we going to receive the contract from Peterborough so that I can review it?"],
 ('2026-09-23', 880): ["the ward and trust met yesterday. Yep. And we voted to add another 7,000 to the roof"],
 ('2026-10-07', 45): ["Of course, let's remind people that voting day is Tuesday, November 3rd.", "Let's try and get a 50% turnout.", "The town invites you to trick or treat on Halloween night. Saturday, October 31st from 4pm to 7pm."],
 ('2026-10-07', 161): ["So we need a few people to volunteer for that. I think we have one for the audience tonight."],
 ('2026-10-07', 578): ["I'll make a motion to approve 9-9, 26, 9-23, 26, and 4-22, 26. Seconded by Tom. All in favor? Aye."],
 ('2026-10-07', 617): ["So for the last two years or so, the town we're just using this live streaming company called Town Hall Streams,", "to basically broadcast these so people can come and and watch. You can watch later on. The contract is coming up."],
 ('2026-10-07', 1008): ["Next review of police chief job description. Drafted by town council."],
 ('2026-10-07', 2021): ["This is the official proposal to make the executive secretary role full time of the hours that was previously established."],
 ('2026-10-07', 2588): ["There was an application for a special events permit.", "basically it's a rain date for the women's club"],
 ('2026-10-07', 3444): ["Earlier this year, I put in a grant to the state of New Hampshire for the Emergency Management Performance Grant. We've got a soft offer of $4,500."],
 ('2026-10-07', 4281): ["up to $600 for the repair of", "He was one of our Revolutionary War soldiers, and his gravestone is in three pieces."],
}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videodata.json')
D = json.load(open(p))
for e in D.values():
    if 'chapters' not in e: continue
    full = ' '.join(x for _, x in MV.transcript(e['date']))
    for c in e['chapters']:
        frs = EX.get((e['date'], c['t']))
        if not frs: c['text'] = ''; continue
        for f in frs: assert f in full, (e['date'], c['t'], f)
        c['text'] = ' […] '.join(frs)
json.dump(D, open(p, 'w'), indent=1)
print('ok')
