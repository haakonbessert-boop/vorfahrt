# Erzeugt den ausführlichen Ernährungsplan (Markdown fürs Second Brain) aus data/.
#   python3 plan.py <ziel.md>
import json, math, sys, pathlib
root = pathlib.Path(__file__).parent
R = json.loads((root/"data/rezepte.json").read_text()); Z = json.loads((root/"data/zutaten.json").read_text())
by = {r["id"]: r for r in R["rezepte"]}
def fmt(n): return f"{n:,.0f}".replace(",", ".") if abs(n - round(n)) < 1e-9 else f"{n:.1f}".replace(".", ",")
def unit(k): return " Stk." if Z[k].get("stueck") else (" Bund" if k == "fruehlingszwiebel" else " g")
PL = {"Dose": "Dosen", "Glas": "Gläser", "Schale 250 g": "Schalen à 250 g", "Flasche": "Flaschen", "Netz 2 kg": "Netze à 2 kg"}
def einkauf(rs):
    tot = {}
    for r in rs:
        for e in r["zutaten"]:
            tot[e[0]] = tot.get(e[0], 0) + e[1] * (e[2] if len(e) > 2 else r["portionen"])
    out, vor = {}, []
    for k, m in tot.items():
        z = Z[k]
        if z.get("vorrat"): vor.append(z["name"]); continue
        p = z["packung"]; n = max(1, math.ceil(m / p["menge"] - 0.08)); e = p["einheit"]
        q = f"{n} {PL.get(e, e) if n > 1 else e}"
        need = f" ({fmt(round(m))} g gebraucht)" if p["menge"] >= 50 else ""
        out.setdefault(z["abteilung"], []).append(f"- [ ] {z['name']}: **{q}**{need}")
    return out, sorted(set(vor))
z = R["ziele"]; L = []; A = L.append
A(f"""---
tags: [ernaehrung, mealprep, aufbau, typ/plan]
dauer: 4 Wochen, rotierend
kcal_tag: {z['kcal_min']}-{z['kcal_max']}
protein_tag: {z['protein_tag']}+
app: https://haakonbessert-boop.github.io/vorfahrt/
aktualisiert: 2026-11-27
---

# 4-Wochen-Plan Aufbau: Mittags-Box und schnelles Abendessen

**Prinzip:** Das Grundgerüst ist jeden Tag gleich, das Essen wechselt jede Woche. Innerhalb einer Woche gibt es mittags dieselbe Box und abends dasselbe Abendessen, damit eine Koch-Session pro Woche reicht. Woche 5 fängt wieder bei Woche 1 an.

**Zwei Mahlzeiten, kein Frühstück, kein Snack.** Alle Kalorien und das ganze Protein kommen aus Mittag und Abendessen. Darum sind beide Portionen bewusst groß, mittags die Hauptmahlzeit.

**Ihre Regeln (Stand 27.11.):**
- Hähnchen höchstens jede zweite Woche (Woche 2 und 4, nur mittags). Sonst Schinken, Würstchen, Salami, Ei, Käse.
- Nicht nur Nudeln: 2 Wochen Nudeln, 2 Wochen Kartoffeln.
- Lieblinge: Tortellini-Pfanne (All-Time-Favorite) und Pesto-Pasta-Salat.
- Mag sie nicht: Paprika (als Gemüse, Paprikapulver ist ok), Fisch, Reis, Brot, Bulgur, Brokkoli, Spinat, Erbsen, Curry, Teriyaki, Erdnuss, Shakshuka, Halloumi aus der Pfanne, Magerquark. Gnocchi gerade nicht, Feta nur sparsam.

Die App **Prep Box** zeigt dieselben Daten mit Einkaufsliste zum Abhaken: https://haakonbessert-boop.github.io/vorfahrt/

## Wochenrhythmus

- **Samstag:** Einkauf für die ganze Woche (Mo–Fr).
- **Sonntag:** einmal kochen, 5 Mittags-Boxen für Mo–Fr (ca. 35–50 min).
- **Montag bis Freitag:** mittags die Box kalt aus dem Kühlschrank, abends das Abendessen der Woche frisch in max. 15–20 min, alles unter einer halben Stunde (Pfanne oder Ofen, keine Mikrowelle).
- **Wochenende:** nicht Teil des Plans.

**Kein Tiefkühler.** Darum gilt:
- Am Sonntag gebratenes Hähnchen hält im Kühlschrank bis Donnerstag (Tag 4), das ist die Obergrenze. Die **Freitags-Box** bekommt gegarte Hähnchenstreifen aus der Vakuumpackung, erst Freitagmorgen öffnen.
- Schinken und Würstchen bleiben bis zum Morgen in der Packung und kommen erst dann in die Box.
- Rohes Fleisch hält ohne Tiefkühler nur 1–2 Tage. Die Abendessen nutzen darum nur Zutaten, die ungeöffnet bis Freitag halten: Kochschinken, Salami, gegarte Hähnchenstreifen, Käse, Eier, Kühlregal-Teig und -Teigwaren, Dosen.

## Der Tag (Mo–Fr)
""")
A("| Woche | Mittag (Box) | Abendessen | Summe |"); A("|---|---|---|---|")
for w in R["rotation"]:
    a, b = by[w["salat"]]["makros"], by[w["abend"]]["makros"]
    A(f"| {w['woche']} | {fmt(a['kcal'])} kcal, {a['protein']} g P | {fmt(b['kcal'])} kcal, {b['protein']} g P | **{fmt(a['kcal'] + b['kcal'])} kcal, {a['protein'] + b['protein']} g P** |")
