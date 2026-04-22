# Script — Von der Cloud ins Rack

Slot: 35 min. Ziel: **~30 min** Vortrag + 5 min Q&A.

**Kernthese:** Die technischen Probleme sind gelöst. Der harte Teil ist, Produkte und Prozesse neu zu denken, und zwar jenseits des IT-Silos.

---

## Titel (~20s)

- Veit Heller, Port Zero. Netzautomatisierung für regulierte und kommunale Umgebungen.
- Heute: warum die Rückkehr an die eigene Infrastruktur scheitert, obwohl die Technik längst steht.

---

## 1 · Das Problem (~4:00)

### Section divider (~10s)

### Warum überhaupt zurück? (~75s)
- Souveränität ist Auflage, nicht Präferenz.
- Data Act, NIS2, DORA, AI Act. Konkreter Handlungsdruck.
- Kommunen, KRITIS, Finanz.

### Der Komfort der Hyperscaler (~75s)
- Self-Service, APIs, Reproduzierbarkeit, klare Owner.
- Das ist Produktdesign, kein Zufall.

### Die Angst (~45s)
- Zitat stehen lassen.
- Das Bild bei Repatriation.

### Die eigentliche Frage (~45s)
- Nicht: „Wie automatisiere ich alles?"
- Sondern: „Warum scheitern die meisten Projekte, obwohl die Technik gelöst ist?"

---

## 2 · Die Technik ist das einfache Problem (~6:15)

### Section divider (~10s)

### Thesis hero (~30s)
- Automatisierungs-Pipelines bauen wir seit Jahren.
- Das ist Handwerk, nicht Wissenschaft.

### Architektur-Überblick (~100s)
- Drei Schichten. Saubere Verantwortungen.
- Quellen links: Ticket-System, Kundenportal, ERP, CRM, …
- Source of Truth, Automation, Pipeline.

### Source of Truth: DCIM/IPAM (~60s)
- Zentrales Modell: Standorte, Racks, IPs, VLANs, Mandanten.
- Kein Modell, keine Automatisierung.
- Netbox, Nautobot.

### Automatisierung als Ausführung (~60s)
- Idempotenz, Drift Detection, Pre/Post-Checks.
- Ansible, Nornir.

### Pipelines als Kontrollschicht (~50s)
- Request, Änderung, Review, Rollout.
- Merge Request = Change Request.

### Praxis: WOBCOM (~75s)
- Regionaler ISP der Stadtwerke Wolfsburg.
- In 6 Monaten vom Inventar zum ersten automatisierten Rollout.
- Stack: NetBox, GitLab, Ansible. Genau die drei Schichten.
- Technische Langfassung: DENOG 2019, „Automate yourself within six months", mit Christian Dieckhoff.

---

## 3 · Warum Projekte trotzdem scheitern (~3:00)

### Section divider (~10s)

### Trotzdem scheitern die meisten (~45s)
- Die Pipeline steht. Der Workflow nicht.
- Tech fertig, Organisation nicht.

### Silo: IT für IT (~40s)
- Die IT automatisiert für die IT.
- Niemand außerhalb weiß, dass die Pipeline existiert.

### Falsche Abstraktionsebene (~40s)
- Wir bauen Tooling. Die Teams haben Prozesse.
- Tooling automatisiert Schritte. Prozesse bleiben unberührt.

### Keine Anbindung ans Geschäft (~55s)
- Das Projekt bleibt im IT-Bereich.
- Niemand fragt die Fachteams.
- Schmerzhafte Workflows bleiben schmerzhaft.

---

## 4 · Daten folgen Produkten und Prozessen (~7:20)

### Section divider (~10s)

### Cloud als Produkt (~30s)
- Cloud-Komfort ist Produktdesign. Die Technik kam danach.

### Die Eigenschaften (~60s)
- Fünf Merkmale. Keines exklusiv für Hyperscaler.

### Was ist euer Produkt? (~50s)
- „VLAN einrichten" ist ein Ticket.
- „Mandantennetz bereitstellen" ist ein Produkt.
- Outcomes, keine Einzelaktionen.

### Vor der Technik (~60s)
- Drei Fragen: Produkte, Prozesse, Lohnt sich Automatisierung.
- Ohne Prozessklarheit automatisiert man Chaos.

### Vom impliziten zum expliziten Prozess (~45s)
- Aufschreiben, vereinfachen, automatisieren.
- Automatisierung ist der letzte Schritt.

### Dirks-Zitat (~50s)
- Stehen lassen, vorlesen.
- Schlechter Prozess bleibt schlecht.

### Wo Automatisierung Sinn macht (~50s)
- Kriterien: häufig, fehleranfällig, reproduzierbar.
- 80/20.

### Nicht alles. Nicht sofort. (~55s)
- 3 bis 5 Vorgänge. Rest bleibt manuell.
- Self-Service ist Ziel, nicht Start.

### Prozesse definieren Services (~40s)
- Der Servicekatalog ist kein Dokument.
- Er ist das, was die Pipelines können.

---

## 5 · Compliance als Nebenprodukt (~2:45)

### Section divider (~10s)

### Change Management wird einfacher (~75s)
- ITIL-Mapping. Alles automatisch da.
- Nebenprodukt, kein separater Aufwand.

### Audits und Zertifizierungen (~60s)
- ISO 27001, BSI, SOC 2.
- „Hier ist das Repo."

### Dokumentation als Nebenprodukt (~30s)
- Source of Truth stimmt → Doku stimmt.

---

## 6 · Brownfield-Muster (~3:00)

### Section divider (~10s)

### Kein Greenfield nötig (~30s)
- Brownfield ist der Normalfall.

### Schritt 1: Inventar und Modell (~50s)
- Bestand ins DCIM. Good enough für den ersten Prozess.

### Schritt 2: Ein Prozess, Ende zu Ende (~50s)
- Einen Prozess. Tief statt breit.

### Schritt 3: Ausweiten (~50s)
- Pipeline als Muster. Self-Service folgt.

---

## 7 · Fazit (~1:40)

### Section divider (~10s)

### Nicht Technik, sondern Klarheit (~50s)
- Automatisierung ist der einfache Teil.
- Der harte Teil: Produkte und Prozesse, Gespräche jenseits der IT.

### Rückführung als Upgrade (~50s)
- Cloud-Komfort ist reproduzierbar.
- Souveränität als Upgrade, nicht Rückschritt.

### Danke / Fragen (~10s)

---

## Zusammenfassung

| Abschnitt | Zeit |
|---|---|
| Titel | 0:20 |
| 1 · Das Problem | 4:00 |
| 2 · Die Technik ist das einfache Problem | 6:15 |
| 3 · Warum Projekte trotzdem scheitern | 3:00 |
| 4 · Daten folgen Produkten und Prozessen | 7:20 |
| 5 · Compliance als Nebenprodukt | 2:45 |
| 6 · Brownfield-Muster | 3:00 |
| 7 · Fazit | 1:40 |
| Danke | 0:10 |
| **Gesamt** | **~28:30** |

Slot 35 min. Ziel 30 min + 5 min Q&A. ~1:30 Puffer. Risikozonen: Sektionen 2 und 4 sind die schwersten; wenn sie auslaufen, absorbiert der Puffer. Wenn alle Sektionen straff laufen, bleibt mehr Q&A-Zeit.