A(f"""
Ziel: {fmt(z['kcal_min'])}–{fmt(z['kcal_max'])} kcal und mindestens {z['protein_tag']} g Protein pro Tag (Annahme, ihr Gewicht ist nicht bekannt). Gerechnet mit Standard-Nährwerten, ihre Tracking-App weicht je nach Marke etwas ab. Öl zum Braten und für Dressings ist eingerechnet.

## Die Rotation

| Woche | Mittag (kalt, Box) | Abendessen (Pfanne/Ofen) |
|---|---|---|""")
for w in R["rotation"]:
    A(f"| {w['woche']} | {by[w['salat']]['name']} | {by[w['abend']]['name']} |")
A("""
## So bleiben die Boxen gut

- Nudeln bissfest kochen und kalt abspülen, sonst werden sie bis Freitag matschig.
- Nudeln, Kartoffeln und Hähnchen nach dem Kochen flach ausbreiten, abkühlen lassen und innerhalb von 2 Stunden in den Kühlschrank.
- Knuspriges (Speck) und Dressings in ein Extra-Döschen, erst beim Essen dazu.
- Boxen hinten in den Kühlschrank, nicht in die Tür. Die Boxen sind groß: 1,5-Liter-Box nehmen.

---
""")
for w in R["rotation"]:
    s, a = by[w["salat"]], by[w["abend"]]
    A(f"## Woche {w['woche']}: {s['kurz']} + {a['kurz']}\n")
    for lab, r in [("Mittag", s), ("Abend", a)]:
        A(f"### {lab}: {r['name']} ({r['portionen']} Portionen)"); A("Pro Portion:")
        for e in r["zutaten"]:
            k, m = e[0], e[1]
            if not m: continue
            l = f"- {fmt(m)}{unit(k)} {Z[k]['name']}"
            if len(e) > 2 and e[2] < r["portionen"]: l += f" (nur {e[2]} von {r['portionen']} Portionen)"
            A(l)
        m = r["makros"]; A(f"- **ca. {fmt(m['kcal'])} kcal, {m['protein']} g Protein, {m['fett']} g Fett**\n"); A(f"{r['hinweis']}\n")
    A(f"### Meal Prep Sonntag (ca. {w['prep_minuten']} min)")
    for i, p in enumerate(w["prep"], 1): A(f"{i}. {p}")
    A(f"\n### Abends (Mo–Fr)\nJeden Abend 1 Portion {a['name']} frisch, wie oben beschrieben.\n")
    out, vor = einkauf([s, a]); A("### Einkauf Samstag")
    for abt in ["Obst & Gemüse", "Kühltheke", "Konserven & Trocken"]:
        if abt in out: A(f"**{abt}**"); L.extend(out[abt]); A("")
    A(f"Aus dem Vorrat: {', '.join(vor)}.\n\n---\n")
A("""## Vorrat (einmal kaufen, hält mehrere Wochen)
- Öl, Essig, Senf, Gemüsebrühe, Salz, Pfeffer, Paprikapulver, Oregano
- Reste, die von Woche zu Woche bleiben dürfen: Nudeln, Kartoffeln (dunkel lagern), Parmesan, Pinienkerne, Mayo, Gewürzgurken, Röstzwiebeln, Eier

## Checkliste
- [ ] Samstag: Einkauf nach der Liste der Woche
- [ ] Sonntag: 5 Boxen fertig (in Hähnchen-Wochen 4 mit Hähnchen, Freitags-Box ohne)
- [ ] Morgens: Schinken, Würstchen oder in Hähnchen-Wochen freitags die Hähnchenstreifen aus der Packung dazu
- [ ] Nach 2 Wochen: Gewichtsdurchschnitt prüfen und Werte mit der Tracking-App abgleichen

Siehe auch: [[Meal-Prep-App]]
""")
pathlib.Path(sys.argv[1]).write_text("\n".join(L))
